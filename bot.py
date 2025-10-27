# bot.py
import time
import os
import logging
from dotenv import load_dotenv
import pandas as pd

from exchange_client import create_exchange
from strategy import signal_from_ohlcv
from telegram_alert import send_telegram_message


load_dotenv()

LOGFILE = os.path.join("logs", "bot.log")
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()

SYMBOL = os.getenv("SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")
ORDER_SIZE_USD = float(os.getenv("ORDER_SIZE_USD", "10"))

def fetch_ohlcv(exchange, symbol, timeframe, limit=100):
    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["timestamp","open","high","low","close","volume"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def place_market_order(exchange, symbol, side, usd_amount):
    # converter usd -> amount de base asset com ticker price
    ticker = exchange.fetch_ticker(symbol)
    price = float(ticker['last'])
    base_amount = float(usd_amount) / price
    # ajustar precision
    market = exchange.markets[symbol]
    precision = market.get('precision', {}).get('amount', 8)
    base_amount = exchange.amount_to_precision(symbol, base_amount)
    logger.info(f"Placing {side} market order {symbol} qty={base_amount} (≈${usd_amount})")
    try:
        order = exchange.create_market_order(symbol, side, float(base_amount))
        logger.info(f"Order executed: {order}")
        return order
    except Exception as e:
        logger.exception("Order failed")
        return None

def main_loop():
    ex = create_exchange()
    logger.info("Starting bot for %s" % SYMBOL)
    position = None  # 'long' ou None

    while True:
        try:
            df = fetch_ohlcv(ex, SYMBOL, TIMEFRAME, limit=200)
            sig = signal_from_ohlcv(df)
            logger.info(f"Signal: {sig}")

            if sig == "buy" and position != "long":
                order = place_market_order(ex, SYMBOL, "buy", ORDER_SIZE_USD)
                if order:
                    position = "long"
            elif sig == "sell" and position == "long":
                order = place_market_order(ex, SYMBOL, "sell", ORDER_SIZE_USD)
                if order:
                    position = None
        except Exception as e:
            logger.exception("Erro no loop principal")
        time.sleep(30)  # espera entre iterações (ajuste conforme timeframe)
    
if __name__ == "__main__":
    main_loop()

# estando no diretório do projeto e com venv ativado:
tmux new -ds trading-bot "source ~/trading-bot-venv/bin/activate; python3 $(pwd)/bot.py |& tee logs/bot.log"

# clonar (se quiser)
git clone <seu-repo> trading-bot
cd trading-bot

# criar virtualenv
python3 -m venv ~/trading-bot-venv
source ~/trading-bot-venv/bin/activate
pip install ccxt python-dotenv pandas numpy requests

# preparar .env (editar)
nano .env

# iniciar bot em tmux (detached) e registrar logs
tmux new -ds trading-bot "source ~/trading-bot-venv/bin/activate; python3 $(pwd)/bot.py |& tee logs/bot.log"

# ver sessões
tmux ls

# anexar para checar
tmux attach -t trading-bot
# ou sair (detach) com Ctrl+b d



