import os
import json

# Set paths
json_file_path = 'blockchain.json'       # Make sure this file exists
output_folder = 'txt_blocks'             # Folder to store .txt files

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the blockchain JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    blockchain = json.load(f)

# Process each block
for block in blockchain:
    index = block.get('index', 'unknown')
    message = block.get('message', '')

    # Normalize line breaks
    cleaned_message = message.replace('\\n', '\n').strip()

    # Write to a .txt file
    file_name = f"block_{index}.txt"
    file_path = os.path.join(output_folder, file_name)
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(cleaned_message)

print(f"✅ Converted {len(blockchain)} blocks to {output_folder}/block_*.txt")
