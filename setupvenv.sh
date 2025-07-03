#!/bin/bash
echo "📦 Creating virtual environment..."
python3 -m venv venv

echo "🔗 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ venv setup complete. You can now run: source venv/bin/activate"
