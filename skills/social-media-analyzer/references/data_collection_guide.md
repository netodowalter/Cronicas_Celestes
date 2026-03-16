# Guia de Coleta de Dados por Plataforma

Este guia oferece dicas para coletar dados de diferentes plataformas de mídia social usando as ferramentas disponíveis.

## Estratégia Geral

- **Combine `search` e `browser`**: Use `search` com operadores de site (`site:twitter.com`) para encontrar URLs relevantes e, em seguida, use `browser` para extrair o conteúdo completo da página. Isso é mais eficaz do que apenas confiar nos snippets de busca.
- **Documente tudo**: Salve o texto bruto, a URL de origem e a data de coleta para cada item em um arquivo `collected_data.txt` ou similar. Isso garante a rastreabilidade.
- **Seja específico nas buscas**: Use aspas para frases exatas (`"nome da marca"`) e combine com outros termos relevantes para focar a coleta.

## X/Twitter

- **Busca Avançada via `search`**: A busca do Google indexa o Twitter razoavelmente bem. Use queries como:
  - `"palavra-chave" site:twitter.com since:AAAA-MM-DD until:AAAA-MM-DD`
  - `from:nome_de_usuario "palavra-chave" site:twitter.com`
  - `"frase exata" lang:pt site:twitter.com`
- **Extração com `browser`**: Ao visitar uma URL de tweet, foque em extrair o texto do tweet principal, os comentários (se relevantes e visíveis) e as métricas de engajamento (likes, retweets).

## Reddit

- **Busca por Subreddit**: Foque a busca em subreddits relevantes para o tópico.
  - `"palavra-chave" site:reddit.com/r/subreddit_especifico`
- **Extração de Threads**: Ao usar o `browser` em uma thread do Reddit, extraia o post original (OP) e os comentários mais votados (`top comments`). A estrutura aninhada dos comentários pode ser complexa, então foque nos níveis superiores.
- **API PRAW**: Para uma coleta mais robusta, considere usar a biblioteca PRAW do Python em um script, mas para a maioria dos casos, a combinação `search` + `browser` é suficiente.

## Instagram & Facebook

- **Conteúdo Público**: A coleta é limitada a posts e comentários públicos. A busca dentro dessas plataformas é mais difícil externamente.
- **Foco em Hashtags**: Use `search` para encontrar discussões públicas em outras plataformas que mencionem hashtags populares do Instagram.
  - `"#hashtagdamarca" site:twitter.com`
- **Páginas Públicas**: Se a marca tiver uma página pública no Facebook, você pode navegar diretamente para ela com o `browser` e extrair o conteúdo dos posts e os comentários visíveis.

## Blogs e Notícias

- **Busca Geral**: Use a ferramenta `search` com o tipo `news` ou `info` para encontrar artigos e posts de blog.
  - `"nome da marca" review`
  - `"nome do time" notícias`
- **Extração de Artigos**: Use o `browser` com o `intent` `informational` e um `focus` claro para extrair o texto principal do artigo, ignorando anúncios e barras laterais.

## Exemplo de Registro de Dados (em `collected_data.txt`)

```json
{
  "source_url": "https://twitter.com/user/status/12345",
  "collected_at": "2026-03-16T14:30:00Z",
  "platform": "Twitter",
  "text": "Acabei de usar o produto X e é incrível! Recomendo a todos."
}
{
  "source_url": "https://www.reddit.com/r/gadgets/comments/abcde/review_product_x/",
  "collected_at": "2026-03-16T14:32:00Z",
  "platform": "Reddit",
  "text": "Minha análise do produto X: prós e contras. No geral, uma boa compra, mas a bateria poderia ser melhor."
}
```

Manter um formato estruturado como JSON por linha facilita o processamento posterior.
