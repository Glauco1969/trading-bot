import pandas as pd
import numpy as np

def sma(series, period):
    return series.rolling(period).mean()

def atr(df, period=14):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(period).mean()

def signal_from_ohlcv(
    df,
    entry_price=None,
    stop_mult=2.5,
    take_mult=4.0
):
    """
    df: DataFrame com ['timestamp','open','high','low','close','volume']
    entry_price: último preço de entrada da posição atual (None se estiver flat)
    stop_mult: múltiplo do ATR para stop loss
    take_mult: múltiplo do ATR para take profit

    Retorna: 'buy', 'sell' ou None
    """

    if len(df) < 50:
        return None

    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    sma_fast = sma(close, 7)
    sma_slow = sma(close, 25)
    vol_sma = sma(volume, 20)
    atr_val = atr(df, 14)

    prev_fast = sma_fast.iloc[-2]
    prev_slow = sma_slow.iloc[-2]
    last_fast = sma_fast.iloc[-1]
    last_slow = sma_slow.iloc[-1]

    last_close = close.iloc[-1]
    last_atr = atr_val.iloc[-1]
    last_vol = volume.iloc[-1]
    last_vol_sma = vol_sma.iloc[-1]

    # 1) Gestão da posição atual (se já estiver comprado)
    if entry_price is not None and last_atr is not None and not np.isnan(last_atr):
        stop_price = entry_price - stop_mult * last_atr
        take_price = entry_price + take_mult * last_atr

        if last_close <= stop_price:
            return "sell"   # stop loss
        if last_close >= take_price:
            return "sell"   # take profit

    # 2) Gatilho de cruzamento de médias
    golden_cross = prev_fast <= prev_slow and last_fast > last_slow
    death_cross = prev_fast >= prev_slow and last_fast < last_slow

    # 3) Filtros adicionais para BUY
    up_trend = last_close > last_slow              # preço acima da SMA lenta
    vol_ok = last_vol > last_vol_sma * 1.2         # volume atual acima da média
    atr_ok = last_atr is not None and last_atr > 0

    if golden_cross and up_trend and vol_ok and atr_ok and entry_price is None:
        return "buy"

    # 4) SELL por mudança de tendência
    if death_cross and entry_price is not None:
        return "sell"

    return None
