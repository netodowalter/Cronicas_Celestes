import sys
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def plot_sentiment_distribution(df, output_dir):
    """Gera um gráfico de pizza da distribuição de sentimentos."""
    sentiment_counts = df['sentiment'].value_counts()
    colors = {'positive': '#4CAF50', 'neutral': '#FFC107', 'negative': '#F44336', 'error': '#9E9E9E'}
    
    plt.figure(figsize=(8, 6))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=[colors.get(s, '#9E9E9E') for s in sentiment_counts.index])
    plt.title('Distribuição de Sentimentos', fontsize=16)
    plt.ylabel('')
    plt.savefig(os.path.join(output_dir, 'sentiment_distribution.png'))
    plt.close()

def plot_top_topics(df, output_dir, top_n=10):
    """Gera um gráfico de barras dos tópicos mais frequentes."""
    all_topics = [topic for sublist in df['topics'] for topic in sublist]
    topic_counts = Counter(all_topics).most_common(top_n)
    
    if not topic_counts:
        print("Nenhum tópico encontrado para gerar o gráfico.")
        return

    topics, counts = zip(*topic_counts)
    
    plt.figure(figsize=(10, 7))
    plt.barh(topics, counts, color='#2196F3')
    plt.xlabel('Número de Menções')
    plt.title(f'Top {top_n} Tópicos Mais Discutidos')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_topics.png'))
    plt.close()

def plot_engagement_pattern(df, output_dir):
    """Gera um gráfico de linha do volume de menções ao longo do tempo."""
    if 'collected_at' not in df.columns:
        print("Coluna 'collected_at' não encontrada para gerar padrão de engajamento.")
        return

    df['collected_at'] = pd.to_datetime(df['collected_at'], errors='coerce')
    df.dropna(subset=['collected_at'], inplace=True)
    
    if df.empty:
        print("Nenhum dado de data válido para gerar o gráfico de engajamento.")
        return

    mentions_by_day = df.set_index('collected_at').resample('D').size()
    
    plt.figure(figsize=(12, 6))
    mentions_by_day.plot(kind='line', marker='o', linestyle='-')
    plt.title('Volume de Menções por Dia')
    plt.xlabel('Data')
    plt.ylabel('Número de Menções')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'engagement_pattern.png'))
    plt.close()

def main():
    """Função principal para gerar todos os gráficos."""
    if len(sys.argv) != 3:
        print("Uso: python chart_generator.py <arquivo_json_de_entrada> <diretorio_de_saida>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    except (FileNotFoundError, json.JSONDecodeError, pd.errors.EmptyDataError) as e:
        print(f"Erro ao ler ou processar o arquivo de entrada: {e}", file=sys.stderr)
        sys.exit(1)

    if df.empty:
        print("O arquivo de dados está vazio. Nenhum gráfico será gerado.")
        return

    plot_sentiment_distribution(df, output_dir)
    plot_top_topics(df, output_dir)
    plot_engagement_pattern(df, output_dir)

    print(f"Gráficos salvos com sucesso em '{output_dir}'.")

if __name__ == "__main__":
    main()
