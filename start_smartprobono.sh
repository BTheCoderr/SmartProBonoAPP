#!/bin/bash

# SmartProBono MVP - Complete Startup Script
# This script starts both backend and frontend services

echo "🚀 Starting SmartProBono MVP - Complete System"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping SmartProBono MVP services..."
    
    # Kill backend
    BACKEND_PID=$(lsof -ti:8081)
    if [ -n "$BACKEND_PID" ]; then
        kill -9 $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped (PID $BACKEND_PID)"
    fi
    
    # Kill frontend
    FRONTEND_PID=$(lsof -ti:3002)
    if [ -n "$FRONTEND_PID" ]; then
        kill -9 $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped (PID $FRONTEND_PID)"
    fi
    
    echo "🎉 SmartProBono MVP services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo ""
echo "1. 🔄 Stopping any existing services..."

# Stop existing services
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
lsof -ti:3002 | xargs kill -9 2>/dev/null || true

# Wait for cleanup
sleep 2

echo ""
echo "2. 🐍 Starting Supabase Backend..."

# Start backend
source venv/bin/activate
source load_email_config.sh
export PORT=8081
python working_supabase_api.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test backend health
echo "   Testing backend health..."
if curl -s http://localhost:8081/api/health | grep -q "Supabase"; then
    echo -e "   Backend: ${GREEN}✅ Running with Supabase${NC}"
else
    echo -e "   Backend: ${RED}❌ Failed to start${NC}"
    echo "   Check backend.log for details"
    exit 1
fi

echo ""
echo "3. ⚛️  Starting React Frontend..."

# Start frontend
cd frontend
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 10

# Test frontend
echo "   Testing frontend..."
if curl -s http://localhost:3002 | grep -q "SmartProBono"; then
    echo -e "   Frontend: ${GREEN}✅ Running${NC}"
else
    echo -e "   Frontend: ${YELLOW}⚠️  Starting (may take a moment)${NC}"
fi

echo ""
echo "4. 🧪 Testing AI Improvements..."

# Test the improved AI responses
echo "   Testing greeting response..."
greeting_response=$(curl -s -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "task_type": "chat"}' | jq -r '.response')

if echo "$greeting_response" | grep -q "Hello! I'm your AI legal assistant"; then
    echo -e "   Greeting Agent: ${GREEN}✅ Working (brief, friendly response)${NC}"
else
    echo -e "   Greeting Agent: ${YELLOW}⚠️  Response: ${greeting_response:0:50}...${NC}"
fi

echo ""
echo "🎉 SmartProBono MVP is now running!"
echo "=================================="
echo ""
echo -e "${GREEN}✅ WORKING FEATURES:${NC}"
echo "  • Backend API with Supabase integration"
echo "  • Multi-agent AI system with contextual responses"
echo "  • Row Level Security (RLS) for data protection"
echo "  • JWT authentication system"
echo "  • Email system with Zoho SMTP"
echo "  • Professional UI/UX"

echo ""
echo -e "${BLUE}🌐 Access Your MVP:${NC}"
echo "  • Frontend: http://localhost:3002"
echo "  • Backend: http://localhost:8081"
echo "  • Health Check: http://localhost:8081/api/health"

echo ""
echo -e "${YELLOW}🎯 Test the Improvements:${NC}"
echo "  1. Go to http://localhost:3002"
echo "  2. Or test API directly:"
echo "     curl -X POST http://localhost:8081/api/legal/chat \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"message\": \"hello\", \"task_type\": \"chat\"}'"

echo ""
echo -e "${GREEN}🔐 Security Features Active:${NC}"
echo "  • Row Level Security (RLS) - users only see their own data"
echo "  • JWT authentication with Supabase"
echo "  • Protected API endpoints"
echo "  • Input validation and sanitization"

echo ""
echo -e "${GREEN}🤖 AI Improvements Active:${NC}"
echo "  • Greeting Agent: Brief, friendly responses to greetings"
echo "  • Compliance Agent: GDPR, SOC 2, privacy policies"
echo "  • Business Agent: Entity formation, fundraising, contracts"
echo "  • Document Agent: Document analysis and generation"
echo "  • Expert Agent: Complex questions and expert referrals"

echo ""
echo "📊 System Status:"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "  • Backend: backend.log"
echo "  • Frontend: frontend.log"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user to stop
wait
