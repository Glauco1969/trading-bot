#!/bin/bash
# ======================================
# 🚀 Start script do Trading Bot (auto-restart)
# Autor: Glauco (projeto Traidbolt)
# ======================================

#!/bin/bash
# Evita múltiplas instâncias
if pgrep -f start.sh > /dev/null; then
  echo "⚠️ Já existe uma instância rodando!"
  exit 1
fi


SESSION_NAME="trading-bot"
VENV_PATH="$HOME/trading-bot-venv"
BOT_SCRIPT="$(pwd)/bot.py"
LOG_DIR="$(pwd)/logs"

echo "🔍 Verificando ambiente..."

# Cria pasta de logs se não existir
mkdir -p "$LOG_DIR"

# Verifica ambiente virtual
if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️ Criando ambiente virtual..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    [ -f requirements.txt ] && pip install -r requirements.txt
else
    source "$VENV_PATH/bin/activate"
fi

# Testa se bot.py existe
if [ ! -f "$BOT_SCRIPT" ]; then
    echo "❌ ERRO: bot.py não encontrado!"
    exit 1
fi

# Mata sessão antiga, se existir
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "🧹 Encerrando sessão antiga..."
    tmux kill-session -t $SESSION_NAME
fi

# Inicia nova sessão tmux com loop de auto-restart
tmux new -ds $SESSION_NAME "
while true; do
    LOG_FILE='$LOG_DIR/bot_\$(date +%Y%m%d_%H%M%S).log'
    echo '🚀 Iniciando bot... Logs: '\$LOG_FILE
    source $VENV_PATH/bin/activate
    python3 $BOT_SCRIPT |& tee \$LOG_FILE
    echo '⚠️  Bot caiu! Reiniciando em 5s...'
    sleep 5
done
"

sleep 1
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Bot iniciado com auto-restart!"
    echo "   📜 Ver logs: tmux attach -t $SESSION_NAME"
    echo "   ❌ Parar bot: ./stop.sh"
else
    echo "❌ Falha ao iniciar o bot."
fi

chmod +x start.sh
./start.sh

