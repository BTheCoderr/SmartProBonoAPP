#!/bin/bash

# Easy script to stop both backend and frontend servers

echo "🛑 Stopping SmartProBono AI Servers..."
echo ""

# Stop backend
if lsof -i :3001 &> /dev/null; then
    pkill -f "python.*combined_server.py"
    echo "✅ Backend stopped"
else
    echo "⚠️  Backend was not running"
fi

# Stop frontend
if lsof -i :3002 &> /dev/null; then
    pkill -f "npm start"
    echo "✅ Frontend stopped"
else
    echo "⚠️  Frontend was not running"
fi

echo ""
echo "✅ All servers stopped"
echo ""
echo "To start again: ./start_ai_servers.sh"
echo ""

