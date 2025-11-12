import subprocess
import time
import requests
import json
import os
import sys

# --- CONFIGURAÇÃO (versão para Windows) ---
NGROK_PATH = r"C:\Users\84857528487\Desktop\traid-bot\trading-bot\ngrok.exe"  # Caminho do ngrok
PORT = 5000
APP_PATH = r"C:\Users\84857528487\Desktop\traid-bot\trading-bot\app.py"       # Caminho do Flask app

# --- Inicia Flask ---
print("🚀 Iniciando servidor Flask...")
flask_proc = subprocess.Popen(["python", APP_PATH])
time.sleep(10)  # Espera o Flask iniciar

# --- Inicia ngrok ---
print("🌐 Iniciando ngrok...")
ngrok_proc = subprocess.Popen([NGROK_PATH, "http", str(PORT)])
time.sleep(5)

# --- Obtém o link público ---
public_url = None
for i in range(5):
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = json.loads(response.text)
        public_url = data["tunnels"][0]["public_url"]
        break
    except Exception as e:
        print("⏳ Tentando obter link público...")
        time.sleep(3)

if public_url:
    print(f"\n✅ Painel Flask online em: {public_url}\n")
else:
    print("❌ Não foi possível obter o link do ngrok. Verifique se está rodando corretamente.")

# --- Mantém o script ativo ---
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Encerrando Flask e ngrok...")
    flask_proc.terminate()
    ngrok_proc.terminate()
    sys.exit(0)
