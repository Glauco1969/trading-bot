import os
import time
from dotenv import load_dotenv
from datetime import datetime

from exchange_client import get_client, get_ohlcv, place_order
from strategy import signal_from_ohlcv
from telegram_alert import alert_info, alert_trade, alert_error, alert_stoploss

# ============================================================
# 🤖 TRAIDBOLT — Bot de Trade Automático (versão Termux)
# Compatível com pandas-lite ou sem pandas!
# ============================================================

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")

STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0))
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 20))

LOG_FILE = "logs/bot.log"
os.makedirs("logs", exist_ok=True)

client = get_client()
position = None
entry_price = None

# ============================================================
# FUNÇÃO DE LOG
# ============================================================

def log_event(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {msg}"
    print(text)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# ============================================================
# LOOP PRINCIPAL
# ============================================================

def trade_loop():
    global position, entry_price

    alert_info("🤖 Traidbolt iniciado (modo Termux otimizado).")
    log_event("Bot iniciado.")

    while True:
        try:
            # get_ohlcv já retorna lista -> convertendo manual sem pandas
            raw = get_ohlcv(client, SYMBOL, TIMEFRAME, 100)

            # Último candle (time, open, high, low, close, volume)
            last = raw[-1]
            last_close = float(last[4])

            # Gerar sinal da sua estratégia
            signal = signal_from_ohlcv(raw)

            # --------------------------------------------------------
            # 🟢 Sinal de compra
            # --------------------------------------------------------
            if signal == "buy" and position is None:
                log_event(f"Sinal BUY para {SYMBOL} a {last_close:.2f}")
                alert_info(f"📈 Compra detectada em `{SYMBOL}` ({last_close:.2f})")

                order = place_order(client, SYMBOL, "buy", TRADE_AMOUNT)
                if order:
                    position = "long"
                    entry_price = last_close
                    alert_trade(SYMBOL, "compra", TRADE_AMOUNT)
                    log_event(f"Compra executada a {entry_price:.2f}")

            # --------------------------------------------------------
            # 🔴 Sinal de venda
            # --------------------------------------------------------
            elif signal == "sell" and position == "long":
                log_event(f"Sinal SELL para {SYMBOL} a {last_close:.2f}")
                alert_info(f"📉 Venda detectada em `{SYMBOL}` ({last_close:.2f})")

                order = place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
                if order:
                    position = None
                    alert_trade(SYMBOL, "venda", TRADE_AMOUNT)
                    log_event(f"Venda executada a {last_close:.2f}")

            # --------------------------------------------------------
            # STOP LOSS / TAKE PROFIT
            # --------------------------------------------------------
            if position == "long" and entry_price is not None:
                pct = ((last_close - entry_price) / entry_price) * 100

                # STOP LOSS
                if pct <= -STOP_LOSS_PCT:
                    log_event(f"STOP LOSS acionado: {pct:.2f}%")
                    alert_stoploss(SYMBOL, last_close)
                    place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
                    position = None
                    entry_price = None

                # TAKE PROFIT
                elif pct >= TAKE_PROFIT_PCT:
                    log_event(f"TAKE PROFIT atingido: {pct:.2f}%")
                    alert_trade(SYMBOL, "take-profit", pct)
                    place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
                    position = None
                    entry_price = None

            time.sleep(SLEEP_TIME)

        except Exception as e:
            msg = f"Erro no loop principal: {e}"
            log_event(msg)
            alert_error(msg)
            time.sleep(10)

if __name__ == "__main__":
    trade_loop()
