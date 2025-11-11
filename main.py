import json
import os
import sys
import os
import platform
import subprocess
from flask import Flask, render_template

# --- Detectar o sistema operacional ---
SO = platform.system().lower()

if 'windows' in SO:
    NGROK_PATH = os.path.join(os.getcwd(), "ngrok.exe")
else:
    NGROK_PATH = "/storage/emulated/0/ngrok"

# --- Verificar se o ngrok existe ---
if not os.path.exists(NGROK_PATH):
    print(f"❌ Ngrok não encontrado em: {NGROK_PATH}")
    print("👉 No Windows, coloque o arquivo ngrok.exe dentro da pasta do projeto.")
    print("👉 No Android (Termux), baixe e coloque /storage/emulated/0/ngrok")
    exit()

# --- Tornar o ngrok executável (só Android) ---
if 'windows' not in SO:
    os.chmod(NGROK_PATH, 0o755)

# --- Iniciar o Flask ---
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')

# --- Iniciar ngrok ---
def start_ngrok():
    print("🚀 Iniciando ngrok...")
    if 'windows' in SO:
        subprocess.Popen([NGROK_PATH, "http", "5000"])
    else:
        subprocess.Popen([NGROK_PATH, "http", "5000", "--log=stdout"])

if __name__ == '__main__':
    start_ngrok()
    app.run(host='0.0.0.0', port=5000, debug=True)


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
