@echo off
title Traidbolt - Início Automático
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

REM 2️⃣ Cria venv se não existir
if not exist venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM 3️⃣ Ativa o ambiente
call venv\Scripts\activate.bat

REM 4️⃣ Instala dependências
if exist requirements.txt (
    echo 📦 Instalando dependências...
    pip install -r requirements.txt
) else (
    echo ⚠️ Nenhum requirements.txt encontrado, instalando Flask...
    pip install flask
)

REM 5️⃣ Inicia o Flask
echo 🚀 Iniciando servidor Traidbolt Flask...
if exist main.py (
    python main.py
) else if exist app.py (
    python app.py
) else (
    echo ❌ Nenhum arquivo Flask encontrado (main.py ou app.py).
)

echo ===========================================
echo ✅ Painel iniciado! Pressione CTRL+C para encerrar.
echo ===========================================

pause

