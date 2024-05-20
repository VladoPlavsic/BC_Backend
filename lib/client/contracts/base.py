
from web3 import Web3, middleware, HTTPProvider

from lib.client.base import Base
from lib.client.contracts.builder import build_contract
from lib.client.contracts.builder import get_abi_from_compiled_contract
from lib.client.contracts.builder import get_bytecode_from_compiled_contract

class ContractBase(Base):
    contract = ""
    account_address = None

    def __init__(self):
        super().__init__()
        self.setup_contract()

    def setup_contract(self):
        contract_name, compiled = build_contract(self.contract)
        self.abi = get_abi_from_compiled_contract(compiled, contract_name)
        self.bbytecode = get_bytecode_from_compiled_contract(compiled, contract_name)

    def initialize_contract(self, abi, bytecode):
        return self.w3.eth.contract(abi=abi, bytecode=bytecode)

    def prepare_transaction(self, contract):
        return contract.build_transaction(
            self.transaction_args()
        )

    def prepare_contract_transaction(self, Contract):
        return Contract.constructor().build_transaction(
           self.transaction_args()
        )
    
    def transaction_args(self):
        import time    
        nonce = int(time.time())
        nonce = self.w3.eth.get_transaction_count(self.account_address)
        gas_price = self.w3.eth.gas_price
        return  {
                "chainId": 1214,
                "from": self.account_address,
                "nonce": nonce,
                "gasPrice": gas_price
            }

    def get_transaction_count(self):
        return self.w3.eth.get_transaction_count(self.account_address)

    def sign_transaction(self, transaction):
        return self.w3.eth.account.sign_transaction(transaction, private_key="0x7d5f3566289fa9fa5893d782612dcaa550e8613c29699c6c0fda498613d5ebfa")
        
    def send_raw_transaction(self, signed_transaction):
        return self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    def wait_for_receipt(self, transaction_hash):
        return self.w3.eth.wait_for_transaction_receipt(transaction_hash)

    def deploy_contract(self, password):
        self.unlock_account(self.account_address, password)
        print("Deploying contract...")
        print("---------------------------------------------")
        print(self.contract)
        transaction_hash = self.w3.eth.send_transaction({
            "from": Web3.to_checksum_address(self.account_address),
            "data": self.bbytecode
        })
        self.lock_account(self.account_address)
        print("---------------------------------------------")
        transaction_receipt = self.wait_for_receipt(transaction_hash)
        self.contract_address = transaction_receipt.contractAddress
        return self.contract_address
  