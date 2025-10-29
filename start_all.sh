#!/data/data/com.termux/files/usr/bin/bash
# ======================================
# 🚀 Script unificado: Painel + Bot Traidbolt
# Autor: Glauco (Traidbolt)
# ======================================

BOT_SESSION="trading-bot"
PAINEL_SESSION="painel"
VENV_PATH="$HOME/trading-bot-venv"
LOG_DIR="$(pwd)/logs"
BOT_SCRIPT="$(pwd)/bot.py"
APP_SCRIPT="$(pwd)/app.py"

echo "🔍 Verificando ambiente..."

# 🧱 Cria pasta de logs se não existir
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 Criando pasta de logs..."
    mkdir -p "$LOG_DIR"
fi

# ⚙️ Cria/ativa ambiente virtual
if [ ! -d "$VENV_PATH" ]; then
    echo "⚙️ Criando ambiente virtual..."
    python3 -m venv "$VENV_PATH"
fi
source "$VENV_PATH/bin/activate"

# 📦 Instala dependências essenciais
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install flask python-dotenv requests solana jupiter-api

# 🔄 Finaliza sessões antigas (se travadas)
if tmux has-session -t $BOT_SESSION 2>/dev/null; then
    echo "🧹 Limpando sessão antiga do bot..."
    tmux kill-session -t $BOT_SESSION
fi
if tmux has-session -t $PAINEL_SESSION 2>/dev/null; then
    echo "🧹 Limpando sessão antiga do painel..."
    tmux kill-session -t $PAINEL_SESSION
fi

# 🧠 Validação de arquivos
if [ ! -f "$BOT_SCRIPT" ]; then
    echo "❌ ERRO: bot.py não encontrado em $(pwd)"
    exit 1
fi
if [ ! -f "$APP_SCRIPT" ]; then
    echo "❌ ERRO: app.py não encontrado em $(pwd)"
    exit 1
fi

# 🧾 Cria logs com data/hora
BOT_LOG="$LOG_DIR/bot_$(date +%Y%m%d_%H%M%S).log"
PAINEL_LOG="$LOG_DIR/painel_$(date +%Y%m%d_%H%M%S).log"

# 🚀 Inicia o Painel Flask
echo "🖥️ Iniciando painel Flask..."
tmux new -ds $PAINEL_SESSION "source $VENV_PATH/bin/activate && python3 $APP_SCRIPT |& tee -a $PAINEL_LOG"

sleep 3

# 🚀 Inicia o Bot de Trade
echo "🤖 Iniciando trading bot..."
tmux new -ds $BOT_SESSION "source $VENV_PATH/bin/activate && python3 $BOT_SCRIPT |& tee -a $BOT_LOG"

sleep 2

# 🔗 Mostra informações
if tmux has-session -t $PAINEL_SESSION 2>/dev/null && tmux has-session -t $BOT_SESSION 2>/dev/null; then
    echo "✅ Tudo pronto!"
    echo "🔗 Painel Web: http://$(curl -s ifconfig.me):5000"
    echo "🖥️  Log Painel: $PAINEL_LOG"
    echo "🤖 Log Bot:     $BOT_LOG"
    echo ""
    echo "📜 Ver painel: tmux attach -t $PAINEL_SESSION"
    echo "📜 Ver bot:    tmux attach -t $BOT_SESSION"
    echo "↩️  Sair do log: Ctrl + B, depois D"
else
    echo "❌ Falha ao iniciar algum processo."
fi
