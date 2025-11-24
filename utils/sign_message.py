from eth_account import Account
from eth_account.messages import encode_defunct
from datetime import datetime

def sign_message():
    print("✍️ Ethereum Message Signer (Ethers.js compatible)\n")

    raw_message = input("📝 Enter message: ").strip()
    private_key = input("🔑 Enter private key (0x...): ").strip()

    # Validate key
    if not private_key.startswith("0x") or len(private_key) != 66:
        print("❌ Invalid private key format (must be 0x + 64 hex chars).")
        return

    # ---- SAME TIMESTAMP FORMAT AS HTML/JS ----
    timestamp = datetime.utcnow().isoformat().split('.')[0]   # "YYYY-MM-DDTHH:MM:SS"
    full_message = f"{raw_message} {timestamp}"

    try:
        # Create account from private key
        acct = Account.from_key(private_key)

        # Same encoding as ethers.js "personal_sign"
        encoded_msg = encode_defunct(text=full_message)

        # Sign message
        signed = acct.sign_message(encoded_msg)

        print("\n✅ SIGNATURE COMPLETE:")
        print(f"Address   : {acct.address}")
        print(f"Message   : {full_message}")
        print(f"Signature : 0x{signed.signature.hex()}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    sign_message()
