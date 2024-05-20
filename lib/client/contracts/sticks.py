from lib.client.contracts.base import ContractBase

class Sticks(ContractBase):
    contract = """
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.6.0;
        pragma experimental ABIEncoderV2;

        contract Sticks {
        
            enum Players { Player1, Player2, None }
            address NullAddress = payable(address(0));

            struct Meta {
                address player1_address;
                address player2_address;
                Players current_player;
                Players winner;
                uint8 player_count;
                int256 sticks_count;
            }

            Meta private state;
            Meta[] private history;
            
            constructor(string memory _we) public {
                state = Meta(NullAddress, NullAddress, Players.None, Players.None, 0, 10);
                history.push(state);
            }
         
            function join(address player_address) public {
                if (state.player_count == 0) {
                    state = Meta(player_address, NullAddress, Players.None, Players.None, 1, 10);
                    history.push(state);
                } else if (state.player_count == 1) {
                    state = Meta(state.player1_address, player_address, Players.Player1, Players.None, 2, 10);
                    history.push(state);
                }
            }
            
            function play(address player_address, int how_much) public {
                if (state.player1_address == player_address && state.current_player == Players.Player1) {
                    if (state.sticks_count - how_much <= 0) {
                        state = Meta(state.player1_address, state.player2_address, Players.None, Players.Player2, 2, state.sticks_count - how_much);
                        history.push(state);
                    } else {
                        state = Meta(state.player1_address, state.player2_address, Players.Player2, Players.None, 2, state.sticks_count - how_much);
                        history.push(state);
                    }
                } else if (state.player2_address == player_address && state.current_player == Players.Player2) {
                    if (state.sticks_count - how_much <= 0) {
                        state = Meta(state.player1_address, state.player2_address, Players.None, Players.Player1, 2, state.sticks_count - how_much);
                        history.push(state);
                    } else {
                        state = Meta(state.player1_address, state.player2_address, Players.Player1, Players.None, 2, state.sticks_count - how_much);
                        history.push(state);
                    }
                }
            }

            function can_join() public view returns (bool) {
                return state.player_count < 2;
            }

           function game_ended() public view returns (bool) {
                return state.sticks_count <= 0;
           }

           function get_state() public view returns (Meta memory) {
                return state;
           }
        }
        """
    def __init__(self):
        super().__init__()
        self.contract_address = "0xfF4C32a620e5Fc58699E8786014aD7Bc13A47474"

    def join(self, address):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.join(address)
    
        call_fn = self.prepare_transaction(contract)
        signed_transaction = self.sign_transaction(call_fn)
        tx_hash = self.get_transaction_hash(signed_transaction)
        print(self.wait_for_receipt(tx_hash))

    def play(self, address, count):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        contract = contract.functions.play(address, count)
    
        call_fn = self.prepare_transaction(contract)
        signed_transaction = self.sign_transaction(call_fn)
        tx_hash = self.get_transaction_hash(signed_transaction)
        print(self.wait_for_receipt(tx_hash))

    def game_ended(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.game_ended().call()

    def get_state(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.get_state().call()

    def can_join(self):
        contract = self.w3.eth.contract(abi=self.abi, address=self.contract_address)
        return contract.functions.can_join().call()
