#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "Project directory: $PROJECT_DIR"
echo "Backend directory: $BACKEND_DIR"
echo "Frontend directory: $FRONTEND_DIR"

# Stop any existing processes on these ports
echo "Stopping any servers running on ports 8080 and 3002..."
lsof -ti:8080 | xargs kill -9 2>/dev/null
lsof -ti:3002 | xargs kill -9 2>/dev/null

# Set up Python environment
echo "Setting up Python environment..."
if [ -d "$BACKEND_DIR/venv" ]; then
  echo "Using existing virtual environment..."
  source "$BACKEND_DIR/venv/bin/activate"
else
  echo "Creating new virtual environment..."
  cd "$BACKEND_DIR"
  python3 -m venv venv
  source "$BACKEND_DIR/venv/bin/activate"
  python3 -m pip install --upgrade pip
  python3 -m pip install -r requirements.txt
fi

# Start backend server
echo "Starting backend server on port 8080..."
cd "$PROJECT_DIR"
python3 "$PROJECT_DIR/fix_api.py" &
backend_pid=$!

# Wait for backend to start
sleep 2
echo "Backend started with PID $backend_pid"

# Start frontend server
echo "Starting frontend server on port 3002..."
cd "$FRONTEND_DIR"
export PATH="$PATH:./node_modules/.bin"
npm start &
frontend_pid=$!

echo "Frontend started with PID $frontend_pid"
echo "Frontend: http://localhost:3002"
echo "Backend: http://localhost:8080"
echo "Health check: http://localhost:8080/api/health"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to press Ctrl+C
trap "kill $backend_pid $frontend_pid 2>/dev/null" INT
wait 