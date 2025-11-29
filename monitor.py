import requests, time, schedule
from config import HONEYPOT_FILTERS, STRATEGY_PARAMS

def find_targets():
    # Top 20 Pump.fun novos
    pump_new = requests.get("https://frontend-api.pump.fun/coins?offset=0&limit=20").json()
    
    # Dexscreener gainers Solana
    dexscreener = requests.get("https://api.dexscreener.com/latest/dex/search/?q=solana").json()
    
    targets = []
    for coin in pump_new + dexscreener['pairs'][:20]:
        if passes_filters(coin):  
            targets.append({
                'mint': coin['mint'],
                'score': coin.get('priceChange', 0) * coin.get('liquidity', 0)/10000
            })
    return sorted(targets, key=lambda x: x['score'], reverse=True)[:3]

def passes_filters(coin):
    return (coin.get('liquidity', 0) > HONEYPOT_FILTERS['min_liquidity_usd'] and
            coin.get('pairAge', 0) > HONEYPOT_FILTERS['min_age_minutes']*60 and
            coin.get('txns', {}).get('buys', 0) > HONEYPOT_FILTERS['min_txns_5m'])

schedule.every(45).seconds.do(find_targets)  # Scan a cada 45s
