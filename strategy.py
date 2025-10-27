# strategy.py
import pandas as pd
import numpy as np

def sma(series, period):
    return series.rolling(period).mean()

def signal_from_ohlcv(df):
    """
    df: DataFrame com columns: ['timestamp','open','high','low','close','volume']
    Retorna: 'buy', 'sell' ou None
    """
    close = df['close'].astype(float)
    sma_fast = sma(close, 7)
    sma_slow = sma(close, 25)
    if len(close) < 30:
        return None

    prev_fast = sma_fast.iloc[-2]
    prev_slow = sma_slow.iloc[-2]
    last_fast = sma_fast.iloc[-1]
    last_slow = sma_slow.iloc[-1]

    if prev_fast <= prev_slow and last_fast > last_slow:
        return "buy"
    if prev_fast >= prev_slow and last_fast < last_slow:
        return "sell"
    return None
