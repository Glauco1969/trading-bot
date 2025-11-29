#!/data/data/com.termux/files/usr/bin/bash
# ======================================
# 🚀 Start script do Trading Bot (Traidbolt)
# ======================================

set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$HOME/projetos/tradingbot}"  # ajuste se precisar
SESSION_NAME="${SESSION_NAME:-trading-bot}"
VENV_DIR="${VENV_DIR:-venv}"
BOT_FILE="${BOT_FILE:-bot.py}"        # arquivo principal do bot
LOG_FILE="${LOG_FILE:-bot.log}"

log() { printf "[%s] %s
" "$(date +'%H:%M:%S')" "$*"; }
err() { printf "[ERRO %s] %s
" "$(date +'%H:%M:%S')" "$*" >&2; }

log "📁 Indo para a pasta do projeto: $PROJECT_DIR"
cd "$PROJECT_DIR" || { err "Projeto não encontrado em $PROJECT_DIR"; exit 1; }

# 1) checa tmux
if ! command -v tmux >/dev/null 2>&1; then
  err "tmux não está instalado. Instale com: pkg install tmux"
  exit 1
fi

# 2) checa arquivo do bot
if [ ! -f "$BOT_FILE" ]; then
  err "Arquivo do bot '$BOT_FILE' não encontrado."
  exit 1
fi

# 3) cria venv se não existir
if [ ! -d "$VENV_DIR" ]; then
  log "📦 Criando ambiente virtual em '$VENV_DIR'..."
  python -m venv "$VENV_DIR" || { err "Falha ao criar venv."; exit 1; }
fi

# 4) prepara comando de inicialização
START_CMD="source $VENV_DIR/bin/activate && \
  pip install -r requirements.txt 2>/dev/null || true && \
  echo '🚀 Iniciando bot...' && \
  python $BOT_FILE 2>&1 | tee -a $LOG_FILE"

# 5) evita duplicar sessão
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  log "⚠️ Sessão '$SESSION_NAME' já está ativa."
  log "👉 Para anexar: tmux attach -t $SESSION_NAME"
  exit 0
fi

# 6) cria sessão tmux e roda o bot
log "🧠 Criando sessão tmux: $SESSION_NAME"
tmux new-session -d -s "$SESSION_NAME" "bash -lc '$START_CMD'"

log "✅ Bot iniciado na sessão: $SESSION_NAME"
log "📝 Logs: $PROJECT_DIR/$LOG_FILE"
log "👉 Para ver em tempo real: tmux attach -t $SESSION_NAME"
