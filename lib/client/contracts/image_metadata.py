from web3 import Web3
from web3.auto import w3
from lib.client.contracts.base import ContractBase

class ImageMetadata(ContractBase):
    contract = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.6.0;
        pragma experimental ABIEncoderV2;

        contract ImageMetadata {
        
            struct Meta {
                string ipfs_address;
                uint256 size;
            }

            mapping(string => Meta) private store;
            string[] private images;

            function get(string memory key) public view returns (Meta memory) {
                return store[key];
            }

            function set(string memory key, Meta memory value) public {
                images.push(key);
                store[key] = value;
            }

            function list() public view returns (string[] memory) {
                return images;
            }
        }
        """
    def __init__(self, account_address=None):
        super().__init__()
        if account_address: self.account_address = Web3.to_checksum_address(account_address)
        self.contract_address = Web3.to_checksum_address("0xcE947c238Bfc0C31E0d8203b52327b5A4F01830e")

    def set(self, key, meta, password):
        print(meta)
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.set(key, meta)

        call_fn = self.prepare_transaction(contract)
        self.unlock_account(self.account_address, password)
        tx_hash = self.w3.eth.send_transaction(call_fn)
        self.lock_account(self.account_address)
        print(self.wait_for_receipt(tx_hash))

    def get(self, key):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.get(key).call()

    def list(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.list().call()

    def get_all(self):
        keys = self.list()
        values = {}
        for key in keys:
            values[key] = self.get(key)
        return prepare_all_meta_response(values)
    
def prepare_all_meta_response(contract_response):
    response = []
    for filename in contract_response:
        response.append({
            "filename": filename, 
            "size": contract_response[filename][1]
            }
        )
    return response
