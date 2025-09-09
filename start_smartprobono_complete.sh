#!/bin/bash

# SmartProBono Complete Startup Script
# This script starts both backend and frontend in one terminal

echo "🚀 Starting SmartProBono Complete System..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} ✅ $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')]${NC} ⚠️  $1"
}

print_error() {
    echo -e "${RED}[$(date +'%H:%M:%S')]${NC} ❌ $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the SmartProBono-main directory"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Set environment variables
export RESEND_API_KEY=re_N7YNzBXp_HyNzVsWjuLNqxqUQr8oxaxvf
export FLASK_ENV=development

# Check if ports are available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port $port is already in use"
        return 1
    else
        print_success "Port $port is available"
        return 0
    fi
}

# Kill existing processes on our ports
print_status "Checking for existing processes..."
pkill -f "combined_server.py" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true
sleep 2

# Start backend server
print_status "Starting backend server..."
cd backend
python combined_server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
print_status "Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if curl -s http://localhost:3001/api/health > /dev/null; then
    print_success "Backend server started successfully on port 3001"
else
    print_error "Backend server failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend server
print_status "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
print_status "Waiting for frontend to initialize..."
sleep 5

# Check if frontend is running
if curl -s http://localhost:3002 > /dev/null; then
    print_success "Frontend server started successfully on port 3002"
else
    print_warning "Frontend may still be starting up..."
    sleep 3
    if curl -s http://localhost:3002 > /dev/null; then
        print_success "Frontend server is now running on port 3002"
    else
        print_error "Frontend server failed to start"
        kill $BACKEND_PID 2>/dev/null || true
        kill $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
fi

# Display system status
echo ""
echo "🎉 SmartProBono System is Running!"
echo "=================================="
echo -e "${GREEN}✅ Backend API:${NC} http://localhost:3001"
echo -e "${GREEN}✅ Frontend App:${NC} http://localhost:3002"
echo ""
echo "🔧 Available Services:"
echo "   • Document Scanner (with safety features)"
echo "   • PDF Generator"
echo "   • AI Legal Chat"
echo "   • Contact Form"
echo "   • Enhanced Health Monitoring"
echo ""
echo "🛡️ Safety Features Active:"
echo "   • UPL Prevention"
echo "   • Escalation Detection"
echo "   • Legal Disclaimers"
echo "   • Response Sanitization"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    print_status "Shutting down SmartProBono system..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    print_success "System shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running and show status
print_status "System is running! Press Ctrl+C to stop all services"
echo ""

# Monitor system health
while true; do
    sleep 30
    
    # Check backend health
    if ! curl -s http://localhost:3001/api/health > /dev/null; then
        print_error "Backend server is not responding"
        break
    fi
    
    # Check frontend health
    if ! curl -s http://localhost:3002 > /dev/null; then
        print_error "Frontend server is not responding"
        break
    fi
    
    print_success "System health check passed"
done

# If we get here, something went wrong
print_error "System health check failed. Shutting down..."
cleanup
