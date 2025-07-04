# -*- coding: utf-8 -*-
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
import re

# === Use same folder as script ===
script_dir = os.path.dirname(os.path.abspath(__file__))
timechain_dir = script_dir
AUDIT_LOG_PATH = os.path.join(timechain_dir, "auditiplog.txt")
os.makedirs(timechain_dir, exist_ok=True)

# === Flask app ===
app = Flask(__name__, template_folder="templates")

def parse_user_agent(ua):
    ua = ua.lower()
    platform = "Unknown"
    browser = "Unknown"
    version = ""

    if "windows" in ua:
        platform = "Windows"
    elif "iphone" in ua:
        platform = "iPhone"
    elif "ipad" in ua:
        platform = "iPad"
    elif "android" in ua:
        platform = "Android"
    elif "mac os x" in ua:
        platform = "Mac"

    # Common browsers
    match = re.search(r"(chrome|firefox|safari|edg|opera)[/\s]?([\d\.]+)", ua)
    if match:
        b, v = match.groups()
        browser = {
            "chrome": "Chrome",
            "firefox": "Firefox",
            "safari": "Safari",
            "edg": "Edge",
            "opera": "Opera"
        }.get(b, b.capitalize())
        version = v

    return platform, browser, version

def log_visitor_ip():
    ip = request.headers.get('X-Real-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown')
    platform, browser, version = parse_user_agent(user_agent)

    sydney_tz = pytz.timezone("Australia/Sydney")
    now = datetime.now(sydney_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    log_entry = f"{now} - {ip} - {platform} - {browser} {version}\n"

    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
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
        if block["index"] != i:
            messages.append(f"❌ Block {i}: Incorrect index")
            errors += 1

        if i > 0 and block["previous_hash"] != chain[i - 1]["hash"]:
            messages.append(f"❌ Block {i}: Previous hash mismatch")
            errors += 1

        if calculate_block_hash(block) != block["hash"]:
            messages.append(f"❌ Block {i}: Hash mismatch")
            errors += 1

    if errors == 0:
        messages.append("✅ All blocks are valid and consistent.")

    return jsonify({"errors": errors, "messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
