from lib.smart_contracts.base import ContractBase

class ImageMetadata(ContractBase):
    contract = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.6.0;
        pragma experimental ABIEncoderV2;

        contract KeyValueStore {
        
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
    def __init__(self):
        super().__init__()
        self.contract_address = "0x98F975cA85b80892Fc242963a62F85c9d20144D1"

    def set(self, key, meta):
        print(meta)
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.set(key, meta)

        call_fn = self.prepare_transaction(contract)
        signed_transaction = self.sign_transaction(call_fn)
        tx_hash = self.get_transaction_hash(signed_transaction)
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
