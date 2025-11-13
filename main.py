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

/* ---- Fundo animado ---- */
@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.animate-gradientMove {
  background-size: 200% 200%;
  animation: gradientMove 8s ease infinite;
}

/* ---- Fade suave ---- */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 1s ease forwards;
}
.animate-fadeInDelay {
  animation: fadeIn 1.5s ease forwards;
}

/* ---- Rotação lenta ---- */
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow {
  animation: spin-slow 20s linear infinite;
}

/* ---- Botão brilhante ---- */
.btn-glow {
  background: linear-gradient(90deg, #6d28d9, #2563eb);
  color: #fff;
  transition: 0.3s;
  box-shadow: 0 0 20px rgba(109, 40, 217, 0.4);
}
.btn-glow:hover {
  box-shadow: 0 0 35px rgba(37, 99, 235, 0.6);
  transform: scale(1.05);
}


if __name__ == "__main__":
    print("🚀 Painel Traidbolt iniciado em: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

