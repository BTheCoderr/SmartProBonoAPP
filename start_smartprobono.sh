#!/bin/bash

# SmartProBono MVP - Complete Startup Script
echo "🚀 Starting SmartProBono MVP - Complete System"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "1. 🔄 Stopping any existing services..."

# Stop existing services
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
lsof -ti:3002 | xargs kill -9 2>/dev/null || true

# Wait for cleanup
sleep 2

echo ""
echo "2. 🐍 Starting Backend..."

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
if curl -s http://localhost:8081/api/health | grep -q "SmartProBono"; then
    echo -e "   Backend: ${GREEN}✅ Running${NC}"
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
