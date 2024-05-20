from web3 import Web3
from lib.client.contracts.base import ContractBase

class StudentInfo(ContractBase):
    contract = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.6.0;
        pragma experimental ABIEncoderV2;

        contract StudentInformation {
        
            struct Information {
                string student_first_name;
                string student_last_name;
                uint16 birthday;
            }

            Information[] private students;

            function set(Information memory value) public {
                students.push(value);
            }

            function list() public view returns (Information[] memory) {
                return students;
            }
        }
        """
    def __init__(self, account_address=None):
        super().__init__()
        if account_address: self.account_address = Web3.to_checksum_address(account_address)
        self.contract_address = Web3.to_checksum_address("0x3c48125F6972380B6866e7502c559e5Cf17D7bD4")

    def set(self, information, password):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.set(information)

        call_fn = self.prepare_transaction(contract)
        signed_transaction = self.sign_transaction(call_fn)
        tx_hash = self.send_raw_transaction(signed_transaction)
        print(self.wait_for_receipt(tx_hash))

    def list(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        raw = contract.functions.list().call()
        prepared = []
        for student in raw:
            prepared.append({
                "first_name": student[0],
                "last_name": student[1],
                "birthday": student[2]
            })
        
        return prepared