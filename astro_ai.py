from __future__ import annotations

import json
import os
from typing import Any, Dict, Generator, Optional

import requests


# ============================================
# CONFIGURAÇÃO Z-AI
# ============================================

ZAI_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DEFAULT_MODEL = "glm-5"
DEFAULT_MAX_TOKENS = 32768
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TIMEOUT = 1200

ALLOWED_PROMPT_PLANETS = {
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
}


# ============================================
# BLOCO TÉCNICO DO CÁLCULO PARA O PROMPT
# ============================================


def build_chart_calculation_block(chart: Dict[str, Any]) -> str:
    """
    Gera apenas a entrada técnica do cálculo para o prompt.

    Conteúdo incluído:
    - Ascendente e Meio do Céu (posição + signo)
    - sete planetas na ordem já recebida em chart['dignities']
      (assumindo que o core já ordenou por dignidade essencial)
    - tabela de aspectos válidos já filtrados pelo cálculo

    Conteúdo excluído:
    - nodos
    - parte da fortuna
    - tabela completa de dignidades
    - regentes das casas
    - metadados extras
    """
    positions_by_planet = {
        item["planet"]: item
        for item in chart.get("positions", [])
        if item.get("planet") in ALLOWED_PROMPT_PLANETS
    }

    dignities = [
        item
        for item in chart.get("dignities", [])
        if item.get("planet") in ALLOWED_PROMPT_PLANETS
    ]

    lines = []
    lines.append("# DADOS DO MAPA")
    lines.append("")
    lines.append("## Ângulos")
    lines.append(
        f"- Ascendente: {chart['ascendant']['sign']} {chart['ascendant']['degree']:.2f}°"
    )
    lines.append(
        f"- Meio do Céu: {chart['midheaven']['sign']} {chart['midheaven']['degree']:.2f}°"
    )
    lines.append("")
    lines.append("## Planetas ordenados por dignidade essencial")

    for idx, dignity in enumerate(dignities, start=1):
        planet = dignity["planet"]
        pos = positions_by_planet.get(planet)
        if not pos:
            continue

        detail_text = "; ".join(dignity.get("essentialDetails", [])) or "Nenhum"
        lines.append(
            f"{idx}. {planet} — {pos['sign']} {pos['degree']:02d}°{pos['minute']:02d}' — Casa {pos.get('house', '-')}"
        )
        lines.append(f"   - Dignidade essencial: {dignity.get('essentialScore', 0)}")
        lines.append(f"   - Detalhes essenciais: {detail_text}")
        lines.append("")

    lines.append("## Aspectos válidos")
    lines.append("| Planeta A | Planeta B | Aspecto | Aplicativo/Separativo |")
    lines.append("|---|---|---|---|")

    for aspect in chart.get("aspects", []):
        planet1 = aspect.get("planet1")
        planet2 = aspect.get("planet2")
        if planet1 not in ALLOWED_PROMPT_PLANETS or planet2 not in ALLOWED_PROMPT_PLANETS:
            continue

        phase = "Aplicativo" if aspect.get("phase") == "applicative" else "Separativo"
        lines.append(
            f"| {planet1} | {planet2} | {aspect.get('aspect', '')} | {phase} |"
        )

    lines.append("")
    return "\n".join(lines)


# ============================================
# PROMPT
# ============================================


def build_interpretation_prompt(chart: Dict[str, Any]) -> str:
    calculation_block = build_chart_calculation_block(chart)

    instructions = """
Você opera exclusivamente em astrologia tradicional, usando whole sign houses. Cada signo corresponde integralmente a uma casa. Regências são somente tradicionais; planetas modernos não regem casas. Você escreve em prosa contínua, em terceira pessoa, com parágrafos densos e articulados. Evite listas, bullets, linguagem terapêutica, motivacional ou new age. Qualidades, limitações e contradições devem ser explicitadas.

1.

Para cada planeta, descreva como sua expressão resulta da combinação entre sua natureza, o signo onde se encontra e sua dignidade essencial. Na ordem recebida (dignidade essencial maior para o menor).

2.

Terminados os planetas, passa ao exame das casas. Ordene pela localização dos planetas mais forte ao mais fraco.

Você deve analisar tudo o que cada casa contém, de forma exaustiva e definitiva:

- o planeta mais forte ali localizado, integrando signo, dignidade e efeitos dos aspectos;
- outros planetas eventualmente presentes nessa casa;
- o regente da casa, indicando onde se encontra no mapa e em que condições está.

Após essa análise, a casa é encerrada definitivamente.
Você não retorna a essa casa.

Em seguida, você analisa todas as casas cujos signos são regidos por esse primeiro planeta, aplicando o mesmo princípio:

- examine tudo o que estiver presente nessas casas;
- utilize o estado do regente para estruturar a leitura;
- explicite como os temas dessas casas interagem estruturalmente com os temas da casa onde o planeta está.

Cada casa é analisada por completo e encerrada.

Regra de progressão

Somente após concluir:

a casa onde o planeta está e

todas as casas que ele rege,

você passa ao próximo planeta do ranking, repetindo o procedimento apenas para casas ainda não analisadas.

Exemplo normativo:
Se Júpiter for o planeta mais forte e estiver na Casa 8 em Peixes, a leitura começa pela Casa 8; em seguida, passa à Casa 5 (Sagitário), regida por Júpiter, integrando quaisquer planetas ali; só então avança para o segundo planeta mais forte.

3. Redigir a interpretação final do mapa, obedecendo rigorosamente às regras abaixo.

Forma

Não mencione qualquer termo astrológico (planetas, signos, casas, aspectos, dignidades etc.).
Texto em prosa contínua, densa, em terceira pessoa, referindo-se sempre ao indivíduo como “ele” ou "ela".
Sem tom terapêutico ou linguagem motivacional.
Com previsões objetivas, precisas e específicas para a vida da pessoa.

Estrutura obrigatória

Cada parágrafo corresponde exatamente a uma casa, na mesma ordem em que as casas foram analisadas e encerradas na Etapa 2.

Cada parágrafo é uma tradução direta e fiel do que foi estabelecido naquela casa:

não adicionar significados,
não suavizar conclusões,
não deslocar temas para outras áreas da vida.

Conteúdo e coerência interna

As contradições estruturais já identificadas nas etapas anteriores devem reaparecer explicitamente nos lugares de origem corretos (ex.: força intelectual × fragilidade afirmativa; sentido de propósito × atraso; resistência × desgaste).

Essas contradições não devem ser resolvidas nem conciliadas: elas devem ser descritas como tensões constitutivas da experiência dele.

Densidade e ousadia interpretativa

Todos os parágrafos devem ter densidade equivalente.
Garanta a mesma extensão na descrição dos temas de cada casa.

Nas casas com testemunhos muito fortes (positivos ou negativos), como:

grande concentração de planetas,
efeitos muito benéficos ou muito maléficos,
clara dominância estrutural,

você deve ousar mais na precisão da leitura preditiva, descrevendo formas concretas de manifestação daquele tema no mapa.

Quando apropriado, isso inclui:

indicar campos profissionais específicos,
tipos recorrentes de experiência,
funções sociais plausíveis,
ou dois ou três exemplos claros de realização ou impasse.

Essas previsões devem ser apresentadas como promessas estruturais.

4. Tabela

Faça uma tabela síntese com as casas por linha, naquela mesma ordem, contendo duas colunas:  temas; previsões.
""".strip()

    return f"{calculation_block}\n\n{instructions}\n"


# ============================================
# CLIENTE Z-AI
# ============================================


def get_zai_api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = (explicit_api_key or os.getenv("ZAI_API_KEY", "")).strip()
    if not api_key:
        raise ValueError(
            "ZAI_API_KEY não configurada. Defina a variável de ambiente antes de gerar a interpretação."
        )
    return api_key



def build_zai_payload(
    prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    stream: bool = True,
) -> Dict[str, Any]:
    return {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": stream,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }



def build_zai_headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }



def iter_sse_content(response: requests.Response) -> Generator[str, None, None]:
    for line in response.iter_lines():
        if not line:
            continue

        line_str = line.decode("utf-8", errors="ignore")
        if not line_str.startswith("data: "):
            continue

        payload = line_str[6:]
        if payload == "[DONE]":
            break

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            continue

        choices = data.get("choices", [])
        if not choices:
            continue

        delta = choices[0].get("delta", {})
        content = delta.get("content", "")
        if content:
            yield content



def call_zai_stream(
    prompt: str,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Generator[str, None, None]:
    try:
        resolved_api_key = get_zai_api_key(api_key)
        headers = build_zai_headers(resolved_api_key)
        payload = build_zai_payload(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        response = requests.post(
            ZAI_API_URL,
            headers=headers,
            json=payload,
            timeout=timeout,
            stream=True,
        )

        if response.status_code != 200:
            error_msg = response.text
            try:
                error_json = response.json()
                error_msg = error_json.get("error", {}).get("message", error_msg)
            except Exception:
                pass
            yield f"❌ Erro API Z-AI ({response.status_code}): {error_msg}"
            return

        full_response = ""
        for chunk in iter_sse_content(response):
            full_response += chunk
            yield full_response

        if not full_response.strip():
            yield "❌ A API respondeu sem conteúdo textual."

    except requests.exceptions.ConnectionError:
        yield "❌ Erro de conexão. Verifique sua internet."
    except requests.exceptions.Timeout:
        yield "❌ Timeout: a API demorou muito para responder."
    except ValueError as exc:
        yield f"❌ {exc}"
    except Exception as exc:
        yield f"❌ Erro inesperado: {exc}"



def call_zai_once(
    prompt: str,
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> str:
    resolved_api_key = get_zai_api_key(api_key)
    headers = build_zai_headers(resolved_api_key)
    payload = build_zai_payload(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=False,
    )

    response = requests.post(
        ZAI_API_URL,
        headers=headers,
        json=payload,
        timeout=timeout,
        stream=False,
    )
    response.raise_for_status()

    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        return ""

    return choices[0].get("message", {}).get("content", "")


# ============================================
# GERADORES PARA O GRADIO
# ============================================


def generate_interpretation_stream_from_chart(
    chart: Dict[str, Any],
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> Generator[str, None, None]:
    if not chart:
        yield "❌ Calcule o mapa primeiro."
        return

    prompt = build_interpretation_prompt(chart)
    yield from call_zai_stream(prompt=prompt, model=model, api_key=api_key)



def generate_interpretation_once_from_chart(
    chart: Dict[str, Any],
    model: str = DEFAULT_MODEL,
    api_key: Optional[str] = None,
) -> str:
    prompt = build_interpretation_prompt(chart)
    return call_zai_once(prompt=prompt, model=model, api_key=api_key)
