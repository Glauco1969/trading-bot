from flask import Flask, render_template, jsonify
import random
import datetime

app = Flask(__name__)

# --- Página inicial ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Endpoint de status ---
@app.route("/status")
def status():
    # Aqui simulamos dados — depois dá pra integrar com o bot real
    saldo = round(random.uniform(1.0, 2.5), 3)
    lucro = round(random.uniform(5.0, 35.0), 2)
    return jsonify({
        "online": True,
        "saldo": saldo,
        "lucro": lucro,
        "ultima_atualizacao": datetime.datetime.now().strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
