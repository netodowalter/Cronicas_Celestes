# Crônicas Celestes

Aplicação local em Python para **cálculo de mapa natal em astrologia tradicional**, geração de **interpretação por IA** e **exportação em PDF**.

O projeto foi dividido em quatro módulos principais para separar responsabilidades e facilitar manutenção:

- `astro_core.py` → cálculo astrológico (Swiss Ephemeris)
- `astro_render.py` → renderização Markdown / HTML / PDF
- `astro_ai.py` → prompt e integração com API Z‑AI
- `app.py` → interface Gradio

---

# Estrutura do projeto

```
cronicas_celestes/

astro_core.py
astro_render.py
astro_ai.py
app.py

requirements_cronicas_celestes.txt
executar_cronicas_celestes.bat
README.md
```

---

# Requisitos

Python recomendado:

```
Python 3.10 ou superior
```

Bibliotecas principais:

- gradio
- pyswisseph
- markdown
- weasyprint
- requests

Todas são instaladas automaticamente pelo `.bat`.

---

# Configurar chave da API

A interpretação usa a API **Z‑AI (BigModel)**.

Crie a variável de ambiente:

### Windows (PowerShell)

```
setx ZAI_API_KEY "SUA_CHAVE_AQUI"
```

Depois reinicie o terminal.

---

# Executar a aplicação

Basta clicar duas vezes em:

```
executar_cronicas_celestes.bat
```

O script irá:

1. Criar ambiente virtual
2. Instalar dependências
3. Iniciar o app Gradio

Depois abra no navegador:

```
http://127.0.0.1:7860
```

---

# Fluxo de uso

1️⃣ Preencher dados de nascimento

- Nome
- Data
- Hora
- Local

2️⃣ Buscar cidade (opcional)

O sistema usa **OpenStreetMap Nominatim** para preencher latitude e longitude.

3️⃣ Clicar em **Calcular mapa**

4️⃣ Abrir aba **Interpretação**

5️⃣ Clicar em **Gerar interpretação**

6️⃣ Exportar PDF se desejar

---

# Sistema astrológico

O cálculo segue astrologia tradicional:

- Casas **Whole Sign**
- Regências **clássicas apenas**
- Dignidades:

  - domicílio
  - exaltação
  - triplicidade
  - termo
  - face

- Avaliação de dignidade:

  - essencial
  - acidental

- Pontos adicionais:

  - Nodo Norte
  - Nodo Sul
  - Parte da Fortuna

---

# Exportação PDF

O PDF contém:

1. Mapa técnico
2. Tabelas de dignidades
3. Aspectos
4. Interpretação textual

A geração usa **WeasyPrint**.

---

# Problemas comuns

### WeasyPrint não instala

No Windows pode ser necessário instalar dependências do GTK.

Se houver erro:

```
pip install weasyprint
```

Consulte:

https://weasyprint.org/docs/install/

---

### API não responde

Verifique se a variável foi definida:

```
ZAI_API_KEY
```

---

### Erro de cálculo do Swiss Ephemeris

Reinstale:

```
pip install pyswisseph
```

---

# Melhorias futuras

Ideias para evolução do projeto:

- mapa gráfico circular
- escolha de estilo interpretativo
- múltiplos modelos de IA
- cache de cidades
- timezone automático
- geração de relatório expandido

---

# Licença

Uso educacional e experimental.

---

# Autor

Projeto desenvolvido para o assistente **Crônicas Celestes**.

