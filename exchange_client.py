# exchange_client.py
import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_NAME = os.getenv("EXCHANGE", "binance")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TESTNET = os.getenv("TESTNET", "true").lower() in ("true","1","yes")

def create_exchange():
    params = {}
    ex_class = getattr(ccxt, EXCHANGE_NAME)
    ex = ex_class({
        "apiKey": API_KEY,
        "secret": API_SECRET,
        "enableRateLimit": True,
        # opcional: 'options': {...}
    })
    # Binance testnet adjustment example (aplica-se somente a binance/futures libs)
    if EXCHANGE_NAME == "binance" and TESTNET:
        ex.set_sandbox_mode(True)  # CCXT suporta sandbox para algumas exchanges.
    return ex

git init
git add .
git commit -m "Versão funcional do robô Binance Testnet"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/trading-bot.git
git push -u origin main

tmux attach -t trading-bot

