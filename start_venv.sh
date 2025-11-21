#!/bin/bash
# ==========================================
# 🚀 Script de inicialização do projeto Flask
# Autor: Glauco (Traidbolt)
# ==========================================

VENV_DIR="venv"
APP_FILE="app.py"

echo "🔍 Verificando ambiente..."

# Cria o venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv $VENV_DIR
fi

# Ativa o venv
echo "⚙️ Ativando ambiente virtual..."
source $VENV_DIR/bin/activate

# Instala dependências
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
else
    echo "📦 Instalando Flask e dotenv..."
    pip install flask python-dotenv
fi

# Inicia o app Flask
echo "🚀 Iniciando aplicação Flask..."
python $APP_FILE
