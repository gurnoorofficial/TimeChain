from flask import Flask, request, jsonify, render_template
from blockchain import (
    load_blockchain, save_blockchain, calculate_block_hash,
    get_latest_eth_timestamp
)
from eth_account.messages import encode_defunct
from eth_account import Account
from datetime import datetime

app = Flask(__name__, template_folder="templates")

AUDIT_LOG_PATH = "/root/auditiplog"

def log_visitor_ip():
    ip = request.headers.get('X-Real-IP', request.remote_addr)
    now = datetime.utcnow().isoformat()
    log_entry = f"{now} - {ip}\n"
    try:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️ Failed to write audit log: {e}")

@app.route("/")
def index():
    log_visitor_ip()
    return render_template("index.html")

@app.route("/chain", methods=["GET"])
def get_chain():
    log_visitor_ip()
    try:
        return jsonify(load_blockchain())
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

@app.route("/add_block", methods=["POST"])
def add_block():
    log_visitor_ip()
    data = request.get_json()
    if not data or "message" not in data or "signature" not in data:
        return jsonify({"error": "Missing message or signature"}), 400

    message = data["message"].strip()
    signature = data["signature"].strip()

    try:
        encoded_msg = encode_defunct(text=message)
        recovered_address = Account.recover_message(encoded_msg, signature=signature).lower()
    except Exception as e:
        return jsonify({"error": "Invalid signature", "details": str(e)}), 400

    try:
        chain = load_blockchain()
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

    if len(chain) >= 10:  # ⬅️ Updated block limit
        return jsonify({"error": "Chain has reached its limit (10 blocks)"}), 403

    try:
        timestamp, eth_block_number = get_latest_eth_timestamp()
    except Exception as e:
        return jsonify({"error": "Ethereum timestamp fetch failed", "details": str(e)}), 500

    previous_hash = chain[-1]["hash"] if chain else "0" * 64

    block_data = {
        "index": len(chain),
        "message": message,
        "eth_address": recovered_address,
        "signature": signature,
        "timestamp": timestamp,
        "eth_block_number": eth_block_number,
        "previous_hash": previous_hash,
    }

    block_data["hash"] = calculate_block_hash(block_data)
    chain.append(block_data)

    try:
        save_blockchain(chain)
    except Exception as e:
        return jsonify({"error": f"Failed to save block: {str(e)}"}), 500

    return jsonify(block_data)

@app.route("/verify_chain", methods=["GET"])
def verify_chain():
    log_visitor_ip()
    try:
        chain = load_blockchain()
    except Exception as e:
        return jsonify({"error": f"Failed to load blockchain: {str(e)}"}), 500

    if not chain:
        return jsonify({"error": "Blockchain is empty"}), 400

    errors = 0
    messages = []

    for i, block in enumerate(chain):
        index = i
        if block["index"] != index:
            messages.append(f"❌ Block {index}: Incorrect index")
            errors += 1

        if i > 0 and block["previous_hash"] != chain[i - 1]["hash"]:
            messages.append(f"❌ Block {index}: Previous hash mismatch")
            errors += 1

        if calculate_block_hash(block) != block["hash"]:
            messages.append(f"❌ Block {index}: Hash mismatch")
            errors += 1

    if errors == 0:
        messages.append("✅ All blocks are valid and consistent.")

    return jsonify({"errors": errors, "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
