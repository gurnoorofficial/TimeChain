import json
import os
from datetime import datetime, timezone
from eth_utils import keccak
from web3 import Web3

# === Constants ===
BLOCKCHAIN_FILE = "/root/TimeChain/blockchain.json"
FINGERPRINT_FILE = "/root/TimeChain/chain_fingerprint.txt"
INFURA_URL = "https://mainnet.infura.io/v3/e8740e4245d64df0bb6d7966a77255c3"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

MAX_BLOCKS = 10  # ⬅️ New max block limit

def keccak_hash(data):
    return keccak(data.encode() if isinstance(data, str) else data).hex()

def normalize_message(msg):
    return msg.replace('\\n', '\n').replace('\r\n', '\n').strip()

def calculate_block_hash(block_data):
    block_copy = dict(block_data)
    block_copy.pop("hash", None)
    if "message" in block_copy:
        block_copy["message"] = normalize_message(block_copy["message"])
    data = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(data).hex()

def is_chain_valid(chain):
    for i in range(1, len(chain)):
        prev = chain[i - 1]
        curr = chain[i]
        if curr["previous_hash"] != calculate_block_hash(prev):
            print(f"❌ Tampering: block {i} has invalid previous hash")
            return False
        if curr["hash"] != calculate_block_hash(curr):
            print(f"❌ Tampering: block {i} has invalid current hash")
            return False
    return True

def load_blockchain():
    if not os.path.exists(BLOCKCHAIN_FILE):
        if os.path.exists(FINGERPRINT_FILE):
            raise Exception("❌ blockchain.json is missing — possible tampering or accidental deletion.")
        print("🆕 Starting new blockchain (empty).")
        return []

    with open(BLOCKCHAIN_FILE, "r") as f:
        chain = json.load(f)

    if not is_chain_valid(chain):
        raise Exception("❌ Blockchain integrity check failed!")

    if os.path.exists(FINGERPRINT_FILE):
        with open(FINGERPRINT_FILE, "r") as f:
            expected_hash = f.read().strip()
            if chain[-1]["hash"] != expected_hash:
                raise Exception("❌ Chain fingerprint mismatch — possible rollback.")

    return chain

def save_chain_fingerprint(chain):
    with open(FINGERPRINT_FILE, "w") as f:
        f.write(chain[-1]["hash"])

def save_blockchain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)
    save_chain_fingerprint(chain)

def add_block(message, signature):
    chain = load_blockchain()
    if len(chain) >= MAX_BLOCKS:
        raise ValueError(f"❌ Maximum number of blocks ({MAX_BLOCKS}) reached.")

    message = normalize_message(message)
    index = len(chain)
    timestamp, eth_block = get_latest_eth_timestamp()
    previous_hash = calculate_block_hash(chain[-1]) if chain else "0"

    new_block = {
        "index": index,
        "message": message,
        "timestamp": timestamp,
        "eth_block": eth_block,
        "signature": signature,
        "previous_hash": previous_hash
    }
    new_block["hash"] = calculate_block_hash(new_block)

    chain.append(new_block)
    save_blockchain(chain)
    return new_block

def get_latest_eth_timestamp():
    block = w3.eth.get_block('latest')
    block_time = datetime.fromtimestamp(block["timestamp"], timezone.utc).replace(tzinfo=None).isoformat()
    return block_time, block["number"]

def eth_signed_message(message):
    prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return (prefix + message).encode()
