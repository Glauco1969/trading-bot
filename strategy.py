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

upython config_loader.py
chmod 600 .env


git init
git add .
git commit -m "Versão funcional do robô Binance Testnet"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/trading-bot.git
git push -u origin main

tmux attach -t trading-bot



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

