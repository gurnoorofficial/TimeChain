# -*- coding: utf-8 -*-
from eth_account.messages import encode_defunct
from eth_account import Account
import sys
import os

def verify_signature(message: str, signature: str):
    try:
        message_encoded = encode_defunct(text=message)
        recovered_address = Account.recover_message(message_encoded, signature=signature)
        return {
            "valid": True,
            "recovered_address": recovered_address
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }

if __name__ == "__main__":
    print("=== Ethereum Signature Verifier ===\n")

    # Step 1: Get path to message file
    file_path = input("Enter path to .txt file containing the original message: ").strip().strip('"')


    if not os.path.isfile(file_path):
        print("❌ File not found.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        message = f.read().strip()

    print(f"\nLoaded message from: {file_path}")
    print(f"Preview: {message[:80]}{'...' if len(message) > 80 else ''}\n")

    # Step 2: Get signature
    signature = input("Enter signature (0x...): ").strip()

    # Step 3: Verify
    result = verify_signature(message, signature)
    print("\n--- Verification Result ---")
    if result["valid"]:
        print("✅ Signature is VALID")
        print("Recovered Ethereum address:", result["recovered_address"])
    else:
        print("❌ Signature is INVALID")
        print("Error:", result["error"])
