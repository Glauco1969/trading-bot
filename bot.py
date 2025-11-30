import os
import time
from dotenv import load_dotenv
from datetime import datetime

from exchange_client import get_client, get_ohlcv, place_order
from strategy import signal_from_ohlcv
from telegram_alert import alert_info, alert_trade, alert_error, alert_stoploss

# ============================================================
# 🤖 TRAIDBOLT — Bot de Trade Automático (Termux)
# ============================================================

load_dotenv()

SYMBOL = os.getenv("TRADE_SYMBOL", "BTC/USDT")
TIMEFRAME = os.getenv("TIMEFRAME", "1m")

STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", 0.5))      # %
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", 1.0))  # %
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 0.001))      # quantidade
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 20))               # intervalo entre ciclos (s)

LOG_FILE = "logs/bot.log"
os.makedirs("logs", exist_ok=True)

client = get_client()
position = None        # "long" ou None
entry_price = None     # preço médio da entrada atual


# ============================================================
# FUNÇÃO DE LOG
# ============================================================

def log_event(msg: str) -> None:
    """Grava log local e exibe com timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {msg}"
    print(text)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "
")


# ============================================================
# STATUS PARA O PAINEL
# ============================================================

def get_status() -> dict:
    """Retorna status atual para o painel Flask."""
    return {
        "symbol": SYMBOL,
        "timeframe": TIMEFRAME,
        "position": position,
        "entry_price": entry_price,
    }


# ============================================================
# UM CICLO DE TRADE (SEM while True)
# ============================================================

def trade_loop():
    """
    Executa APENAS UM ciclo de leitura de mercado + decisão.
    O loop contínuo fica no bot_controller (main.py).
    """
    global position, entry_price

    try:
        # Busca OHLCV e gera sinal
        df = get_ohlcv(client, SYMBOL, TIMEFRAME, 100)
        signal = signal_from_ohlcv(df)
        last_price = float(df["close"].iloc[-1])

        # ----------------------------------------------------
        # 🟢 COMPRA
        # ----------------------------------------------------
        if signal == "buy" and position is None:
            log_event(f"Sinal de COMPRA para {SYMBOL} a {last_price:.2f} USDT")
            alert_info(
                f"📈 *Sinal de COMPRA* em `{SYMBOL}` a `{last_price:.2f}` USDT"
            )

            order = place_order(client, SYMBOL, "buy", TRADE_AMOUNT)
            if order:
                position = "long"
                entry_price = last_price
                alert_trade(SYMBOL, "compra", TRADE_AMOUNT)
                log_event(
                    f"Ordem de compra executada. Entrada: {entry_price:.2f} USDT"
                )

        # ----------------------------------------------------
        # 🔴 VENDA POR SINAL
        # ----------------------------------------------------
        elif signal == "sell" and position == "long":
            log_event(f"Sinal de VENDA para {SYMBOL} a {last_price:.2f} USDT")
            alert_info(
                f"📉 *Sinal de VENDA* em `{SYMBOL}` a `{last_price:.2f}` USDT"
            )

            order = place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
            if order:
                position = None
                entry_price = None
                alert_trade(SYMBOL, "venda", TRADE_AMOUNT)
                log_event(f"Ordem de venda executada a {last_price:.2f} USDT")

        # ----------------------------------------------------
        # 🎯 STOP LOSS / TAKE PROFIT
        # ----------------------------------------------------
        if position == "long" and entry_price is not None:
            change_pct = ((last_price - entry_price) / entry_price) * 100

            # STOP LOSS
            if change_pct <= -STOP_LOSS_PCT:
                msg = (
                    f"❌ Stop-Loss atingido ({change_pct:.2f}%) — vendendo posição."
                )
                alert_stoploss(SYMBOL, last_price)
                log_event(msg)
                place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
                position = None
                entry_price = None

            # TAKE PROFIT
            elif change_pct >= TAKE_PROFIT_PCT:
                msg = (
                    f"🏁 Take-Profit atingido ({change_pct:.2f}%) — realizando lucro."
                )
                alert_trade(SYMBOL, "take-profit", change_pct)
                log_event(msg)
                place_order(client, SYMBOL, "sell", TRADE_AMOUNT)
                position = None
                entry_price = None

        # Pequena pausa entre ciclos (controlada pelo bot_controller)
        time.sleep(SLEEP_TIME)

    except Exception as e:
        error_text = f"⚠️ Erro no loop principal: {e}"
        log_event(error_text)
        alert_error(error_text)
        time.sleep(10)


# ============================================================
# EXECUÇÃO DIRETA (opcional)
# ============================================================

if __name__ == "__main__":
    log_event("Bot iniciado em modo standalone.")
    alert_info("🤖 Traidbolt iniciado em modo standalone.")
    while True:
        trade_loop()
