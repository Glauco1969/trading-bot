#!/bin/bash
# ======================================
# 🚀 Start script do Trading Bot
# Autor: Glauco (projeto Traidbolt)
# ======================================

SESSION_NAME="trading-bot"
VENV_PATH="$HOME/trading-bot-venv"
LOG_DIR="$(pwd)/logs"
BOT_SCRIPT="$(pwd)/bot.py"

echo "🔍 Verificando ambiente..."

# Cria a pasta de logs se não existir
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 Criando pasta de logs..."
    mkdir -p "$LOG_DIR"
fi

# Verifica se o venv existe
if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️  Criando ambiente virtual..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
else
    source "$VENV_PATH/bin/activate"
fi

# Testa se o bot existe
if [ ! -f "$BOT_SCRIPT" ]; then
    echo "❌ ERRO: bot.py não encontrado em $(pwd)"
    exit 1
fi

# Mata sessão antiga, se existir
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "🧹 Finalizando sessão antiga..."
    tmux kill-session -t $SESSION_NAME
fi

# Inicia nova sessão tmux
echo "🚀 Iniciando trading bot em background..."
tmux new -ds $SESSION_NAME "source $VENV_PATH/bin/activate && python3 $BOT_SCRIPT |& tee $LOG_DIR/bot.log"

sleep 1
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Bot iniciado com sucesso!"
    echo "   📜 Ver logs:      tmux attach -t $SESSION_NAME"
    echo "   ❌ Parar bot:     ./stop.sh"
    echo "   📊 Status:        ./status.sh"
    echo "   ↩️  Sair do log:   Ctrl + B, depois D"
else
    echo "❌ Falha ao iniciar o bot."
fi
