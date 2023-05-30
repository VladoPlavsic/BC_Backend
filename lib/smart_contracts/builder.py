import json
from typing import Tuple

from solcx import compile_standard, install_solc
from solidity_parser import parse

def build_contract(raw_sol) -> Tuple[str, str]:
    contract_name = get_contract_name(raw_sol)
    
    install_solc("0.6.0")
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {f'{contract_name}.sol': {"content": raw_sol}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.6.0"
    )

    return [contract_name, compiled]

def get_contract_name(raw_sol):
    for child in parse(raw_sol)['children']:
        if child['type'] == 'ContractDefinition':
            return child['name']

def get_bytecode_from_compiled_contract(contract, contract_name):
    return contract["contracts"][f"{contract_name}.sol"][contract_name]["evm"]["bytecode"]["object"]

def get_abi_from_compiled_contract(contract, contract_name):
    return json.loads(contract["contracts"][f"{contract_name}.sol"][contract_name]["metadata"])["output"]["abi"]

