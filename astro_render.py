from __future__ import annotations

import html
import os
import re
import tempfile
from typing import Any, Dict, List, Optional

from markdown import markdown

try:
    from weasyprint import HTML
except Exception:
    HTML = None

from astro_core import PLANET_PT, PLANET_SYMBOLS, ZODIAC_PT, ZODIAC_SYMBOLS


# ============================================
# HELPERS DE FORMATAÇÃO
# ============================================

def safe_filename(value: str, fallback: str = "mapa_astral") -> str:
    cleaned = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip()
    cleaned = re.sub(r"[-\s]+", "_", cleaned)
    return cleaned or fallback


def fmt_degree(value: float) -> str:
    degree = int(value)
    minute = int(round((value % 1) * 60))
    if minute == 60:
        degree += 1
        minute = 0
    return f"{degree:02d}°{minute:02d}'"


def fmt_position(pos: Dict[str, Any]) -> str:
    sign = pos["sign"]
    sign_pt = ZODIAC_PT.get(sign, sign)
    sign_symbol = ZODIAC_SYMBOLS.get(sign, "")
    retro = " ℞" if pos.get("retrograde") else ""
    return f"{pos['degree']:02d}°{pos['minute']:02d}' {sign_symbol} {sign_pt}{retro}"


def fmt_planet_name(planet: str) -> str:
    symbol = PLANET_SYMBOLS.get(planet, "")
    pt = PLANET_PT.get(planet, planet)
    return f"{symbol} {pt}".strip()


def fmt_aspect_phase(phase: str) -> str:
    if phase == "applicative":
        return "Aplicativo"
    if phase == "separative":
        return "Separativo"
    return phase or "-"


def normalize_interpretation_text(text: Optional[str]) -> str:
    text = (text or "").strip()
    if not text:
        return "Interpretação ainda não gerada."
    return text


# ============================================
# TABELAS
# ============================================

def build_positions_table(chart: Dict[str, Any]) -> str:
    rows = ["| Ponto | Posição | Casa |", "|---|---|---|"]
    ordered_names = [
        "Sun","Moon","Mercury","Venus","Mars",
        "Jupiter","Saturn","North Node","South Node","Part of Fortune",
    ]
    positions_by_name = {item["planet"]: item for item in chart["positions"]}

    for name in ordered_names:
        pos = positions_by_name.get(name)
        if not pos:
            continue
        rows.append(
            f"| {fmt_planet_name(name)} | {fmt_position(pos)} | {pos.get('house', '-')} |"
        )

    return "\n".join(rows)


def build_angles_table(chart: Dict[str, Any]) -> str:
    asc = chart["ascendant"]
    mc = chart["midheaven"]

    asc_sign_pt = ZODIAC_PT.get(asc["sign"], asc["sign"])
    mc_sign_pt = ZODIAC_PT.get(mc["sign"], mc["sign"])

    asc_symbol = ZODIAC_SYMBOLS.get(asc["sign"], "")
    mc_symbol = ZODIAC_SYMBOLS.get(mc["sign"], "")

    return "\n".join([
        "| Ângulo | Posição |",
        "|---|---|",
        f"| Ascendente | {fmt_degree(asc['degree'])} {asc_symbol} {asc_sign_pt} |",
        f"| Meio do Céu | {fmt_degree(mc['degree'])} {mc_symbol} {mc_sign_pt} |",
    ])


def build_dignities_table(chart: Dict[str, Any]) -> str:
    rows = ["| Planeta | Total | Essencial | Acidental |", "|---|---:|---:|---:|"]

    for item in chart.get("dignities", []):
        rows.append(
            f"| {fmt_planet_name(item['planet'])} | {item['totalScore']} | {item['essentialScore']} | {item['accidentalScore']} |"
        )

    return "\n".join(rows)


def build_dignities_details(chart: Dict[str, Any]) -> str:
    blocks: List[str] = []

    for item in chart.get("dignities", []):
        title = f"### {fmt_planet_name(item['planet'])}"

        essential = item.get("essentialDetails", [])
        accidental = item.get("accidentalDetails", [])

        section_lines = [
            title,
            f"**Pontuação total:** {item['totalScore']}",
            "",
            "**Dignidades essenciais**",
        ]

        section_lines.extend([f"- {x}" for x in essential] if essential else ["- Nenhuma"])
        section_lines.extend(["", "**Dignidades acidentais**"])
        section_lines.extend([f"- {x}" for x in accidental] if accidental else ["- Nenhuma"])

        blocks.append("\n".join(section_lines))

    return "\n\n".join(blocks)


def build_aspects_table(chart: Dict[str, Any]) -> str:
    rows = [
        "| Planeta A | Planeta B | Aspecto | Aplicativo/Separativo |",
        "|---|---|---|---|",
    ]

    essential_rank = {
        item["planet"]: item.get("essentialScore", 0)
        for item in chart.get("dignities", [])
    }

    valid_aspects = list(chart.get("aspects", []))

    valid_aspects.sort(
        key=lambda asp: (
            -essential_rank.get(asp.get("planet1"), float("-inf")),
            fmt_planet_name(asp.get("planet1", "")),
            fmt_planet_name(asp.get("planet2", "")),
            asp.get("aspect", ""),
        )
    )

    for asp in valid_aspects:
        rows.append(
            f"| {fmt_planet_name(asp['planet1'])} | {fmt_planet_name(asp['planet2'])} | {asp['aspect']} | {fmt_aspect_phase(asp.get('phase', ''))} |"
        )

    return "\n".join(rows)


# ============================================
# MARKDOWN PRINCIPAL
# ============================================

def render_chart_markdown(chart: Dict[str, Any], name: str, birth_date: str, birth_time: str, birth_place: str) -> str:

    title_name = name.strip() or "Sem nome"
    place_text = birth_place.strip() or "Local não informado"

    parts = [
        f"# Crônicas Celestes — Mapa de {title_name}",
        "",
        f"**Nascimento:** {birth_date} às {birth_time}",
        f"**Local:** {place_text}",
        "",
        "## Ângulos",
        build_angles_table(chart),
        "",
        "## Posições planetárias",
        build_positions_table(chart),
        "",
        "## Pontuações de dignidade",
        build_dignities_table(chart),
        "",
        "## Detalhamento das dignidades",
        build_dignities_details(chart),
        "",
        "## Aspectos",
        build_aspects_table(chart),
    ]

    return "\n".join(parts).strip() + "\n"


# ============================================
# HTML + PDF
# ============================================

def render_full_html(chart_markdown: str, interpretation_text: Optional[str], title: str):

    chart_html = markdown(chart_markdown, extensions=["tables", "fenced_code", "nl2br"])

    interp_text = html.escape(
        normalize_interpretation_text(interpretation_text)
    ).replace("\n", "<br>")

    title_escaped = html.escape(title)

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{title_escaped}</title>

<style>

@page {{
size:A4;
margin:2cm;
}}

body {{
font-family: "Garamond","Georgia","Times New Roman",serif;
font-size:12pt;
line-height:1.7;
color:#1a1625;
}}

h1 {{
font-size:26pt;
border-bottom:3px solid #7c3aed;
padding-bottom:6px;
margin-bottom:20px;
}}

h2 {{
font-size:18pt;
margin-top:32px;
border-bottom:1px solid #c4b5fd;
padding-bottom:4px;
}}

h3 {{
font-size:14pt;
margin-top:22px;
}}

p,li {{
text-align:justify;
}}

table {{
width:100%;
border-collapse:collapse;
margin:14px 0 20px 0;
font-size:10.5pt;
}}

th,td {{
border:1px solid #cfc7e6;
padding:7px 8px;
}}

th {{
background:#e9e2ff;
color:#2a165e;
font-weight:700;
}}

tr:nth-child(even) td {{
background:#faf7ff;
}}

.page-break {{
page-break-before:always;
}}

.box {{
background:#f7f3ff;
border:1px solid #d6ccff;
border-radius:12px;
padding:22px;
font-size:12pt;
line-height:1.8;
}}

</style>

</head>

<body>

{chart_html}

<div class="page-break"></div>

<h2>Interpretação</h2>

<div class="box">
{interp_text}
</div>

</body>
</html>
"""


def export_pdf(name: str, chart_markdown: str, interpretation_text: Optional[str]):

    output_dir = tempfile.gettempdir()

    filename = safe_filename(name or "mapa_astral") + ".pdf"

    output_path = os.path.join(output_dir, filename)

    html_content = render_full_html(
        chart_markdown,
        interpretation_text,
        f"Crônicas Celestes — {name}",
    )

    if HTML is None:
        raise RuntimeError("WeasyPrint não instalado")

    HTML(string=html_content).write_pdf(output_path)

    return output_path


# ============================================
# OUTPUT PARA GRADIO
# ============================================

def build_render_payload(chart, name, birth_date, birth_time, birth_place):

    chart_markdown = render_chart_markdown(
        chart,
        name,
        birth_date,
        birth_time,
        birth_place,
    )

    return {
        "markdown": chart_markdown,
        "html": ""
    }