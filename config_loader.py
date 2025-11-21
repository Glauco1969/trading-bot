# config_loader.py
import os
from dotenv import load_dotenv

def load_and_validate_env():
    load_dotenv()

    required_vars = [
        "EXCHANGE", "SYMBOL", "API_KEY", "API_SECRET",
        "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"⚠️ Variáveis ausentes no .env: {', '.join(missing)}")

    print("✅ Ambiente carregado com sucesso!")
    print(f"Exchange: {os.getenv('EXCHANGE')}")
    print(f"Par de trade: {os.getenv('SYMBOL')}")
    print(f
