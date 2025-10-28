#!/bin/bash
# ======================================
# 🛑 Stop script do Trading Bot
# ======================================

SESSION_NAME="trading-bot"

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "🧹 Encerrando sessão do bot..."
    tmux kill-session -t $SESSION_NAME
    echo "✅ Bot parado com sucesso."
else
    echo "⚠️ Nenhuma sessão ativa encontrada."
fi
chmod +x stop.sh
.stop.sh
