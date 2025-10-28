#!/bin/bash
# ======================================
# 📊 Status script do Trading Bot
# ======================================

SESSION_NAME="trading-bot"

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ O bot está rodando na sessão: $SESSION_NAME"
    echo "👉 Para ver os logs em tempo real:"
    echo "   tmux attach -t $SESSION_NAME"
else
    echo "❌ O bot não está em execução."
fi

