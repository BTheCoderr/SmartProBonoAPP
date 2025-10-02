#!/bin/bash

# 🚀 SmartProBono Production Startup Script
# This script starts the SmartProBono system in production mode

echo "🚀 Starting SmartProBono Production Server..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r backend/requirements.txt

# Kill any existing servers
echo "🔄 Stopping existing servers..."
pkill -f combined_server 2>/dev/null || true
sleep 2

# Set production environment variables
export FLASK_ENV=production
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the server
echo "🌐 Starting SmartProBono server..."
echo "Server will be available at: http://localhost:3001"
echo "Press Ctrl+C to stop the server"
echo "=================================================="

# Run the server
python backend/combined_server.py

