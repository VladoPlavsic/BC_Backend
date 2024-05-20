from web3 import Web3
from web3.auto import w3
from lib.client.contracts.base import ContractBase

class Semaphore(ContractBase):
    contract = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.6.0;
        pragma experimental ABIEncoderV2;

        contract Semaphore {
        
            enum Light { Red, Yellow, Green }

            Light private currentState;
            
            constructor() public {
                currentState = Light.Red;
            }

            function get_current_state() public view returns (string memory) {
                if (currentState == Light.Red) {
                    return "Red";
                } else if (currentState == Light.Yellow) {
                    return "Yellow";
                } else if (currentState == Light.Green) {
                    return "Green";
                }
            }

            function change_light() public {
                if (currentState == Light.Red) {
                    currentState = Light.Yellow;
                } else if (currentState == Light.Yellow) {
                    currentState = Light.Green;
                } else if (currentState == Light.Green) {
                    currentState == Light.Red;
                }
            }
        }
        """
    def __init__(self, account_address=None):
        super().__init__()
        if account_address: self.account_address = Web3.to_checksum_address(account_address)
        self.contract_address = "0x4708ca2bE846F899aeB98F4A8a5009A018787D50"


    def change_light(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.change_light()
        call_fn = self.prepare_transaction(contract)
        signed_transaction = self.sign_transaction(call_fn)
        tx_hash = self.send_raw_transaction(signed_transaction)
        result = self.wait_for_receipt(tx_hash)
        print(result)
        return result

    def get_current_state(self):
        key = {"address":"2ee4b180678ee32a88e10bbe7c4efe4a6f9b70de","crypto":{"cipher":"aes-128-ctr","ciphertext":"80a57f00a9bb250d1f5ad7f69fad377e71a82f40fb4be91122ed40cda6c7a12a","cipherparams":{"iv":"15ce2262550e4a01059ab0b388d3c090"},"kdf":"scrypt","kdfparams":{"dklen":32,"n":262144,"p":1,"r":8,"salt":"f4b19a9a613be44e9030910bfa7c203b1067bc5036a552475ccf9312201c5063"},"mac":"2f01efc5a35d9196eeaca8e5aaea968acbf165b592fd0a4c076539ada6a82119"},"id":"4b3e8f4d-e628-4e9d-944a-65bbb3c6e553","version":3}
        priv_key = w3.eth.account.decrypt(key, "password")
        print(priv_key.hex())
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.get_current_state().call()
