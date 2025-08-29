#!/bin/bash

# SmartProBono Standalone App Startup Script
# This script starts the advanced standalone app in the background

echo "🚀 Starting SmartProBono Standalone App..."

# Stop any existing app on port 8081
echo "1. Stopping any existing app on port 8081..."
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
sleep 2

# Activate virtual environment
echo "2. Activating virtual environment..."
source venv/bin/activate

# Start the standalone app in background
echo "3. Starting standalone app..."
python3 app_standalone.py > app.log 2>&1 &
APP_PID=$!

# Wait for app to start
echo "4. Waiting for app to start..."
sleep 3

# Test the app
echo "5. Testing app health..."
if curl -s http://localhost:8081/api/health > /dev/null; then
    echo "✅ SmartProBono Standalone App is running!"
    echo "   • Health: http://localhost:8081/api/health"
    echo "   • Legal Chat: http://localhost:8081/api/legal/chat"
    echo "   • Beta Signup: http://localhost:8081/api/beta/signup"
    echo "   • Feedback: http://localhost:8081/api/feedback"
    echo "   • Process ID: $APP_PID"
    echo "   • Logs: tail -f app.log"
    echo ""
    echo "🎯 Advanced Features Available:"
    echo "   • Legal Chat with task types (chat, research, draft)"
    echo "   • Document Analysis and Generation"
    echo "   • Research-based responses"
    echo "   • Template generation"
else
    echo "❌ Failed to start app. Check app.log for errors."
    exit 1
fi
