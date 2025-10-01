#!/bin/bash

# SmartProBono System Startup Script
# This script starts both the backend and frontend servers

echo "🚀 Starting SmartProBono System..."
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "Run: python3 -m venv venv && source venv/bin/activate && pip install flask flask-cors requests sqlalchemy python-dotenv PyPDF2 reportlab"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check Supabase configuration
echo "🔄 Checking Supabase configuration..."
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
    echo "⚠️ Supabase environment variables not set. Using defaults."
    echo "   To set custom values: export SUPABASE_URL=your_url && export SUPABASE_KEY=your_key"
else
    echo "✅ Supabase configuration found"
fi

# Start backend server
echo "🔄 Starting existing SmartProBono system..."
cd backend
python combined_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:3001/api/health > /dev/null; then
    echo "✅ Backend server is running on http://localhost:3001"
else
    echo "❌ Backend server failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend server (if Node.js is available)
if command -v npm &> /dev/null; then
    echo "🔄 Starting frontend server..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Frontend server is starting on http://localhost:3000"
else
    echo "⚠️ Node.js not found. Frontend server not started."
    echo "To start frontend manually: cd frontend && npm start"
fi

echo ""
echo "🎉 SmartProBono System Started Successfully!"
echo "============================================="
echo "🌐 Backend API: http://localhost:3001"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Health Check: http://localhost:3001/api/health"
echo ""
echo "📋 Available Endpoints:"
echo "  • POST /api/contact/submit - Contact form"
echo "  • POST /api/scanner/analyze - Document analysis"
echo "  • POST /api/generator/create - Document generation"
echo "  • GET /api/generator/templates - Document templates"
echo "  • GET /api/v1/crm/clients - CRM clients"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
