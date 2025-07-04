from flask import Flask, request, jsonify, render_template
from blockchain import (
    load_blockchain, save_blockchain, calculate_block_hash,
    get_latest_eth_timestamp, add_block as add_block_to_chain
)
from eth_account.messages import encode_defunct
from eth_account import Account
from datetime import datetime
import os
import pytz

# === Use same folder as script ===
script_dir = os.path.dirname(os.path.abspath(__file__))
timechain_dir = script_dir
AUDIT_LOG_PATH = os.path.join(timechain_dir, "auditiplog.txt")
os.makedirs(timechain_dir, exist_ok=True)

# === Flask app ===
app = Flask(__name__, template_folder="templates")

def log_visitor_ip():
    ip = request.headers.get('X-Real-IP', request.remote_addr)
    sydney_tz = pytz.timezone("Australia/Sydney")
    now = datetime.now(sydney_tz).strftime("%Y-%m-%d %H:%M:%S %Z")  # Sydney local time
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
        block = add_block_to_chain(message, signature, recovered_address)
        return jsonify(block)
    except Exception as e:
        return jsonify({"error": f"Failed to add block: {str(e)}"}), 500

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
