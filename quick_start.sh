#!/bin/bash

# Quick Start Script for IDE Development
# Minimal resource usage to prevent freezing

echo "⚡ SmartProBono Quick Start (IDE-Friendly)"
echo "========================================="

# Kill existing processes
pkill -f "advanced_multi_agent_api.py" 2>/dev/null || true
pkill -f "uvicorn.*agent_service" 2>/dev/null || true
sleep 1

# Start only the backend with minimal resources
echo "🚀 Starting backend only..."
source venv/bin/activate

# Start backend in background with minimal logging
python advanced_multi_agent_api.py > /dev/null 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend started (PID: $BACKEND_PID)"
    echo "🌐 Backend: http://localhost:8081"
    echo "🔍 Health: http://localhost:8081/api/health"
    echo ""
    echo "💡 Tips to prevent freezing:"
    echo "   • Use lightweight models (qwen2.5:0.5b)"
    echo "   • Keep IDE memory usage low"
    echo "   • Close unnecessary browser tabs"
    echo "   • Use the performance monitor: python3 monitor_performance.py"
    echo ""
    echo "🛑 To stop: kill $BACKEND_PID"
else
    echo "❌ Backend failed to start"
    exit 1
fi
