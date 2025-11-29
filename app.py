import requests
from solana.rpc.api import Client

def check_honeypot(token_mint):
    dexscreener = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{token_mint}").json()
    data = dexscreener['pairs'][0] if dexscreener['pairs'] else None
    return (data and data['liquidity']['usd'] > 10000 and 
            data['pairAgeHuman'] > '5 mins' and data['txns']['h24']['buys'] > 50)

def smart_trade(token_mint, amount_sol=0.05, entry_price=None):
    if not check_honeypot(token_mint): return {"error": "Honeypot detectado"}
    
    # Buy via Jupiter
    tx_buy = swap_meme(token_mint, amount_sol)  # Do código anterior
    
    # Monitor loop (APScheduler ou JS frontend)
    current_price = get_price(token_mint)  # Dexscreener API
    profit = (current_price / entry_price - 1) * 100 if entry_price else 0
    
    if profit >= 45:
        sell_half = swap_meme("So11111111111111111111111111111111111111112", amount_sol/2)  # 50% to SOL
        return {"tp": True, "tx_sell": sell_half}
    elif profit <= -15:
        sell_all = swap_meme("So11111111111111111111111111111111111111112", amount_sol)
        return {"sl": True, "tx_sell": sell_all, "reinvest": "50/50 next"}
    
    return {"hold": profit}

@app.route("/smart_buy", methods=['POST'])
def execute_strategy():
    data = request.json
    token = data['token']
    result = smart_trade(token, 0.05)
    return jsonify(result)

@app.route('/api/stream')
def stream():
    def event_stream():
        while True:
            data = get_status()  # Sua lógica
            yield f"data: {json.dumps(data)}

"
            time.sleep(2)
    return Response(event_stream(), mimetype='text/plain')
