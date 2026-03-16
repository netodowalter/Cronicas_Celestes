---
name: social-media-analyzer
description: "Monitore e analise o conteúdo de mídias sociais sobre um time, marca ou tópico. Realize análise de sentimentos, identifique tendências e forneça insights e planos de ação em uma apresentação de slides profissional."
---

# Social Media Analyzer

Esta skill transforma o Manus em um analista de mídias sociais, capaz de conduzir uma análise completa desde a coleta de dados até a apresentação de insights estratégicos.

## Workflow Principal

O processo de análise de mídias sociais é dividido nas seguintes fases:

1.  **Coleta de Requisitos**: Entender as necessidades do usuário.
2.  **Coleta de Dados**: Buscar menções e discussões nas mídias sociais.
3.  **Análise de Sentimentos e Tendências**: Processar os dados coletados para extrair insights.
4.  **Criação do Conteúdo da Apresentação**: Estruturar os resultados em um formato de apresentação.
5.  **Geração da Apresentação**: Criar os slides com visualizações de dados.

### Fase 1: Coleta de Requisitos

Faça as seguintes perguntas ao usuário para definir o escopo da análise:

- Qual é o tópico, marca ou time a ser analisado?
- Qual o período de análise desejado?
- Quais plataformas de mídia social devem ser priorizadas (X/Twitter, Reddit, Instagram, etc.)?
- Existem preferências de cores para a apresentação (ex: cores da marca)?
- Há algum evento ou contexto específico a ser considerado?

### Fase 2: Coleta de Dados

Utilize a ferramenta `search` para encontrar menções relevantes. Varie as queries para cobrir diferentes plataformas e tipos de conteúdo.

- Use queries como `"[tópico]" site:twitter.com`, `"[tópico]" site:reddit.com`.
- Para cada resultado de busca relevante, use a ferramenta `browser` para extrair o conteúdo completo.
- Salve todo o conteúdo coletado em um arquivo de texto, por exemplo, `collected_data.txt`.
- Consulte `references/data_collection_guide.md` para dicas específicas por plataforma.

### Fase 3: Análise de Sentimentos e Tendências

Com os dados coletados, execute o script `scripts/sentiment_analyzer.py` para classificar o sentimento de cada menção.

```bash
python /home/ubuntu/skills/social-media-analyzer/scripts/sentiment_analyzer.py collected_data.txt analyzed_data.json
```

O script irá gerar um arquivo JSON com os dados analisados, incluindo o sentimento (positivo, neutro, negativo) e os tópicos principais.

### Fase 4: Criação do Conteúdo da Apresentação

Com base nos dados analisados, prepare o conteúdo para cada slide. Utilize o template `templates/slide_content_template.md` como guia.

Este arquivo markdown servirá como a fonte de dados para a geração dos slides.

### Fase 5: Geração da Apresentação

Primeiro, gere os gráficos necessários com o script `scripts/chart_generator.py`:

```bash
python /home/ubuntu/skills/social-media-analyzer/scripts/chart_generator.py analyzed_data.json charts/
```

Depois, use a ferramenta `slides` para criar a apresentação final, passando o arquivo de conteúdo e a contagem de slides.

```python
default_api.slides(
    brief="Gerar apresentação de análise de mídias sociais",
    slide_content_file_path="/home/ubuntu/path/to/your/slide_content.md",
    slide_count=9,
    generate_mode='html'
)
```

Consulte `references/presentation_structure.md` para a estrutura detalhada de cada slide.
