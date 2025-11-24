# -*- coding: utf-8 -*-
from bip_utils import (
    Bip39SeedGenerator,
    Bip32Slip10Secp256k1,
    Secp256k1PublicKey,
    Secp256k1PrivateKey,
    EthAddr,
    P2PKHAddr,
    WifEncoder
)

# ⭐⭐ EDIT THESE ⭐⭐
ETH_DERIVATION_PATH = "m/44'/60'/0'/0/0"
BTC_DERIVATION_PATH = "m/44'/0'/0'/0/0"


def normalize(path: str) -> str:
    path = path.strip()
    if not path.startswith("m"):
        path = "m/" + path
    return path


# ---------------- ETH ----------------

def derive_eth_from_path(seed_bytes: bytes, path: str):
    bip32 = Bip32Slip10Secp256k1.FromSeed(seed_bytes)
    node = bip32.DerivePath(path)

    priv_hex = node.PrivateKey().Raw().ToHex()
    pub_hex = node.PublicKey().RawCompressed().ToHex()

    return priv_hex, pub_hex, node.PublicKey()


def eth_addr_from_public(pub_obj):
    uncompressed = pub_obj.RawUncompressed().ToBytes()
    secp_key = Secp256k1PublicKey.FromBytes(uncompressed)
    return EthAddr.EncodeKey(secp_key)


# ---------------- BTC ----------------

def derive_btc_from_path(seed_bytes: bytes, path: str):
    bip32 = Bip32Slip10Secp256k1.FromSeed(seed_bytes)
    node = bip32.DerivePath(path)

    # RAW private key
    priv_bytes = node.PrivateKey().Raw().ToBytes()
    priv_hex = node.PrivateKey().Raw().ToHex()

    # ⭐ Correct WIF for latest bip_utils
    priv_key_obj = Secp256k1PrivateKey.FromBytes(priv_bytes)
    wif = WifEncoder.Encode(priv_key_obj, net_ver=b"\x80")  # BTC mainnet

    pub_hex = node.PublicKey().RawCompressed().ToHex()

    # BTC P2PKH (legacy 1xxxx)
    btc_addr = P2PKHAddr.EncodeKey(
        Secp256k1PublicKey.FromBytes(
            node.PublicKey().RawCompressed().ToBytes()
        ),
        net_ver=b"\x00"
    )

    return priv_hex, wif, pub_hex, btc_addr


# ---------------- MAIN ----------------

def main():
    print("=== CUSTOM BTC & ETH DERIVATION TOOL ===\n")

    mnemonic = input("Enter 12/24-word BIP39 mnemonic: ").strip()

    try:
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    except Exception as e:
        print("❌ Invalid mnemonic:", e)
        return

    # -------- ETH --------
    eth_path = normalize(ETH_DERIVATION_PATH)
    eth_priv, eth_pub, eth_pub_obj = derive_eth_from_path(seed_bytes, eth_path)

    print("\n=== Ethereum (Custom Path) ===")
    print("Path        :", eth_path)

    eth_priv_out = "0x" + eth_priv if not eth_priv.startswith("0x") else eth_priv
    print("Private Key :", eth_priv_out)

    print("Public Key  :", eth_pub)

    eth_addr = eth_addr_from_public(eth_pub_obj)
    eth_addr = "0x" + eth_addr if not eth_addr.startswith("0x") else eth_addr
    print("ETH Address :", eth_addr)

    # -------- BTC --------
    btc_path = normalize(BTC_DERIVATION_PATH)
    btc_priv_hex, btc_wif, btc_pub_hex, btc_addr = derive_btc_from_path(seed_bytes, btc_path)

    print("\n=== Bitcoin (Custom Path) ===")
    print("Path             :", btc_path)
    print("Private Key (WIF):", btc_wif)
    print("Public Key       :", btc_pub_hex)
    print("BTC Address      :", btc_addr)

    print("\nDone!")


if __name__ == "__main__":
    main()
