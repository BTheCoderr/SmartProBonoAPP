#!/bin/bash

# Find and kill all processes running the Flask app
echo "Stopping any running Flask servers..."
pkill -f "python3 app.py" || true

# Wait a moment to ensure processes are terminated
sleep 2

# Check if port 5002 is still in use
if lsof -i:5002 > /dev/null; then
  echo "Port 5002 is still in use. Forcefully killing process..."
  lsof -i:5002 | awk 'NR>1 {print $2}' | xargs kill -9
  sleep 1
fi

# Start the Flask app
echo "Starting Flask server..."
cd "$(dirname "$0")"
python3 app.py 