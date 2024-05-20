from web3 import Web3
from eth_account import account

from lib.core.config import CHAIN_ID
from lib.client.base import Base

class Account(Base):
    def __init__(self):
        super().__init__()

    def create_account(self, password):
        return {"address": self.w3.geth.personal.new_account(password)}

    def get_accounts(self):
        return self.w3.geth.personal.list_accounts()
    
    def send_wei(self, from_ ,to, amount, password):
        self.unlock_account(from_, password)
        result = self.w3.eth.send_transaction({
            "from": Web3.to_checksum_address(from_),
            "to": Web3.to_checksum_address(to),
            "value": int(amount)
        })
        self.lock_account(from_)
        return result.hex()

    def check_transaction(self, tx):
        result = self.w3.eth.get_transaction(tx)
        print(dict(result))
        return self.__prepare_transaction_result(dict(result))

    def __prepare_transaction_result(self, result):
        print(result)
        return {
            "block_hash": result["blockHash"],
            "block_number": result["blockNumber"],
            "to": result["to"],
            "gas": result["gas"],
            "gas_price": result["gasPrice"],
            "type": result["type"],
        }
    
    def get_balance(self, address):
        return f'{self.w3.eth.get_balance(Web3.to_checksum_address(address), "latest")}'
