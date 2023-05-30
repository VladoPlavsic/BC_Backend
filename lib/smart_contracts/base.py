
from web3 import Web3, middleware, HTTPProvider

from lib.smart_contracts.builder import build_contract
from lib.smart_contracts.builder import get_abi_from_compiled_contract
from lib.smart_contracts.builder import get_bytecode_from_compiled_contract


class ContractBase:
    contract = ""

    def __init__(self):
        self.url = "http://localhost:5001/api/v0"
        self.setup_w3_client()
        self.setup_account()
        self.chain_id = 51515
        self.setup_contract()

    def setup_w3_client(self):
        self.w3 = Web3(HTTPProvider("http://93.95.97.136:8545"))
        self.w3.middleware_onion.inject(middleware.geth_poa_middleware, layer=0)

    def setup_account(self):
        self.account_address = "0x81C9d4C3F771B35108F624c9C4E540679683c437"
        self.private_key = "0x4803895426f9ba5a9f8667ef849df3c1a794293f2839d4e8f4986f286e58c0fe"

    def setup_contract(self):
        print(self.contract)
        contract_name, compiled = build_contract(self.contract)
        self.abi = get_abi_from_compiled_contract(compiled, contract_name)
        self.bbytecode = get_bytecode_from_compiled_contract(compiled, contract_name)

    def initialize_contract(self, abi, bytecode):
        return self.w3.eth.contract(abi=abi, bytecode=bytecode)

    def prepare_transaction(self, contract):
        nonce = self.get_transaction_count()
        return contract.build_transaction(
            {
                "chainId": self.chain_id,
                "from": self.account_address,
                "nonce": nonce,
                "gasPrice": 100
             }
        )

    def prepare_contract_transaction(self, Contract):
        nonce = self.get_transaction_count()
        return Contract.constructor("1").build_transaction(
            {
                "chainId": self.chain_id,
                "from": self.account_address,
                "nonce": nonce,
                "gasPrice": 100
            }
        )
    
    def get_transaction_count(self):
        return self.w3.eth.get_transaction_count(self.account_address)

    def sign_transaction(self, transaction):
        return self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        
    def get_transaction_hash(self, signed_transaction):
        return self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    def wait_for_receipt(self, transaction_hash):
        return self.w3.eth.wait_for_transaction_receipt(transaction_hash)

    def deploy_contract(self):
        Contract = self.initialize_contract(self.abi, self.bbytecode)
        transaction = self.prepare_contract_transaction(Contract)
        signed_transaction = self.sign_transaction(transaction)
        transaction_hash = self.get_transaction_hash(signed_transaction)
        transaction_receipt = self.wait_for_receipt(transaction_hash)
        self.contract_address = transaction_receipt.contractAddress
        print(self.contract_address)
