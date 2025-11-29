# Parâmetros otimizados para Pump.fun/Dexscreener
HONEYPOT_FILTERS = {
    'min_liquidity_usd': 15000,      # Evita rugs
    'min_holders': 150,              # Distribuição real
    'min_age_minutes': 8,            # Pós-honeymoon dump
    'min_txns_5m': 75,               # Momentum real
    'max_age_hours': 24,             # Fresh pumps
    'min_price_change_5m': 25,       # >25% em 5min
    'blacklist_keywords': ['dev', 'team', 'locked']  # Rug signals
}

STRATEGY_PARAMS = {
    'test_buy_sol': 0.03,            # $5 teste
    'full_buy_sol': 0.08,            # $12 posição
    'take_profit_pct': [40, 50],     # TP tiers
    'stop_loss_pct': -17,            # SL conservador
    'slippage_bps': 150,             # 1.5% Solana volátil
    'max_positions': 5,              # Diversificação
    'cooldown_minutes': 3            # Anti-spam
}
