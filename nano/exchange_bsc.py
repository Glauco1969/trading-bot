# exchange_bsc.py
import os
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
import json

load_dotenv()
BSC_RPC = os.getenv("BSC_RPC")
PRIVATE_KEY = os.getenv("BSC_PRIVATE_KEY")
w3 = Web3(Web3.HTTPProvider(BSC_RPC))
account = Account.from_key(PRIVATE_KEY)
address = account.address

# carregar ABI do PancakeRouter
with open("pancake_router_abi.json") as f:
    router_abi = json.load(f)

ROUTER_ADDRESS = Web3.toChecksumAddress("0x...PancakeRouterAddress...")  # substituir
router = w3.eth.contract(address=ROUTER_ADDRESS, abi=router_abi)

def buy_token_with_bnb(token_address, amount_bnb, slippage=0.01):
    # converter BNB para token via swapExactETHForTokensSupportingFeeOnTransferTokens
    path = [w3.toChecksumAddress(w3.toHex(Web3.toBytes(hexstr='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'))), w3.toChecksumAddress(token_address)]
    deadline = int(w3.eth.get_block('latest')['timestamp']) + 60*10
    value = w3.toWei(amount_bnb, 'ether')
    tx = router.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
        0,  # min amount out -> calcular com slippage
        path,
        address,
        deadline
    ).buildTransaction({
        'from': address,
        'value': value,
        'gas': 300000,
        'nonce': w3.eth.get_transaction_count(address),
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.toHex(tx_hash)
