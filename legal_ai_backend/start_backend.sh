#!/bin/bash
# Legal AI Backend Startup Script

echo "🚀 Starting Legal AI Backend..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if vector store exists
if [ ! -d "../vectorstore/chroma_data" ]; then
    echo "Creating vector store directory..."
    mkdir -p ../vectorstore/chroma_data
fi

# Seed case law data (if not already done)
if [ ! -f "../vectorstore/chroma_data/.seeded" ]; then
    echo "Seeding case law data..."
    python ../scripts/seed_harvard_cases.py
    touch ../vectorstore/chroma_data/.seeded
fi

# Start the API server
echo "Starting API server on port 5000..."
python api_server.py
