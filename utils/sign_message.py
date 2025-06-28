from eth_account import Account
from eth_account.messages import encode_defunct
from datetime import datetime

def sign():
    print("✍️  Ethereum Message Signer (Web-Compatible Format)\n")

    raw_message = input("📝 Enter message to sign: ").strip()
    private_key = input("🔑 Enter private key (starting with 0x): ").strip()

    if not private_key.startswith("0x") or len(private_key) != 66:
        print("❌ Invalid private key format.")
        return

    timestamp = datetime.utcnow().isoformat().split(".")[0]
    full_message = f"{raw_message} {timestamp}"

    try:
        account = Account.from_key(private_key)
        eth_address = account.address
        encoded_msg = encode_defunct(text=full_message)
        signed = Account.sign_message(encoded_msg, private_key=private_key)

        print("\n✅ Signature Complete:")
        print(f"📮 Address : {eth_address}")
        print(f"🧾 Message : {full_message}")
        print(f"✍️  Signature: 0x{signed.signature.hex()}")

    except Exception as e:
        print(f"❌ Signing failed: {e}")

if __name__ == "__main__":
    sign()
