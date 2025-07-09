from web3 import Web3
from config import get_settings

env = get_settings()

INFURA_URL = env.infura_url
PRIVATE_KEY = env.private_key
CONTRACT_ADDRESS = env.contract_address
WALLET_ADDRESS = env.wallet_address

# Remix’dan olingan contract ABI (public, xavfsiz)
contract_abi = [
    {
        "inputs": [{"internalType": "bytes32", "name": "docHash", "type": "bytes32"}],
        "name": "addDocumentHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "name": "documentOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "docHash", "type": "bytes32"}],
        "name": "getOwner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Web3 ulanishi
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def save_hash_to_blockchain(hash_value):
    """
    Hujjat hashini (sha256, hex formatda) Ethereum blokcheynga yozadi.
    :param hash_value: 64 belgili hex string (misol: "740d13b3...")
    :return: tx_hash (string)
    """
    # 1. Hex stringni bytes32 formatga o‘girish
    if not hash_value.startswith('0x'):
        doc_hash = Web3.to_bytes(hexstr='0x' + hash_value)
    else:
        doc_hash = Web3.to_bytes(hexstr=hash_value)

    # 2. Tranzaksiyani qurish
    tx = contract.functions.addDocumentHash(doc_hash).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': w3.eth.get_transaction_count(WALLET_ADDRESS),
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    # 3. Tranzaksiyani imzolash
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    # 4. Yangi versiyada: raw_transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()