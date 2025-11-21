import os
import time
<<<<<<< HEAD
import pandas as pd
=======
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
from dotenv import load_dotenv
from datetime import datetime

from exchange_client import get_client, get_ohlcv, place_order
from strategy import signal_from_ohlcv
from telegram_alert import alert_info, alert_trade, alert_error, alert_stoploss

# ============================================================
<<<<<<< HEAD
# 🤖 TRAIDBOLT — Bot de Trade Automático
# Autor: Glauco (Traidbolt)
# Última atualização: 09/11/2025
=======
# 🤖 TRAIDBOLT — Bot de Trade Automático (versão Termux)
# Compatível com pandas-lite ou sem pandas!
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
# ============================================================

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")
<<<<<<< HEAD
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))     # %
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0)) # %
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))      # quantidade
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 20))               # intervalo entre loops (s)
=======

STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0))
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 20))
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474

LOG_FILE = "logs/bot.log"
os.makedirs("logs", exist_ok=True)

client = get_client()
position = None
entry_price = None

# ============================================================
# FUNÇÃO DE LOG
# ============================================================

def log_event(msg):
<<<<<<< HEAD
    """Grava log local e exibe com timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {msg}"
    print(text)
=======
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {msg}"
    print(text)

>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# ============================================================
# LOOP PRINCIPAL
# ============================================================

def trade_loop():
    global position, entry_price
<<<<<<< HEAD
    alert_info("🤖 Traidbolt iniciado e monitorando o mercado...")
=======

    alert_info("🤖 Traidbolt iniciado (modo Termux otimizado).")
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
    log_event("Bot iniciado.")

    while True:
        try:
<<<<<<< HEAD
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
=======
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
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
                    position = None
                    entry_price = None

                # TAKE PROFIT
<<<<<<< HEAD
                elif change_pct >= TAKE_PROFIT_PCT:
                    msg = f"🏁 Take-Profit atingido ({change_pct:.2f}%) — realizando lucro."
                    alert_trade(SYMBOL, "take-profit", profit=change_pct)
                    log_event(msg)
                    place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
=======
                elif pct >= TAKE_PROFIT_PCT:
                    log_event(f"TAKE PROFIT atingido: {pct:.2f}%")
                    alert_trade(SYMBOL, "take-profit", pct)
                    place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
                    position = None
                    entry_price = None

            time.sleep(SLEEP_TIME)

        except Exception as e:
<<<<<<< HEAD
            error_text = f"⚠️ Erro no loop principal: {e}"
            log_event(error_text)
            alert_error(error_text)
            time.sleep(10)


if __name__ == "__main__":
    trade_loop()

=======
            msg = f"Erro no loop principal: {e}"
            log_event(msg)
            alert_error(msg)
            time.sleep(10)

if __name__ == "__main__":
    trade_loop()
>>>>>>> 29daf3e90110b5fd56ef535e4c562e2ad0725474
