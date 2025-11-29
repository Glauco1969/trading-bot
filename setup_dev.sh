#!/data/data/com.termux/files/usr/bin/bash
# ==========================================
# 🚀 Setup completo do ambiente Dev no Android (Termux)
# Autor: Glauco (Traidbolt)
# ==========================================

set -euo pipefail

# --------- CONFIG BÁSICA (editável) ----------
DEV_DIR="${DEV_DIR:-$HOME/projetos}"
GIT_USER="${GIT_USER:-Glauco}"
GIT_EMAIL="${GIT_EMAIL:-glaferu604@gmail.com}"
CODE_PORT="${CODE_PORT:-8080}"
CODE_HOST="${CODE_HOST:-0.0.0.0}"
PY_PACKAGES="flask jupyter pandas numpy requests python-dotenv rich"
NODE_GLOBALS="yarn nodemon live-server code-server"
# ---------------------------------------------

log()  { printf "
[%s] %s
" "$(date +'%H:%M:%S')" "$*"; }
err()  { printf "
[ERRO %s] %s
" "$(date +'%H:%M:%S')" "$*" >&2; }

# ---- checa se está mesmo no Termux ----
if ! echo "$PREFIX" | grep -q "com.termux"; then
  err "Este script foi feito para Termux. PREFIX="$PREFIX""
  exit 1
fi

log "🔍 Atualizando pacotes..."
if ! pkg update -y && pkg upgrade -y; then
  err "Falha ao atualizar/atualizar pacotes. Verifique sua conexão."
  exit 1
fi

log "📦 Instalando pacotes essenciais..."
ESSENTIAL_PKGS="git python nodejs npm wget curl openssh clang make build-essential tmux htop nano vim tree"
if ! pkg install -y $ESSENTIAL_PKGS; then
  err "Erro instalando pacotes essenciais."
  exit 1
fi

log "🐍 Configurando Python e pip..."
if ! command -v pip >/dev/null 2>&1; then
  err "pip não encontrado. Tentando instalar python-pip..."
  pkg install -y python-pip || { err "Falha ao instalar pip."; exit 1; }
fi

python -m pip install --upgrade pip || err "Não foi possível atualizar o pip (segue com versão atual)."

log "🐍 Instalando dependências Python..."
for pkg in $PY_PACKAGES; do
  log "Instalando Python package: $pkg"
  python -m pip install "$pkg" || err "Falha ao instalar $pkg (pulando, você pode instalar depois)."
done

log "📦 Instalando dependências Node.js globais..."
for mod in $NODE_GLOBALS; do
  log "Instalando Node global: $mod"
  npm install -g "$mod" || err "Falha ao instalar $mod (pulando)."
done

# Tailwind como dependência local de projeto base
log "🎨 Preparando Tailwind CSS base..."
mkdir -p "$DEV_DIR/tailwind-base"
cd "$DEV_DIR/tailwind-base"
if [ ! -f package.json ]; then
  npm init -y >/dev/null 2>&1 || err "Não foi possível inicializar package.json para Tailwind (segue)."
fi
npm install -D tailwindcss || err "Falha ao instalar Tailwind CSS (você pode instalar manualmente depois)."

# ---- Git config (somente se ainda não estiver setado) ----
log "🔧 Configurando Git global..."
CURRENT_NAME=$(git config --global user.name || echo "")
CURRENT_EMAIL=$(git config --global user.email || echo "")

if [ -z "$CURRENT_NAME" ]; then
  git config --global user.name "$GIT_USER"
fi

if [ -z "$CURRENT_EMAIL" ]; then
  git config --global user.email "$GIT_EMAIL"
fi

log "Git configurado como:"
git config --global user.name
git config --global user.email

# ---- Pasta de trabalho ----
log "⚙️ Criando pasta de trabalho em: $DEV_DIR"
mkdir -p "$DEV_DIR"
cd "$DEV_DIR"

# ---- Script VSCode Web (code-server) ----
log "🧠 Criando script de inicialização do VSCode Web..."
cat << EOF > start_vscode.sh
#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
PORT="${1:-$CODE_PORT}"
HOST="$CODE_HOST"

echo "🚀 Iniciando Visual Studio Code Web (code-server) em $HOST:$PORT ..."
code-server --host "$HOST" --port "$PORT"
EOF

chmod +x start_vscode.sh

# ---- Script helper de ambiente rápido ----
log "🧰 Criando script helper de ambiente (env_info.sh)..."
cat << 'EOF' > env_info.sh
#!/data/data/com.termux/files/usr/bin/bash
echo "========= AMBIENTE TRAIDBOLT ========="
echo "Data     : $(date)"
echo "Python   : $(python --version 2>&1)"
echo "Node     : $(node --version 2>&1)"
echo "npm      : $(npm --version 2>&1)"
echo "tmux     : $(tmux -V 2>&1)"
echo "Git user : $(git config --global user.name 2>/dev/null)"
echo "Git email: $(git config --global user.email 2>/dev/null)"
echo "Projetos : $HOME/projetos"
echo "======================================"
EOF

chmod +x env_info.sh

log "✅ Instalação concluída com sucesso!"
echo
echo "👉 Informações rápidas do ambiente:"
./env_info.sh || true
echo
echo "👉 Para iniciar o VSCode Web:"
echo "-------------------------------------"
echo "cd "$DEV_DIR" && ./start_vscode.sh"
echo "-------------------------------------"
echo "🌐 Depois abra no navegador: http://127.0.0.1:$CODE_PORT (ou a porta que você escolher)"
echo
echo "Se algo der erro, copie a mensagem e manda aqui que dá para ajustar bem fino pro teu Android/Termux."
