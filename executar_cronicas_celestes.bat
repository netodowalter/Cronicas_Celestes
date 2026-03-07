@echo off
setlocal
cd /d "%~dp0"

if not exist venv (
    echo [1/5] Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual.
    pause
    exit /b 1
)

echo [2/5] Atualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Falha ao atualizar o pip.
    pause
    exit /b 1
)

echo [3/5] Instalando dependencias...
pip install -r requirements_cronicas_celestes.txt
if errorlevel 1 (
    echo Falha ao instalar as dependencias.
    pause
    exit /b 1
)

if "%ZAI_API_KEY%"=="" (
    echo [4/5] Aviso: ZAI_API_KEY nao esta definida.
    echo O app vai abrir, mas a aba de interpretacao nao funcionara sem essa variavel.
) else (
    echo [4/5] ZAI_API_KEY detectada.
)

echo [5/5] Iniciando app...
python app.py

if errorlevel 1 (
    echo O app foi encerrado com erro.
) else (
    echo App encerrado.
)

pause
