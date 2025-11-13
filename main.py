from flask import Flask, render_template, jsonify
import threading
import time
import os
from bot import trade_loop

app = Flask(__name__)

bot_thread = None
bot_running = False


# ============================================================
# --- ROTAS DO PAINEL WEB ---
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
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-10:]
            log_content = "".join(lines)
    return jsonify({
        "status": "Rodando" if bot_running else "Parado",
        "log": log_content
    })


@app.route("/start")
def start_bot():
    global bot_thread, bot_running
    if not bot_running:
        bot_thread = threading.Thread(target=trade_loop, daemon=True)
        bot_thread.start()
        bot_running = True
        return jsonify({"message": "🤖 Bot iniciado!"})
    else:
        return jsonify({"message": "⚠️ Bot já está rodando."})


@app.route("/stop")
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"message": "🛑 Bot parado manualmente."})


# ============================================================
# --- INICIAR SERVIDOR ---
# ============================================================

if __name__ == "__main__":
    print("🚀 Painel Traidbolt iniciado em: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

