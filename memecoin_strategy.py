import requests

def check_honeypot(token_mint):
    dexscreener = requests.get(
        f"https://api.dexscreener.com/latest/dex/tokens/{token_mint}"
    ).json()
    pairs = dexscreener.get("pairs") or []
    if not pairs:
        return False

    data = pairs[0]
    liq = float(data.get("liquidity", {}).get("usd", 0))
    buys_24h = int(data.get("txns", {}).get("h24", {}).get("buys", 0))
    age = str(data.get("pairAgeHuman", ""))

    return liq > 10000 and "min" in age and buys_24h > 50


def smart_trade(token_mint, amount_sol=0.05, entry_price=None):
    if not check_honeypot(token_mint):
        return {"error": "Honeypot detectado"}

    # TODO: implementar swap_meme() e get_price()
    tx_buy = swap_meme(token_mint, amount_sol)

    current_price = get_price(token_mint)
    profit = (current_price / entry_price - 1) * 100 if entry_price else 0

    if profit >= 45:
        sell_half = swap_meme("So11111111111111111111111111111111111111112", amount_sol / 2)
        return {"tp": True, "tx_sell": sell_half}

    if profit <= -15:
        sell_all = swap_meme("So11111111111111111111111111111111111111112", amount_sol)
        return {"sl": True, "tx_sell": sell_all, "reinvest": "50/50 next"}

    return {"hold": profit}
