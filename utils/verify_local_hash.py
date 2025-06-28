import json
from eth_utils import keccak
import os

def keccak_hash(data):
    """Returns the keccak256 hash (Ethereum-style) as a hex string."""
    if isinstance(data, str):
        data = data.encode()
    return keccak(data).hex()

def normalize_message(msg):
    """Ensure consistent line breaks and remove excess whitespace."""
    return msg.replace('\\n', '\n').replace('\r\n', '\n').strip()

def calculate_block_hash(block_data):
    """Calculates the hash of a block, excluding the 'hash' field and normalizing the message."""
    block_copy = dict(block_data)
    block_copy.pop("hash", None)

    if "message" in block_copy:
        block_copy["message"] = normalize_message(block_copy["message"])

    raw = json.dumps(block_copy, sort_keys=True, separators=(',', ':')).encode()
    return keccak(raw).hex()

def main():
    path = input("📄 Enter path to blockchain JSON file: ").strip().strip('"').strip("'")

    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            chain = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read JSON: {e}")
        return

    if not isinstance(chain, list):
        print("❌ Expected a list of blocks in the JSON.")
        return

    print("\n🔎 Calculating normalized Keccak-256 hashes for each block...\n")
    for block in chain:
        if "index" not in block:
            print("⚠️  Skipping block (missing 'index')")
            continue

        index = block["index"]
        expected = block.get("hash", "[no saved hash]")
        calculated = calculate_block_hash(block)

        match = "✅ MATCH" if calculated == expected else "❌ MISMATCH"
        print(f"Block {index}:\n  Expected:   {expected}\n  Calculated: {calculated}\n  Status:     {match}\n")

if __name__ == "__main__":
    main()
