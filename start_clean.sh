#!/bin/bash

echo "🚀 Starting SmartProBono System (Clean)"
echo "========================================"

# Kill any existing processes
echo "Cleaning up old processes..."
pkill -f "combined_server.py" 2>/dev/null
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:8765 | xargs kill -9 2>/dev/null
lsof -ti:3002 | xargs kill -9 2>/dev/null

sleep 3

# Start backend
echo "Starting backend server..."
cd "$(dirname "$0")/backend"
source ../venv/bin/activate
python combined_server.py > /tmp/smartprobono_server.log 2>&1 &
BACKEND_PID=$!

sleep 5

# Check if server started
if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "✅ Backend server started successfully on port 3001"
    echo "📋 PID: $BACKEND_PID"
else
    echo "❌ Backend server failed to start"
    echo "Check logs: tail -f /tmp/smartprobono_server.log"
    exit 1
fi

# Check multi-agent system
if curl -s http://localhost:3001/api/multi-agent/status > /dev/null 2>&1; then
    echo "✅ Multi-Agent system operational"
else
    echo "⚠️ Multi-Agent system not responding"
fi

echo ""
echo "🎉 System Started!"
echo "===================="
echo "Backend: http://localhost:3001"
echo "Health: http://localhost:3001/api/health"
echo "Multi-Agent: http://localhost:3001/api/multi-agent/status"
echo "Logs: tail -f /tmp/smartprobono_server.log"
echo ""
echo "To run tests: python tests/test_complete_system.py"
echo "To stop: pkill -f combined_server.py"

