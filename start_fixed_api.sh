#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if Python virtual environment exists
if [ -d "$PROJECT_DIR/backend/venv" ]; then
  echo "Using existing virtual environment..."
  source "$PROJECT_DIR/backend/venv/bin/activate"
else
  echo "Creating new virtual environment..."
  cd "$PROJECT_DIR/backend"
  python3 -m venv venv
  source "$PROJECT_DIR/backend/venv/bin/activate"
  python3 -m pip install --upgrade pip
  python3 -m pip install flask flask-cors
fi

# Start the fixed API
echo "Starting fixed API server on port 8080..."
cd "$PROJECT_DIR"
python3 "$PROJECT_DIR/fix_api.py"

# Note: The script will keep running until Ctrl+C is pressed 