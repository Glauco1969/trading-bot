import subprocess
import time
import requests
import json
import os
import sys

# --- CONFIGURAÇÃO ---
NGROK_PATH = "/storage/emulated/0/ngrok"  # Caminho do ngrok
PORT = 5000                               # Porta do Flask
APP_PATH = "/storage/emulated/0/Download/trading-bot-main/trading-bot-main/main.py"  # Seu main.py

# --- Verifica se ngrok é executável ---
if not os.access(NGROK_PATH, os.X_OK):
    print(f"⚠️ ngrok não tem permissão de execução. Corrigindo...")
    os.chmod(NGROK_PATH, 0o755)

# --- Inicia Flask ---
print("🚀 Iniciando servidor Flask...")
flask_proc = subprocess.Popen(["python3", APP_PATH])
time.sleep(10)  # Espera o Flask subir

# --- Inicia ngrok ---
print("🌐 Iniciando ngrok...")
ngrok_proc = subprocess.Popen([NGROK_PATH, "http", str(PORT)])
time.sleep(5)

# --- Tenta obter link público do ngrok ---
public_url = None
for i in range(5):
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = json.loads(response.text)
        public_url = data["tunnels"][0]["public_url"]
        break
    except Exception:
        print("⏳ Tentando obter link público...")
        time.sleep(3)

if public_url:
    print(f"\n✅ Painel Flask online em: {public_url}\n")
else:
    print("❌ Não foi possível obter o link do ngrok. Verifique se está rodando corretamente.")

# --- Mantém script ativo ---
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Encerrando Flask e ngrok...")
    flask_proc.terminate()
    ngrok_proc.terminate()
    sys.exit(0)
