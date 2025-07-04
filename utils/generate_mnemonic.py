import secrets
import hashlib
import os

# Load BIP39 English wordlist (2048 words)
def load_wordlist():
    wordlist_path = os.path.join(os.path.dirname(__file__), "bip39_english.txt")
    with open(wordlist_path, "r", encoding="utf-8") as f:
        return [word.strip() for word in f.readlines()]

# Generate 128-bit entropy + checksum for 12-word mnemonic
def generate_mnemonic(wordlist):
    entropy = secrets.token_bytes(16)  # 128 bits
    entropy_bits = bin(int.from_bytes(entropy, byteorder="big"))[2:].zfill(128)

    checksum = bin(int(hashlib.sha256(entropy).hexdigest(), 16))[2:].zfill(256)[:4]
    full_bits = entropy_bits + checksum  # 132 bits

    mnemonic = []
    for i in range(0, 132, 11):
        index = int(full_bits[i:i+11], 2)
        mnemonic.append(wordlist[index])
    
    return " ".join(mnemonic)

if __name__ == "__main__":
    print("=== BIP39 12-Word Mnemonic Generator ===\n")

    wordlist = load_wordlist()
    mnemonic = generate_mnemonic(wordlist)

    print("🔐 Your 12-word mnemonic:")
    print(mnemonic)
