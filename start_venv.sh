#!/bin/bash
# ==========================================
# 🚀 Script de inicialização do projeto Flask
# Autor: Glauco (Traidbolt)
# ==========================================

set -euo pipefail

VENV_DIR="${VENV_DIR:-venv}"
APP_FILE="${APP_FILE:-app.py}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"
DEBUG="${DEBUG:-1}"        # 1 = debug on, 0 = off
LOG_FILE="${LOG_FILE:-flask.log}"

log() { printf "[%s] %s
" "$(date +'%H:%M:%S')" "$*"; }
err() { printf "[ERRO %s] %s
" "$(date +'%H:%M:%S')" "$*" >&2; }

log "🔍 Verificando ambiente..."

# 1) checa se app existe
if [ ! -f "$APP_FILE" ]; then
  err "Arquivo $APP_FILE não encontrado no diretório atual."
  exit 1
fi

# 2) cria venv se não existir
if [ ! -d "$VENV_DIR" ]; then
  log "📦 Criando ambiente virtual em '$VENV_DIR'..."
  python3 -m venv "$VENV_DIR" || { err "Falha ao criar venv."; exit 1; }
fi

# 3) ativa venv
log "⚙️ Ativando ambiente virtual..."
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# 4) instala dependências
if [ -f "requirements.txt" ]; then
  log "📦 Instalando dependências de requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  log "📦 requirements.txt não encontrado. Instalando pacotes básicos..."
  pip install --upgrade pip
  pip install flask python-dotenv
fi

# 5) exporta variáveis Flask
export FLASK_APP="$APP_FILE"
export FLASK_RUN_HOST="$HOST"
export FLASK_RUN_PORT="$PORT"
[ "$DEBUG" = "1" ] && export FLASK_ENV=development || export FLASK_ENV=production

log "📝 Logs serão gravados em: $LOG_FILE"
log "🚀 Iniciando aplicação Flask em http://$HOST:$PORT (DEBUG=$DEBUG)..."
log "   Para parar: Ctrl+C"

# 6) inicia o app com log em arquivo + console
flask run 2>&1 | tee -a "$LOG_FILE"
