#!/bin/bash

# SmartProBono MVP Startup Script
# This script starts the complete MVP system

echo "🚀 Starting SmartProBono MVP..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "fix_api.py" ]; then
    echo "❌ Error: Please run this script from the SmartProBono root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Function to kill processes on specific ports
kill_port() {
    local port=$1
    echo "🔄 Stopping any existing processes on port $port..."
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 2
}

# Stop any existing processes on our ports
echo "🔄 Cleaning up existing processes..."
kill_port 8081
kill_port 3002

# Wait a moment for cleanup
sleep 3

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not found. Please run 'cd frontend && npm install' first."
    exit 1
fi

# Activate virtual environment and install dependencies
echo "🐍 Setting up Python environment..."
source venv/bin/activate

# Install required Python packages
pip install flask flask-cors python-dotenv > /dev/null 2>&1

# Load email configuration
echo "📧 Loading email configuration..."
source load_email_config.sh

# Start backend
echo "🔧 Starting backend API on port 8081..."
export PORT=8081
python fix_api.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend health
if curl -s http://localhost:8081/api/health > /dev/null; then
    echo "✅ Backend is running and healthy"
else
    echo "❌ Backend failed to start properly"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "⚛️  Starting frontend on port 3002..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Test frontend
if curl -s http://localhost:3002 > /dev/null; then
    echo "✅ Frontend is running and accessible"
else
    echo "❌ Frontend failed to start properly"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

# Display success message
echo ""
echo "🎉 SmartProBono MVP is now running!"
echo "=================================="
echo "📱 Frontend: http://localhost:3002"
echo "🔧 Backend API: http://localhost:8081"
echo "❤️  Health Check: http://localhost:8081/api/health"
echo ""
echo "🔗 Key Features Available:"
echo "  • Beta Signup: http://localhost:3002/"
echo "  • Legal AI Chat: http://localhost:3002/legal-chat"
echo "  • Document Management: http://localhost:3002/documents"
echo "  • Expert Help: http://localhost:3002/expert-help"
echo ""
echo "📊 API Endpoints:"
echo "  • POST /api/beta/signup - Beta program signup"
echo "  • POST /api/legal/chat - AI legal chat"
echo "  • GET /api/documents/history - Document history"
echo "  • GET /api/documents/templates - Document templates"
echo "  • POST /api/feedback - User feedback"
echo ""
echo "🛑 To stop the MVP, press Ctrl+C or run: ./stop_mvp.sh"
echo ""

# Keep script running and show logs
echo "📋 System Status:"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping SmartProBono MVP..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
