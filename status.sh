#!/bin/bash
# ======================================
# 📊 Status script do Trading Bot
# ======================================

SESSION_NAME="${1:-trading-bot}"   # permite passar nome por argumento

# ---- checa se tmux está instalado ----
if ! command -v tmux >/dev/null 2>&1; then
  echo "❌ tmux não está instalado ou não está no PATH."
  exit 1
fi

# ---- lista sessões existentes ----
SESSIONS=$(tmux list-sessions -F '#S' 2>/dev/null || true)

if [ -z "$SESSIONS" ]; then
  echo "⚠️ Nenhuma sessão tmux ativa encontrada."
  exit 0
fi

echo "ℹ️ Sessões tmux ativas:"
echo "$SESSIONS"
echo

# ---- procura sessão principal do bot ----
MATCHED=$(echo "$SESSIONS" | grep -E "^${SESSION_NAME}(-[0-9]+)?$" || true)

if [ -z "$MATCHED" ]; then
  echo "❌ Nenhuma sessão encontrada com o nome base: ${SESSION_NAME}"
  exit 0
fi

echo "✅ Sessões do bot encontradas:"
echo "$MATCHED"
echo

# ---- mostra status resumido de cada sessão ----
while IFS= read -r S; do
  [ -z "$S" ] && continue
  echo "----- sessão: $S -----"
  # última linha do pane 0 (se existir)
  tmux capture-pane -pt "$S:0" -S -5 2>/dev/null | tail -n 5 || \
    echo "(não foi possível capturar logs desta sessão)"
  echo
done <<< "$MATCHED"

# ---- checa processos Python relacionados ao bot ----
if pgrep -af "tradingbot" >/dev/null 2>&1; then
  echo "🧠 Processos Python relacionados ao bot rodando:"
  pgrep -af "tradingbot"
else
  echo "ℹ️ Nenhum processo Python contendo 'tradingbot' encontrado."
fi

echo
echo "👉 Para anexar na sessão principal:"
echo "   tmux attach -t ${SESSION_NAME}"
