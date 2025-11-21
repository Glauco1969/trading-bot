@echo off
title 🚀 Traidbolt - Inicializador Automático
echo ===========================================
echo 🤖 Iniciando ambiente Traidbolt no Windows
echo ===========================================

REM 1️⃣ Verifica se o Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale em https://www.python.org/downloads/
    pause
    exit /b
)

REM 2️⃣ Ativa o ambiente virtual (ajuste o caminho se necessário)
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️ Ambiente virtual não encontrado, criando...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM 3️⃣ Instala dependências básicas
echo 📦 Instalando dependências principais...
pip install flask requests python-dotenv >nul 2>nul

REM 4️⃣ Inicia o Flask em segundo plano
echo 🚀 Iniciando o servidor Flask...
start cmd /k "python main.py"

REM 5️⃣ Espera alguns segundos para o Flask iniciar
timeout /t 5 >nul

REM 6️⃣ Inicia o ngrok automaticamente
echo 🌍 Conectando ngrok ao Flask (porta 5000)...
ngrok http 5000

pause
