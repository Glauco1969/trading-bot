import os
import requests
import threading
from datetime import datetime
from dotenv import load_dotenv

# ============================================================

# 📢 Telegram Alert System — Traidbolt

# Autor: Glauco (Traidbolt)

# Última atualização: 06/11/2025

# ============================================================

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOG_FILE = "logs/telegram_fallback.log"

# ===================== Função base ==========================

def _send_message(message, parse_mode="Markdown"):
"""Envia uma mensagem para o Telegram com tratamento de erros"""
if not TOKEN or not CHAT_ID:
_log_local(f"⚠️ Telegram não configurado. Mensagem: {message}")
return

```
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": parse_mode}

try:
    resp = requests.post(url, json=payload, timeout=10)
    if resp.status_code != 200:
        _log_local(f"❌ Erro Telegram {resp.status_code}: {resp.text}")
except Exception as e:
    _log_local(f"🚨 Falha ao enviar alerta: {e} | Conteúdo: {message}")
```

def _async_send(message):
"""Envia de forma assíncrona (não trava o bot)"""
thread = threading.Thread(target=_send_message, args=(message,))
thread.daemon = True
thread.start()

def _log_local(msg):
"""Salva fallback de mensagens não enviadas"""
os.makedirs("logs", exist_ok=True)
with open(LOG_FILE, "a", encoding="utf-8") as f:
f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

# ===================== Tipos de Alerta ======================

def alert_info(text):
_async_send(f"ℹ️ *INFO:*\n{text}")

def alert_error(text):
_async_send(f"❌ *ERRO:*\n{text}")

def alert_trade(symbol, action, amount=None, profit=None):
msg = f"💹 *TRADE EXECUTADO*\n"
msg += f"🪙 Par: `{symbol}`\n"
msg += f"⚙️ Ação: *{action.upper()}*\n"
if amount:
msg += f"📦 Quantidade: `{amount}`\n"
if profit is not None:
emoji = '🟢' if profit >= 0 else '🔴'
msg += f"{emoji} Lucro: `{profit:.2f}%`\n"
_async_send(msg)

def alert_swap(from_token, to_token, amount):
msg = (
f"🔄 *SWAP REALIZADO*\n"
f"💰 `{amount}` {from_token} → {to_token}\n"
)
_async_send(msg)

def alert_stoploss(symbol, price):
_async_send(f"🛑 *STOP-LOSS ATIVADO*\n🪙 Par: `{symbol}`\n💥 Preço: `{price}`")

def alert_reinvest(symbol, amount):
_async_send(f"♻️ *REINVESTIMENTO*\n🪙 Par: `{symbol}`\n💎 Valor reinvestido: `{amount}`")

# ===================== Teste direto =========================

if **name** == "**main**":
alert_info("Sistema de alertas do Traidbolt iniciado com sucesso ✅")
alert_trade("SOL/USDC", "compra", amount=0.5, profit=2.45)
alert_stoploss("SOL/USDC", 165.23)
alert_error("Erro de conexão com a API Jupiter.")
alert_reinvest("SOL/USDC", 0.35)
