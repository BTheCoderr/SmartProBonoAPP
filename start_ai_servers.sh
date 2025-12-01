#!/bin/bash

# Easy script to start both backend and frontend servers

echo "🚀 Starting SmartProBono AI Servers..."
echo ""

# Check if already running
if lsof -i :3001 &> /dev/null; then
    echo "⚠️  Backend already running on port 3001"
else
    echo "Starting backend server..."
    cd backend
    source ../venv/bin/activate
    nohup python combined_server.py > ../backend.log 2>&1 &
    echo "✅ Backend started (logs: backend.log)"
    cd ..
fi

if lsof -i :3002 &> /dev/null; then
    echo "⚠️  Frontend already running on port 3002"
else
    echo "Starting frontend server..."
    cd frontend
    nohup npm start > ../frontend.log 2>&1 &
    echo "✅ Frontend started (logs: frontend.log)"
    cd ..
fi

echo ""
echo "⏳ Waiting for servers to start..."
sleep 5

# Check health
if curl -s http://localhost:3001/api/health &> /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend may need more time to start"
fi

echo ""
echo "🎉 Servers are starting!"
echo ""
echo "Access your app:"
echo "  Frontend:    http://localhost:3002"
echo "  Backend API: http://localhost:3001"
echo ""
echo "View logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "Check status: ./diagnose_ai.sh"
echo "Stop servers: ./stop_ai_servers.sh"
echo ""

