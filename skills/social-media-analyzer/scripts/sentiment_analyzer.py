import sys
import json
import os
from openai import OpenAI

# A chave da API será lida da variável de ambiente OPENAI_API_KEY
# O cliente OpenAI é inicializado automaticamente com as credenciais do ambiente.
client = OpenAI()

def analyze_sentiment_and_topics(text):
    """
    Analisa o sentimento e extrai tópicos de um texto usando a API da OpenAI.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": 'Você é um especialista em análise de mídias sociais. Analise o texto fornecido e retorne um objeto JSON com duas chaves: "sentiment" (pode ser "positive", "negative", ou "neutral") e "topics" (uma lista de 1 a 3 palavras-chave que resumem o assunto).'
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Erro ao analisar o texto: {e}", file=sys.stderr)
        return {"sentiment": "error", "topics": []}

def main():
    """
    Função principal para ler os dados, analisar e salvar os resultados.
    """
    if len(sys.argv) != 3:
        print("Uso: python sentiment_analyzer.py <arquivo_de_entrada> <arquivo_de_saida>", file=sys.stderr)
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    analyzed_posts = []

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    post = json.loads(line.strip())
                    text_to_analyze = post.get("text", "")
                    if text_to_analyze:
                        analysis_result = analyze_sentiment_and_topics(text_to_analyze)
                        post.update(analysis_result)
                        analyzed_posts.append(post)
                except json.JSONDecodeError:
                    print(f"Aviso: Ignorando linha mal formatada: {line.strip()}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada não encontrado em '{input_file_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(analyzed_posts, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Erro ao escrever no arquivo de saída '{output_file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Análise concluída. {len(analyzed_posts)} posts analisados e salvos em '{output_file_path}'.")

if __name__ == "__main__":
    main()
