from __future__ import annotations

import os
from typing import Any, Dict

import gradio as gr
import requests

from astro_ai import DEFAULT_MODEL, generate_interpretation_stream_from_chart
from astro_core import calculate_chart, calculate_chart_legacy
from astro_render import build_render_payload, export_pdf


APP_TITLE = "Crônicas Celestes"
APP_DESCRIPTION = (
    "Mapa natal em astrologia tradicional com cálculo técnico, "
    "interpretação por IA e exportação em PDF."
)

MODEL_CHOICES = [
    ("GLM-5", "glm-5"),
    ("GLM-4.7", "glm-4.7"),
]

TIMEZONE_SUGGESTIONS = [
    "America/Sao_Paulo",
    "America/Recife",
    "America/Manaus",
    "America/Rio_Branco",
    "Europe/Lisbon",
    "Europe/London",
    "America/New_York",
    "UTC",
]


CITY_CACHE: Dict[str, Dict[str, float]] = {}


# ---------------------------------------------------------
# BUSCA DE CIDADES (campo unificado com Local)
# ---------------------------------------------------------

def search_cities(query: str):
    if not query or len(query.strip()) < 2:
        return []

    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "format": "json",
                "limit": 8,
            },
            headers={"User-Agent": "CronicasCelestes"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
    except Exception:
        return []

    results = []
    for item in data:
        label = item["display_name"]
        try:
            lat = float(item["lat"])
            lon = float(item["lon"])
        except Exception:
            continue
        results.append((label, {"latitude": lat, "longitude": lon}))

    return results


def update_city_dropdown(birth_place: str):
    """Busca cidades a partir do texto digitado no campo Local."""
    CITY_CACHE.clear()
    results = search_cities(birth_place)

    if not results:
        return gr.update(choices=[], value=None), None, None

    labels = []
    for label, coords in results:
        CITY_CACHE[label] = coords
        labels.append(label)

    first = results[0][1]
    return (
        gr.update(choices=labels, value=labels[0]),
        first["latitude"],
        first["longitude"],
    )


def select_city(label: str):
    """Ao selecionar uma cidade no dropdown, atualiza lat/lon e o campo Local."""
    coords = CITY_CACHE.get(label)
    if not coords:
        return None, None, gr.update()
    return coords["latitude"], coords["longitude"], label


# ---------------------------------------------------------
# CÁLCULO
# ---------------------------------------------------------

def validate_inputs(
    name: str,
    birth_date: str,
    birth_time: str,
    latitude: Any,
    longitude: Any,
    timezone_name: str,
) -> str | None:
    if not name or not name.strip():
        return "❌ Informe o nome."
    if not birth_date or not birth_date.strip():
        return "❌ Informe a data de nascimento no formato YYYY-MM-DD."
    if not birth_time or not birth_time.strip():
        return "❌ Informe o horário no formato HH:MM."
    if latitude is None or longitude is None:
        return "❌ Informe latitude e longitude."
    if not timezone_name or not timezone_name.strip():
        return "❌ Informe um timezone IANA, como America/Sao_Paulo."
    return None


def calculate_and_render(
    name,
    birth_date,
    birth_time,
    birth_place,
    latitude,
    longitude,
    timezone_name,
):
    error = validate_inputs(name, birth_date, birth_time, latitude, longitude, timezone_name)
    if error:
        return None, "", error, ""

    try:
        chart = calculate_chart(
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=float(latitude),
            longitude=float(longitude),
            tz_name=timezone_name,
        )

        render_payload = build_render_payload(
            chart,
            name,
            birth_date,
            birth_time,
            birth_place,
        )

        return (
            chart,
            render_payload["markdown"],
            "✅ Mapa calculado",
            "",
        )

    except Exception as e:
        return None, "", f"❌ Erro: {e}", ""


# ---------------------------------------------------------
# INTERPRETAÇÃO
# ---------------------------------------------------------

def generate_interpretation(chart, model):
    if not chart:
        yield "❌ Calcule o mapa primeiro."
        return

    yield from generate_interpretation_stream_from_chart(
        chart=chart,
        model=model or DEFAULT_MODEL,
        api_key=os.getenv("ZAI_API_KEY"),
    )


# ---------------------------------------------------------
# PDF
# ---------------------------------------------------------

def export_current_pdf(name, chart_markdown, interpretation_text):
    if not chart_markdown:
        raise gr.Error("Calcule o mapa antes.")

    return export_pdf(
        name=name,
        chart_markdown=chart_markdown,
        interpretation_text=interpretation_text,
    )


# ---------------------------------------------------------
# COMPATIBILIDADE LEGADA
# ---------------------------------------------------------

def calculate_with_legacy_timezone(
    name,
    birth_date,
    birth_time,
    birth_place,
    latitude,
    longitude,
    timezone_offset,
):
    if not name or not birth_date or not birth_time or latitude is None or longitude is None:
        return None, "", "❌ Preencha nome, data, hora, latitude e longitude.", ""

    try:
        chart = calculate_chart_legacy(
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=float(latitude),
            longitude=float(longitude),
            timezone_value=timezone_offset,
        )

        render_payload = build_render_payload(
            chart,
            name,
            birth_date,
            birth_time,
            birth_place,
        )

        return (
            chart,
            render_payload["markdown"],
            "✅ Mapa calculado com offset legado.",
            "",
        )

    except Exception as e:
        return None, "", f"❌ Erro: {e}", ""


# ---------------------------------------------------------
# INTERFACE
# ---------------------------------------------------------

def build_app():
    with gr.Blocks(title=APP_TITLE) as demo:
        chart_state = gr.State(None)
        chart_markdown_state = gr.State("")
        interpretation_state = gr.State("")

        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(APP_DESCRIPTION)

        status_box = gr.Markdown()

        with gr.Tabs():
            with gr.Tab("Dados"):
                name = gr.Textbox(label="Nome")
                birth_date = gr.Textbox(label="Data", placeholder="YYYY-MM-DD")
                birth_time = gr.Textbox(label="Hora", placeholder="HH:MM")

                # Campo Local unificado: digita o nome da cidade e clica Buscar
                birth_place = gr.Textbox(
                    label="Local",
                    placeholder="Digite a cidade e clique Buscar",
                )
                search_btn = gr.Button("Buscar")
                city_dropdown = gr.Dropdown(
                    label="Resultados",
                    visible=True,
                )

                latitude = gr.Number(label="Latitude")
                longitude = gr.Number(label="Longitude")

                timezone_name = gr.Dropdown(
                    label="Timezone",
                    choices=TIMEZONE_SUGGESTIONS,
                    value="America/Sao_Paulo",
                    allow_custom_value=True,
                )

                with gr.Accordion("Compatibilidade com offset antigo", open=False):
                    legacy_timezone = gr.Number(label="Offset GMT antigo", value=-3)
                    calc_legacy_btn = gr.Button("Calcular com offset legado")

                calc_btn = gr.Button("Calcular mapa")

            with gr.Tab("Mapa"):
                chart_markdown = gr.Markdown()

            with gr.Tab("Interpretação"):
                model = gr.Dropdown(
                    label="Modelo",
                    choices=MODEL_CHOICES,
                    value=DEFAULT_MODEL,
                )
                interpret_btn = gr.Button("Gerar interpretação")

                interpretation = gr.Markdown(
                    label="Leitura",
                    elem_classes=["interpretation-box"],
                )

            with gr.Tab("PDF"):
                export_btn = gr.Button("Exportar PDF")
                pdf_file = gr.File()

        # --- Busca: usa o campo Local como input ---
        search_btn.click(
            update_city_dropdown,
            birth_place,
            [city_dropdown, latitude, longitude],
        )

        # --- Ao selecionar no dropdown, atualiza lat/lon E o campo Local ---
        city_dropdown.change(
            select_city,
            city_dropdown,
            [latitude, longitude, birth_place],
        )

        calc_btn.click(
            calculate_and_render,
            [
                name,
                birth_date,
                birth_time,
                birth_place,
                latitude,
                longitude,
                timezone_name,
            ],
            [chart_state, chart_markdown_state, status_box, interpretation],
        ).then(
            lambda md: md,
            chart_markdown_state,
            chart_markdown,
        )

        calc_legacy_btn.click(
            calculate_with_legacy_timezone,
            [
                name,
                birth_date,
                birth_time,
                birth_place,
                latitude,
                longitude,
                legacy_timezone,
            ],
            [chart_state, chart_markdown_state, status_box, interpretation],
        ).then(
            lambda md: md,
            chart_markdown_state,
            chart_markdown,
        )

        interpret_btn.click(
            generate_interpretation,
            [chart_state, model],
            interpretation,
        ).then(
            lambda x: x,
            interpretation,
            interpretation_state,
        )

        export_btn.click(
            export_current_pdf,
            [name, chart_markdown_state, interpretation_state],
            pdf_file,
        )

    return demo


app = build_app()


if __name__ == "__main__":
    app.launch()
