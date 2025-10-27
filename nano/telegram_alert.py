# telegram_alert.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """Envia uma mensagem simples para o Telegram."""
    if not TOKEN or not CHAT_ID:
        print("⚠️ Telegram não configurado corretamente (.env faltando)")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload, timeout=5)
        if not r.ok:
            print("Erro ao enviar mensagem Telegram:", r.text)
    except Exception as e:
        print("Erro na conexão com Telegram:", e)
