#!/bin/bash

# SmartProBono MVP - Stop Script
echo "🛑 Stopping SmartProBono MVP services..."

# Stop backend
BACKEND_PID=$(lsof -ti:8081)
if [ -n "$BACKEND_PID" ]; then
    kill -9 $BACKEND_PID
    echo "✅ Backend stopped (PID $BACKEND_PID)"
else
    echo "ℹ️  Backend not running on port 8081"
fi

# Stop frontend
FRONTEND_PID=$(lsof -ti:3002)
if [ -n "$FRONTEND_PID" ]; then
    kill -9 $FRONTEND_PID
    echo "✅ Frontend stopped (PID $FRONTEND_PID)"
else
    echo "ℹ️  Frontend not running on port 3002"
fi

# Clean up log files
rm -f backend.log frontend.log

echo "🎉 SmartProBono MVP services stopped"
