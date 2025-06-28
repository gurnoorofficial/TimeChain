TimeChain – Ethereum-Powered Message Blockchain
TimeChain is a minimal blockchain system that lets anyone:

📝 Submit messages signed with Ethereum keys

🔐 Store them immutably and irreversibly on a custom chain

⏳ Anchor each block to a real Ethereum Mainnet block time

🧾 Enforce trustless, time-proof logging of statements

🚫 Prevent tampering, rewrites, or unauthorized inserts

Each message becomes part of a permanent public history — ideal for proof-of-existence, timestamping, declarations, or censorship-resistant records.

✅ Key Features
Ethereum Signature Verification
Every message must be signed with a valid Ethereum private key.

Immutable Message Ledger
Blocks cannot be altered once added — verified by Keccak-256 hashing.

Ethereum Time Anchoring
Each block fetches a real Ethereum Mainnet timestamp and block number.

Fixed Maximum Blocks
The chain accepts up to 10 blocks (configurable).

Lightweight & Local
No database required — messages are stored in blockchain.json.

🔐 Cryptographic Authorship, Forgery Resistance & Immutable Chain
TimeChain ensures message authenticity, immutability, and tamper-proof permanence:

Proves Ownership of Message
Each block requires a valid Ethereum signature. Only the real owner of the private key can submit a valid message — no impersonation possible.

Detects Duplicates & Tampering
Every block includes a Keccak-256 hash of its data. If any block is altered or copied dishonestly, verify_chain will catch it instantly.

Trustless & Auditable
There is no admin or manual approval. All verification is done by cryptography and chain logic. Anyone can audit it.

Dismisses Copy Attempts
Messages are signed and anchored to real Ethereum block times, preventing replay or forgery.

Time-Proof and Permanent
Each block is anchored to a real Ethereum Mainnet timestamp. Once written, it is forever bound to that moment — immutable and undeletable.

📦 Installation
Requirements
Python 3.10+

pip and venv for environment management

Setup on Windows
Open Command Prompt (Windows + R, then type cmd).

Change to a preferred drive (optional but recommended):

bash
Copy
cd /d D:\
Clone the repository:

bash
Copy
git clone https://github.com/gurnoorofficial/TimeChain.git
cd TimeChain
Create and activate a virtual environment:

nginx
Copy
python -m venv venv
venv\Scripts\activate
Install required dependencies:

nginx
Copy
pip install -r requirements.txt
🛠️ Available Utilities
After activating your virtual environment, you can use these scripts:

✍️ Sign Message (with timestamp)
Generates an Ethereum signature with the current UTC timestamp included.

bash
Copy
python utils/sign_message.py
Prompts:

Enter the message to sign

Enter your Ethereum private key (starts with 0x)

Outputs:

Ethereum address

Full message (with timestamp)

Signature (0x-prefixed)

🧾 Verify Signature Ownership
Checks if a signature matches the claimed Ethereum address and message.

bash
Copy
python utils/verify_local_hash.py
Prompts:

Enter the Ethereum address

Enter the message

Enter the signature

Outputs:

Validity confirmation or failure notice

🔎 Verify Blockchain File Integrity
Validates the entire blockchain.json by recalculating and comparing hashes.

bash
Copy
python utils/verify_local_hash.py
Prompts:

Paste the full path to your blockchain.json file (quotes optional)

Outputs:

Keccak hash for each block

Any inconsistencies or tampering alerts

🔄 Convert TXT to JSON (and vice versa)
Convert plain text message files into blockchain JSON format:

bash
Copy
python utils/convert_txt_to_json.py
Convert blockchain JSON blocks back to readable TXT:

bash
Copy
python utils/convert_json_to_txt.py
🚀 Starting the Application
Run the Flask app:

bash
Copy
python app.py
Open your browser and visit:
http://localhost:5000

🌐 Web Interface Routes
Route	Method	Description
/	GET	Frontend message UI
/chain	GET	View full blockchain data
/add_block	POST	Submit signed message (JSON)
/verify_chain	GET	Validate all blocks + hashes

📁 Project Structure
graphql
Copy
TimeChain/
├── app.py                # Flask API and frontend logic
├── blockchain.py         # Core blockchain functions (hashing, limits, Ethereum time)
├── blockchain.json       # Stored blockchain data (local)
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend HTML UI
├── utils/                # Utility scripts
│   ├── convert_txt_to_json.py
│   ├── convert_json_to_txt.py
│   ├── sign_message.py
│   └── verify_local_hash.py
└── venv/                 # Python virtual environment (excluded from git)
⚙️ Configuration
MAX_BLOCKS in blockchain.py controls maximum allowed blocks (default 10).

INFURA_URL holds your Ethereum Mainnet provider endpoint (replace with your own if needed).

📜 License
MIT License

👤 Author
Gurnoor Singh – https://github.com/gurnoorofficial

