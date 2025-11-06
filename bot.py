import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message, parse_mode="Markdown"):
    if not TOKEN or not CHAT_ID:
        print("⚠️ Telegram não configurado corretamente.")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": parse_mode}

    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print(f"📩 Alerta enviado: {message}")
            return True
        else:
            print(f"❌ Erro Telegram ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"🚨 Falha ao enviar alerta: {e}")
    return False
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



