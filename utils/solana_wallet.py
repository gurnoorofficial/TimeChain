from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, SolAddrEncoder, Bip44Changes

def derive_solana_address(mnemonic: str, use_change: bool = False):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA).Purpose().Coin().Account(0)

    if use_change:
        # m/44'/501'/0'/0'
        ctx = ctx.Change(Bip44Changes.CHAIN_EXT)
        label = "m/44'/501'/0'/0'"
    else:
        # m/44'/501'/0'
        label = "m/44'/501'/0'"

    priv_key = ctx.PrivateKey().Raw().ToBytes().hex()
    pub_key_bytes = ctx.PublicKey().RawCompressed().ToBytes()[1:]
    address = SolAddrEncoder.EncodeKey(pub_key_bytes)

    return label, address, priv_key

if __name__ == "__main__":
    mnemonic = input("Enter mnemonic:\n> ").strip()

    path1, addr1, priv1 = derive_solana_address(mnemonic, use_change=False)  # m/44'/501'/0'
    path2, addr2, priv2 = derive_solana_address(mnemonic, use_change=True)   # m/44'/501'/0'/0'

    print(f"\n🔹 Address from {path1}")
    print(f"📬 Address: {addr1}")
    print(f"🔐 Private Key: {priv1}")

    print(f"\n🔹 Address from {path2}")
    print(f"📬 Address: {addr2}")
    print(f"🔐 Private Key: {priv2}")
