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
lsof -ti:8010 | xargs kill -9 2>/dev/null || true

# Wait for cleanup
sleep 2

echo ""
echo "2. 🐍 Starting Backend..."

# Start backend
source venv/bin/activate
source load_email_config.sh
export PORT=8081
python advanced_multi_agent_api.py > backend.log 2>&1 &
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
echo "3. 🧠 Starting LangGraph Service..."

# Start LangGraph service
cd agent_service
pip install -r requirements.txt > ../langgraph_install.log 2>&1
cd ..

export SUPABASE_URL="https://ewtcvsohdgkthuyajyyk.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="***REMOVED***"

# Advanced LangGraph features
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="SmartProBono-Advanced"
export ENABLE_HUMAN_REVIEW="true"
export ENABLE_PARALLEL_EXECUTION="true"
export USE_SUPABASE_CHECKPOINTS="false"  # Use memory checkpoints for now

# Using Ollama local LLM - no API key needed!
uvicorn agent_service.main:app --reload --port 8010 > langgraph.log 2>&1 &
LANGGRAPH_PID=$!

# Wait for LangGraph to start
sleep 5

# Test LangGraph health
echo "   Testing LangGraph health..."
if curl -s http://localhost:8010/health | grep -q "ok"; then
    echo -e "   LangGraph: ${GREEN}✅ Running${NC}"
else
    echo -e "   LangGraph: ${RED}❌ Failed to start${NC}"
    echo "   Check langgraph.log for details"
    echo "   Make sure Ollama is running: ollama serve"
fi

echo ""
echo "4. ⚛️  Starting React Frontend..."

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
echo "  • LangGraph orchestration service for case intake"
echo "  • Row Level Security (RLS) for data protection"
echo "  • JWT authentication system"
echo "  • Email system with Zoho SMTP"
echo "  • Professional UI/UX"

echo ""
echo -e "${BLUE}🌐 Access Your MVP:${NC}"
echo "  • Frontend: http://localhost:3002"
echo "  • Backend: http://localhost:8081"
echo "  • LangGraph: http://localhost:8010"
echo "  • Health Check: http://localhost:8081/api/health"
echo "  • LangGraph Health: http://localhost:8010/health"

echo ""
echo -e "${YELLOW}🎯 Test the Advanced Features:${NC}"
echo "  1. Go to http://localhost:3002"
echo "  2. Test Simple LangGraph intake:"
echo "     curl -X POST http://localhost:8010/intake/run \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"user_id\": null, \"full_text\": \"I need help with a landlord dispute\", \"meta\": {}}'"
echo "  3. Test Advanced Multi-Agent intake:"
echo "     curl -X POST http://localhost:8010/intake/advanced \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"user_id\": null, \"full_text\": \"I was arrested for shoplifting\", \"meta\": {}}'"
echo "  4. Test Graph Info:"
echo "     curl http://localhost:8010/graph/info"
echo "  5. Test Human Reviews:"
echo "     curl http://localhost:8010/human-reviews/pending"
echo "  6. Run Integration Test:"
echo "     python3.13 test_advanced_integration.py"

echo ""
echo "📊 System Status:"
echo "Backend PID: $BACKEND_PID"
echo "LangGraph PID: $LANGGRAPH_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "  • Backend: backend.log"
echo "  • LangGraph: langgraph.log"
echo "  • LangGraph Install: langgraph_install.log"
echo "  • Frontend: frontend.log"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user to stop
wait
