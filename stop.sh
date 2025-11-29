#!/bin/bash
# ======================================
# 🛑 Stop script do Trading Bot
# ======================================

SESSION_NAME="${1:-trading-bot}"   # permite passar nome por argumento
FORCE_KILL="${FORCE_KILL:-0}"      # FORCE_KILL=1 para matar à força

# ---- checa tmux instalado ----
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

# ---- procura sessões que combinam com o nome ----
MATCHED=$(echo "$SESSIONS" | grep -E "^${SESSION_NAME}(-[0-9]+)?$" || true)

if [ -z "$MATCHED" ]; then
  echo "⚠️ Nenhuma sessão encontrada com o nome: ${SESSION_NAME}"
  echo "ℹ️ Sessões atuais:"
  echo "$SESSIONS"
  exit 0
fi

echo "🧹 Encerrando sessões:"
echo "$MATCHED"

# ---- encerra cada sessão encontrada ----
while IFS= read -r S; do
  if [ -n "$S" ]; then
    if tmux has-session -t "$S" 2>/dev/null; then
      tmux kill-session -t "$S"
      echo "✅ Sessão '${S}' encerrada."
    fi
  fi
done <<< "$MATCHED"

# ---- opção de kill extra se algo ficar preso ----
if [ "$FORCE_KILL" = "1" ]; then
  echo "🧨 FORCE_KILL ativado: tentando matar processos python do bot..."
  pkill -f "tradingbot" 2>/dev/null || true
fi

echo "🏁 Finalizado."
exit 0
