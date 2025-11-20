from flask import Flask, render_template, jsonify
import threading
import time
import os
from bot import trade_loop

app = Flask(__name__)

bot_thread = None
bot_running = False

# ============================================================
# --- CONTROLADOR DO BOT ---
# ============================================================

def bot_controller():
    """Garante que o trade_loop rode em ciclos e pare quando bot_running = False."""
    global bot_running

    print("🤖 Bot iniciado...")

    while bot_running:
        try:
            trade_loop()  # executa UM ciclo, NÃO pode ter while True dentro!
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Erro no bot: {e}")
            time.sleep(2)

    print("🛑 Bot finalizado.")


# ============================================================
# --- ROTAS WEB ---
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/painel")
def painel():
    return render_template("painel.html")

@app.route("/status")
def status():
    log_path = "logs/bot.log"
    log_content = ""

    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()[-15:]
                log_content = "".join(lines)
        except:
            log_content = "Erro ao ler log."

    return jsonify({
        "status": "Rodando" if bot_running else "Parado",
        "log": log_content
    })


@app.route("/start")
def start_bot():
    global bot_thread, bot_running

    if bot_running:
        return jsonify({"message": "⚠️ O bot já está rodando!"})

    bot_running = True
    bot_thread = threading.Thread(target=bot_controller, daemon=True)
    bot_thread.start()

    return jsonify({"message": "🚀 Bot iniciado!"})


@app.route("/stop")
def stop_bot():
    global bot_running

    if not bot_running:
        return jsonify({"message": "⚠️ O bot já está parado."})

    bot_running = False
    return jsonify({"message": "🛑 Bot será desligado em alguns segundos."})


# ============================================================
# --- INÍCIO DO SERVIDOR ---
# ============================================================

if __name__ == "__main__":
    print("🌐 Painel Traidbolt rodando em http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
