# -*- coding: utf-8 -*-
from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator, Bip39Languages,
    Bip44, Bip44Coins, Bip84, Bip84Coins
)

def derive_eth_wallet(seed_bytes):
    wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).DeriveDefaultPath()
    return {
        "coin": "Ethereum",
        "address": wallet.PublicKey().ToAddress(),
        "private_key": wallet.PrivateKey().Raw().ToHex()
    }

def derive_btc_wallet(seed_bytes):
    wallet = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN).DeriveDefaultPath()
    return {
        "coin": "Bitcoin (BIP84 - Native SegWit)",
        "address": wallet.PublicKey().ToAddress(),
        "private_key": wallet.PrivateKey().ToWif()
    }

if __name__ == "__main__":
    print("=== Ethereum & Bitcoin Wallet Derivation ===\n")
    mnemonic = input("Enter 12/24-word BIP39 mnemonic: ").strip()

    # ✅ FIXED: Use validator object pattern
    validator = Bip39MnemonicValidator(lang=Bip39Languages.ENGLISH)
    if not validator.IsValid(mnemonic):
        print("❌ Invalid mnemonic.")
        exit(1)

    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    eth_wallet = derive_eth_wallet(seed_bytes)
    btc_wallet = derive_btc_wallet(seed_bytes)

    print("\n--- Ethereum ---")
    print(f"Address:     {eth_wallet['address']}")
    print(f"Private Key: {eth_wallet['private_key']}")

    print("\n--- Bitcoin (BIP84) ---")
    print(f"Address:     {btc_wallet['address']}")
    print(f"Private Key: {btc_wallet['private_key']}")
