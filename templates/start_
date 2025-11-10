import subprocess
import time
import requests
import json
import os

# Caminho do ngrok — ajuste se necessário
NGROK_PATH = os.path.expanduser("~/ngrok")

# Porta do Flask
PORT = 5000

# 1️⃣ Inicia o servidor Flask em segundo plano
subprocess.Popen(["python3", "app.py"])

# 2️⃣ Inicia o ngrok
print("🚀 Iniciando ngrok...")
ngrok_proc = subprocess.Popen([NGROK_PATH, "http", str(PORT)])
time.sleep(3)  # dá tempo de inicializar

# 3️⃣ Pega o link público via API local do ngrok
try:
    resp = requests.get("http://127.0.0.1:4040/api/tunnels")
    data = json.loads(resp.text)
    public_url = data["tunnels"][0]["public_url"]
    print(f"✅ Painel Flask online em: {public_url}")
except Exception as e:
    print("❌ Erro ao obter link do ngrok:", e)
