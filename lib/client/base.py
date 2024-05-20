from web3 import Web3, middleware, HTTPProvider
from eth_account import account

from lib.core.config import CHAIN_ID

class Base:
    def __init__(self):
        self.setup_w3_client()
        self.chain_id = CHAIN_ID

    def setup_w3_client(self):
        self.w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
        self.w3.middleware_onion.inject(middleware.geth_poa_middleware, layer=0)
        
    def unlock_account(self, address, password):
        result = self.w3.geth.personal.unlock_account(Web3.to_checksum_address(address), password)
        print(f"unlock: {result}")
        return result
    
    def lock_account(self, address):
        result = self.w3.geth.personal.lock_account(Web3.to_checksum_address(address))
        print(f"lock: {result}")
        return result