#!/bin/bash
# Quick start script for Legal AI Backend

echo "🚀 Starting Legal AI Backend..."

# Activate virtual environment
source .venv/bin/activate

# Check if .env is configured
if grep -q "sk-your-claude-key-here" .env; then
    echo "⚠️ Please configure your Claude API key in .env file"
    echo "Edit .env and replace 'sk-your-claude-key-here' with your actual API key"
    exit 1
fi

# Start the API server
echo "Starting API server on http://localhost:5000"
python3 api_server.py
