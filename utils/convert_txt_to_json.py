import os
import json

def txt_to_json(txt_path):
    if not os.path.isfile(txt_path):
        print(f"❌ File not found: {txt_path}")
        return

    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    data = {
        "message": content
    }

    json_path = os.path.splitext(txt_path)[0] + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved JSON to: {json_path}")

if __name__ == "__main__":
    path = input("📄 Enter path to .txt file to convert to JSON: ").strip().strip('"').strip("'")
    txt_to_json(path)
