from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, SolAddrEncoder

def derive_trustwallet_solana(mnemonic: str):
    # Generate seed
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    # Use m/44'/501'/0'
    bip44_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA).Purpose().Coin().Account(0)

    private_key_bytes = bip44_ctx.PrivateKey().Raw().ToBytes()
    public_key_bytes = bip44_ctx.PublicKey().RawCompressed().ToBytes()[1:]

    sol_address = SolAddrEncoder.EncodeKey(public_key_bytes)
    return sol_address, private_key_bytes.hex()

if __name__ == "__main__":
    mnemonic = input("Enter mnemonic:\n> ").strip()
    address, priv = derive_trustwallet_solana(mnemonic)
    print(f"\n📬 Solana Address: {address}")
    print(f"🔐 Private Key: {priv}")
