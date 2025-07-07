import hashlib
import os

# Known stamped hash you're trying to match
STAMPED_HASH = "7a0f4ad41fa9c808dea47f1afb8dc3f79aaaebb29e65aa4721c244b159defca1"

def normalize_file(source_path):
    with open(source_path, "r", encoding="utf-8", errors="ignore") as src:
        content = src.read()

    # Normalize line endings and whitespace
    content = content.replace('\r\n', '\n').replace('\r', '\n').strip() + '\n'

    # Build output path automatically
    base, ext = os.path.splitext(source_path)
    output_path = base + "_normalized" + ext

    with open(output_path, "w", encoding="utf-8", newline='\n') as out:
        out.write(content)

    return output_path

def sha256_of_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_conversion():
    input_path = input("📥 Enter path to file to normalize:\n> ").strip()

    if not os.path.exists(input_path):
        print("❌ File not found.")
        return

    output_path = normalize_file(input_path)
    new_hash = sha256_of_file(output_path)

    print(f"\n🧼 Normalized file saved as: {output_path}")
    print(f"🔐 SHA256 Hash: {new_hash}")

    if new_hash == STAMPED_HASH:
        print("✅ Perfect match! File now identical to your original stamped version.")
    else:
        print("❌ Still not matching. Check content carefully (invisible whitespace or line count may differ).")

if __name__ == "__main__":
    run_conversion()
