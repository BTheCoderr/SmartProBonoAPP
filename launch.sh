#!/bin/bash

# Stop running processes on these ports if they exist
echo "Stopping any servers running on ports 8080 and 3002..."
lsof -ti:8080 | xargs kill -9 2>/dev/null
lsof -ti:3002 | xargs kill -9 2>/dev/null

# Start backend server
echo "Starting backend server on port 8080..."
cd "$(dirname "$0")/backend"
python backend/app.py &
backend_pid=$!

# Wait for backend to start
sleep 2
echo "Backend started with PID $backend_pid"

# Start frontend server
echo "Starting frontend server on port 3002..."
cd "$(dirname "$0")/frontend"
PORT=3002 npm start &
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