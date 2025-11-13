import os
import time
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

from exchange_client import get_client, get_ohlcv, place_order
from strategy import signal_from_ohlcv
from telegram_alert import alert_info, alert_trade, alert_error, alert_stoploss

# ============================================================
# 🤖 TRAIDBOLT — Bot de Trade Automático
# Autor: Glauco (Traidbolt)
# Última atualização: 09/11/2025
# ============================================================

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))     # %
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0)) # %
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))      # quantidade
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 20))               # intervalo entre loops (s)

LOG_FILE = "logs/bot.log"
os.makedirs("logs", exist_ok=True)

client = get_client()
position = None
entry_price = None

# ============================================================
# FUNÇÃO DE LOG
# ============================================================

def log_event(msg):
    """Grava log local e exibe com timestamp"""
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
    alert_info("🤖 Traidbolt iniciado e monitorando o mercado...")
    log_event("Bot iniciado.")

    while True:
        try:
            df = get_ohlcv(client, SYMBOL, TIMEFRAME, 100)
            signal = signal_from_ohlcv(df)
            last_price = float(df['close'].iloc[-1])

            # 🟢 Sinal de COMPRA
            if signal == "buy" and position is None:
                log_event(f"Sinal de COMPRA detectado para {SYMBOL} a {last_price:.2f} USDT")
                alert_info(f"📈 *Sinal de COMPRA* detectado para `{SYMBOL}` a `{last_price:.2f}` USDT")

                order = place_order(client, SYMBOL, 'buy', TRADE_AMOUNT)
                if order:
                    position = "long"
                    entry_price = last_price
                    alert_trade(SYMBOL, "compra", TRADE_AMOUNT)
                    log_event(f"Ordem de compra executada. Preço de entrada: {entry_price:.2f} USDT")

            # 🔴 Sinal de VENDA
            elif signal == "sell" and position == "long":
                log_event(f"Sinal de VENDA detectado para {SYMBOL} a {last_price:.2f} USDT")
                alert_info(f"📉 *Sinal de VENDA* detectado para `{SYMBOL}` a `{last_price:.2f}` USDT")

                order = place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                if order:
                    position = None
                    alert_trade(SYMBOL, "venda", TRADE_AMOUNT)
                    log_event(f"Ordem de venda executada em {last_price:.2f} USDT")

            # 🎯 Stop-loss / Take-profit automáticos
            if position == "long" and entry_price:
                change_pct = ((last_price - entry_price) / entry_price) * 100

                # STOP LOSS
                if change_pct <= -STOP_LOSS_PCT:
                    msg = f"❌ Stop-Loss atingido ({change_pct:.2f}%) — vendendo posição."
                    alert_stoploss(SYMBOL, last_price)
                    log_event(msg)
                    place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                    position = None
                    entry_price = None

                # TAKE PROFIT
                elif change_pct >= TAKE_PROFIT_PCT:
                    msg = f"🏁 Take-Profit atingido ({change_pct:.2f}%) — realizando lucro."
                    alert_trade(SYMBOL, "take-profit", profit=change_pct)
                    log_event(msg)
                    place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                    position = None
                    entry_price = None

            time.sleep(SLEEP_TIME)

        except Exception as e:
            error_text = f"⚠️ Erro no loop principal: {e}"
            log_event(error_text)
            alert_error(error_text)
            time.sleep(10)


if __name__ == "__main__":
    trade_loop()

