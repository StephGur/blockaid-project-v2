from web3 import Web3

from config import BLOCKAID_CONFIG

w3 = Web3(Web3.HTTPProvider(BLOCKAID_CONFIG.INFURA_URL))
