import subprocess
import time
import requests
import json
import os
import sys
from dotenv import load_dotenv

# === Carrega variáveis do .env ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# === CONFIGURAÇÃO ===
NGROK_PATH = "C:\\Users\\84857528487\\Desktop\\traid-bot\\trading-bot\\ngrok.exe"
PORT = 5000
APP_PATH = "C:\\Users\\84857528487\\Desktop\\traid-bot\\trading-bot\\app.py"

# === Função para enviar mensagem no Telegram ===
def send_telegram_message(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ BOT_TOKEN ou CHAT_ID não configurados no .env")
        return
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
        print(f"📩 Mensagem enviada: {msg}")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")

# === Inicia o Flask ===
print("🚀 Iniciando servidor Flask...")
flask_proc = subprocess.Popen(["python", APP_PATH])
time.sleep(5)

# === Inicia o ngrok ===
print("🌐 Iniciando ngrok...")
ngrok_proc = subprocess.Popen(
    [NGROK_PATH, "http", str(PORT)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(5)

# === Obtém o link público ===
public_url = None
for _ in range(10):
    try:
        res = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = res.json()
        public_url = data["tunnels"][0]["public_url"]
        break
    except Exception:
        print("⏳ Tentando obter link público...")
        time.sleep(2)

if public_url:
    print(f"\n✅ Painel online em: {public_url}\n")
    send_telegram_message(f"🚀 Painel Flask online!\n🌐 Link: {public_url}")
else:
    print("❌ Não foi possível obter o link público do ngrok.")
    send_telegram_message("⚠️ Erro ao gerar o link público do ngrok.")

# === Mantém o script ativo ===
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Encerrando Flask e ngrok...")
    flask_proc.terminate()
    ngrok_proc.terminate()
    sys.exit(0)
