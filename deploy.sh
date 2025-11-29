#!/bin/bash
# Para Termux -> FTP (seu método)
pip install -r requirements.txt --quiet
echo "PHANTOM_PRIVATE_KEY=your_key" > .env
echo "RPC_URL=https://api.mainnet-beta.solana.com" >> .env
nohup python app.py > app.log 2>&1 &
echo "🚀 Live em http://0.0.0.0:5000 - Logs: tail -f app.log"
