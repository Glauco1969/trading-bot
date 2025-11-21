# exchange_client.py
import ccxt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
USE_TESTNET = os.getenv("USE_TESTNET", "true").lower() == "true"

def get_client():
    """Cria conexão com Binance (Spot Testnet ou produção)."""
    if USE_TESTNET:
        print("🔧 Conectando à Binance Spot TESTNET...")
        exchange = ccxt.binance({
            "apiKey": API_KEY,
            "secret": API_SECRET,
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        })
        exchange.set_sandbox_mode(True)
    else:
        print("⚙️ Conectando à Binance SPOT (produção)...")
        exchange = ccxt.binance({
            "apiKey": API_KEY,
            "secret": API_SECRET,
            "enableRateLimit": True,
        })
    return exchange


def get_ohlcv(client, symbol="BTC/USDT", timeframe="1m", limit=100):
    """Obtém candles OHLCV e retorna como DataFrame."""
    bars = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def place_order(client, symbol, side, amount):
    """
    Executa uma ordem de mercado (simulada na testnet).
    """
    try:
        order = client.create_market_order(symbol, side, amount)
        print(f"✅ Ordem {side.upper()} executada: {amount} {symbol}")
        return order
    except Exception as e:
        print(f"❌ Erro ao enviar ordem {side.upper()}: {e}")
        return None

