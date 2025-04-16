#!/bin/bash

# Start the SmartProBono application

echo "Starting SmartProBono application..."

# Define the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Check if the frontend build exists, if not, build it
if [ ! -d "$FRONTEND_DIR/build" ]; then
  echo "Building frontend..."
  cd "$FRONTEND_DIR" && npm run build
  if [ $? -ne 0 ]; then
    echo "Error: Frontend build failed"
    exit 1
  fi
  echo "Frontend build completed successfully"
fi

# Start the backend server
echo "Starting backend server..."
cd "$BACKEND_DIR"

# Check if restart_server.sh exists and is executable
if [ -f "./restart_server.sh" ] && [ -x "./restart_server.sh" ]; then
  ./restart_server.sh
else
  # Fall back to starting the app directly
  python3 app.py
fi

# Note: In a production environment, you might want to use PM2 or similar tools
# to properly manage the Node and Python processes. 