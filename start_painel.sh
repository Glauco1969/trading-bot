#!/data/data/com.termux/files/usr/bin/bash
# ======================================
# 🖥️ Start do Painel Flask (Traidbolt)
# ======================================

SESSION_NAME="painel"
VENV_PATH="$HOME/trading-bot-venv"
LOG_DIR="$(pwd)/logs"
APP_SCRIPT="$(pwd)/app.py"

echo "🔍 Verificando ambiente do painel..."

# 🛑 Evita rodar se já estiver ativo
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "⚠️ O painel já está em execução."
    exit 1
fi

# Cria pasta de logs
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 Criando pasta de logs..."
    mkdir -p "$LOG_DIR"
fi

# Ativa ambiente virtual
if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️ Criando ambiente virtual..."
    python3 -m venv "$VENV_PATH"
fi
source "$VENV_PATH/bin/activate"

# Instala dependências mínimas se necessário
pip install --upgrade pip
pip install flask python-dotenv requests

# Testa se o app.py existe
if [ ! -f "$APP_SCRIPT" ]; then
    echo "❌ ERRO: app.py não encontrado em $(pwd)"
    exit 1
fi

# Mata sessão antiga, se travada
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    tmux kill-session -t $SESSION_NAME
fi

# Cria log com data/hora
LOG_FILE="$LOG_DIR/painel_$(date +%Y%m%d_%H%M%S).log"

# Inicia painel Flask acessível externamente
echo "🚀 Iniciando painel web Flask..."
tmux new -ds $SESSION_NAME "source $VENV_PATH/bin/activate && python3 $APP_SCRIPT |& tee -a $LOG_FILE"

sleep 2
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Painel iniciado com sucesso!"
    echo "🔗 Acesse: http://$(curl -s ifconfig.me):5000"
    echo "📜 Logs:   $LOG_FILE"
    echo "   ↩️ Sair do log: Ctrl + B, depois D"
else
    echo "❌ Falha ao iniciar o painel."
fi
