from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545')) # Change to your RPC provider
with open('../build/contracts/Notes.json') as f:
    abi = json.load(f)["abi"]
contract_address = '0x6a48BBb770CB895A6B7a80396dB3a2fac83fA0BD'
 # Replace with your contract address

# contract = w3.eth.contract(address=contract_address, abi=abi)
# Verify if the connection is successful
if w3.is_connected():
    print("Connected to Ethereum network")

    # Load contract instance
    contract = w3.eth.contract(address=contract_address, abi=abi)

    # Print contract functions
    # print("Contract functions:", contract.functions)

else:
    print("Failed to connect to Ethereum network")