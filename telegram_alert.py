import requests
import os
from datetime import datetime

# ============================================================
# 🚀 Configurações básicas do Telegram
# ============================================================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_AQUI")


# ============================================================
# 🧩 Função base de envio de mensagem
# ============================================================

def send_telegram_message(msg: str):
    """Envia uma mensagem para o Telegram com tratamento de erros"""
    try:
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print("⚠️  TELEGRAM_TOKEN ou CHAT_ID não configurados.")
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"✅ Mensagem enviada: {msg}")
        else:
            print(f"⚠️ Erro ao enviar mensagem ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ Erro no envio ao Telegram: {e}")


# ============================================================
# 💬 Funções de alerta específicas
# ============================================================

def alert_info(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"ℹ️ <b>[INFO - {timestamp}]</b>\n{msg}"
    send_telegram_message(formatted)


def alert_trade(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"💰 <b>[TRADE - {timestamp}]</b>\n{msg}"
    send_telegram_message(formatted)


def alert_error(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"❌ <b>[ERRO - {timestamp}]</b>\n{msg}"
    send_telegram_message(formatted)


def alert_stoploss(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted = f"🛑 <b>[STOP-LOSS - {timestamp}]</b>\n{msg}"
    send_telegram_message(formatted)


# ============================================================
# 🔧 Teste rápido
# ============================================================

if __name__ == "__main__":
    print("🧠 Testando alertas do Telegram...")
    alert_info("Sistema Traidbolt iniciado.")
    alert_trade("Compra executada com sucesso no par SOL/USDC.")
    alert_error("Falha ao conectar à API Jupiter.")
    alert_stoploss("Stop-loss acionado em -20%.")

