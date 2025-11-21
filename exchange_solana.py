# exchange_solana.py
import os
import requests
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
from solana.rpc.types import TxOpts
from dotenv import load_dotenv

load_dotenv()
SOLANA_RPC = os.getenv("SOLANA_RPC")
client = Client(SOLANA_RPC)

# carregue sua Keypair (ex.: arquivo JSON exportado da Trust/Phantom)
keypair = Keypair.from_secret_key(bytes([...]))  # `from_secret_key` com bytes

JUPITER_QUOTE_URL = "https://quote-api.jup.ag/v1/quote"  # endpoint de exemplo
JUPITER_SWAP_URL = "https://quote-api.jup.ag/v1/swap"   # endpoint de exemplo

def get_jupiter_quote(inputMint, outputMint, amount):
    params = {"inputMint": inputMint, "outputMint": outputMint, "amount": amount, "slippage": 1}
    r = requests.get(JUPITER_QUOTE_URL, params=params)
    return r.json()

def send_signed_tx(tx: Transaction):
    res = client.send_transaction(tx, keypair, opts=TxOpts(preflight_commitment="confirmed"))
    return res
