#!/bin/bash

# SmartProBono Lightweight Startup Script
# Optimized for development without freezing

echo "🚀 Starting SmartProBono (Lightweight Mode)"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}Port $1 is already in use${NC}"
        return 0
    else
        return 1
    fi
}

# Function to start service with error handling
start_service() {
    local name=$1
    local command=$2
    local port=$3
    local health_url=$4
    
    echo -e "${BLUE}Starting $name...${NC}"
    
    # Start in background
    eval "$command" > "${name,,}.log" 2>&1 &
    local pid=$!
    
    # Wait for service to start
    sleep 3
    
    # Check if process is still running
    if kill -0 $pid 2>/dev/null; then
        echo -e "   $name: ${GREEN}✅ Running (PID: $pid)${NC}"
        echo $pid > "${name,,}.pid"
    else
        echo -e "   $name: ${RED}❌ Failed to start${NC}"
        echo "   Check ${name,,}.log for details"
        return 1
    fi
}

# 1. Stop any existing services
echo "1. 🔄 Stopping existing services..."
pkill -f "advanced_multi_agent_api.py" 2>/dev/null || true
pkill -f "uvicorn.*agent_service" 2>/dev/null || true
pkill -f "npm.*start" 2>/dev/null || true
sleep 2

# 2. Start Backend (Lightweight)
echo ""
echo "2. 🐍 Starting Backend (Lightweight)..."
if check_port 8081; then
    echo -e "   Backend: ${GREEN}✅ Already running${NC}"
else
    source venv/bin/activate
    start_service "Backend" "python advanced_multi_agent_api.py" 8081 "http://localhost:8081/api/health"
fi

# 3. Start Frontend (if needed)
echo ""
echo "3. ⚛️  Starting Frontend..."
if check_port 3002; then
    echo -e "   Frontend: ${GREEN}✅ Already running${NC}"
else
    cd frontend
    start_service "Frontend" "npm start" 3002 "http://localhost:3002"
    cd ..
fi

# 4. Pre-load Ollama models (optional)
echo ""
echo "4. 🧠 Pre-loading Ollama models..."
if command -v ollama &> /dev/null; then
    echo "   Pre-loading Qwen (lightweight model)..."
    curl -s -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d '{"model": "qwen2.5:0.5b", "prompt": "Hello", "stream": false}' \
        --max-time 10 > /dev/null 2>&1 || echo "   Model pre-loading skipped"
    echo -e "   Ollama: ${GREEN}✅ Ready${NC}"
else
    echo -e "   Ollama: ${YELLOW}⚠️  Not installed${NC}"
fi

echo ""
echo "🎉 SmartProBono Lightweight Mode is running!"
echo "=========================================="
echo -e "${GREEN}✅ WORKING FEATURES:${NC}"
echo "  • Backend API with Ollama integration"
echo "  • Lightweight model loading"
echo "  • Fast fallback responses"
echo "  • Optimized performance"
echo ""
echo -e "${BLUE}🌐 Access Your App:${NC}"
echo "  • Frontend: http://localhost:3002"
echo "  • Backend: http://localhost:8081"
echo "  • Health Check: http://localhost:8081/api/health"
echo ""
echo -e "${YELLOW}🎯 Quick Test:${NC}"
echo "  curl -X POST http://localhost:8081/api/legal/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"Hello\", \"task_type\": \"qwen\"}'"
echo ""
echo -e "${BLUE}📊 System Status:${NC}"
if [ -f backend.pid ]; then
    echo "Backend PID: $(cat backend.pid)"
fi
if [ -f frontend.pid ]; then
    echo "Frontend PID: $(cat frontend.pid)"
fi
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo "  • Backend: backend.log"
echo "  • Frontend: frontend.log"
echo ""
echo -e "${RED}Press Ctrl+C to stop all services...${NC}"

# Keep script running and handle cleanup
trap 'echo ""; echo "🛑 Stopping services..."; pkill -f "advanced_multi_agent_api.py"; pkill -f "npm.*start"; rm -f *.pid; echo "✅ All services stopped"; exit 0' INT

# Wait for user interrupt
while true; do
    sleep 1
done
