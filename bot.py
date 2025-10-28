# bot.py
import time
import pandas as pd
from exchange_client import get_client, get_ohlcv, place_order
from strategy import signal_from_ohlcv
from telegram_alert import send_telegram_message
from dotenv import load_dotenv
import os

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))   # %
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0))  # %
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))  # quantidade de BTC

client = get_client()

position = None
entry_price = None

def trade_loop():
    global position, entry_price
    send_telegram_message("🤖 Bot iniciado e monitorando o mercado...")

    while True:
        try:
            df = get_ohlcv(client, SYMBOL, TIMEFRAME, 100)
            signal = signal_from_ohlcv(df)

            last_price = float(df['close'].iloc[-1])

            # 🟢 Sinal de COMPRA
            if signal == "buy" and position is None:
                send_telegram_message(f"📈 Sinal de COMPRA detectado para {SYMBOL} a {last_price:.2f} USDT")
                order = place_order(client, SYMBOL, 'buy', TRADE_AMOUNT)
                if order:
                    position = "long"
                    entry_price = last_price
                    send_telegram_message(f"✅ Ordem de compra executada. Preço de entrada: {entry_price:.2f} USDT")

            # 🔴 Sinal de VENDA
            elif signal == "sell" and position == "long":
                send_telegram_message(f"📉 Sinal de VENDA detectado para {SYMBOL} a {last_price:.2f} USDT")
                order = place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                if order:
                    position = None
                    entry_price = None
                    send_telegram_message(f"✅ Ordem de venda executada em {last_price:.2f} USDT")

            # 🎯 Stop-loss / Take-profit automáticos
            if position == "long" and entry_price:
                change_pct = ((last_price - entry_price) / entry_price) * 100

                if change_pct <= -STOP_LOSS_PCT:
                    send_telegram_message(f"❌ Stop-Loss atingido ({change_pct:.2f}%) — vendendo posição.")
                    place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                    position = None
                    entry_price = None

                elif change_pct >= TAKE_PROFIT_PCT:
                    send_telegram_message(f"🏁 Take-Profit atingido ({change_pct:.2f}%) — realizando lucro.")
                    place_order(client, SYMBOL, 'sell', TRADE_AMOUNT)
                    position = None
                    entry_price = None

            time.sleep(20)

        except Exception as e:
            print("Erro no loop principal:", e)
            send_telegram_message(f"⚠️ Erro no bot: {e}")
            time.sleep(10)


if __name__ == "__main__":
    trade_loop()



