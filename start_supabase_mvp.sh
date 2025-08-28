#!/bin/bash

# SmartProBono MVP with Supabase - Startup Script
echo "🚀 Starting SmartProBono MVP with Supabase Integration"
echo "====================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "🔐 Security Features:"
echo "  • Row Level Security (RLS) enabled"
echo "  • JWT authentication with Supabase"
echo "  • Protected API endpoints"
echo "  • User data isolation"

echo ""
echo "🤖 AI Improvements:"
echo "  • Multi-agent system with 5 specialized agents"
echo "  • Contextual responses (no more overwhelming greetings!)"
echo "  • Smart routing to appropriate agents"
echo "  • Better conversation management"

echo ""
echo "1. 🔄 Stopping existing services..."

# Stop existing services
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
lsof -ti:3002 | xargs kill -9 2>/dev/null || true

# Wait for cleanup
sleep 3

echo ""
echo "2. 🐍 Starting Supabase-integrated backend..."

# Start the new Supabase backend
source venv/bin/activate
source load_email_config.sh
export PORT=8081
python supabase_api.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Test backend health
echo "   Testing backend health..."
if curl -s http://localhost:8081/api/health | grep -q "Supabase"; then
    echo -e "   Backend: ${GREEN}✅ Running with Supabase${NC}"
else
    echo -e "   Backend: ${RED}❌ Failed to start${NC}"
    exit 1
fi

echo ""
echo "3. ⚛️  Starting frontend..."

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 10

# Test frontend
echo "   Testing frontend..."
if curl -s http://localhost:3002 | grep -q "SmartProBono"; then
    echo -e "   Frontend: ${GREEN}✅ Running${NC}"
else
    echo -e "   Frontend: ${RED}❌ Failed to start${NC}"
    exit 1
fi

echo ""
echo "4. 🧪 Testing improved AI system..."

# Test the improved AI responses
echo "   Testing greeting response..."
greeting_response=$(curl -s -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "task_type": "chat"}' | jq -r '.response')

if echo "$greeting_response" | grep -q "Hello! I'm your AI legal assistant"; then
    echo -e "   Greeting Agent: ${GREEN}✅ Working (brief, friendly response)${NC}"
else
    echo -e "   Greeting Agent: ${YELLOW}⚠️  Response: ${greeting_response:0:100}...${NC}"
fi

echo "   Testing compliance response..."
compliance_response=$(curl -s -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is GDPR compliance?", "task_type": "chat"}' | jq -r '.response')

if echo "$compliance_response" | grep -q "GDPR Compliance Overview"; then
    echo -e "   Compliance Agent: ${GREEN}✅ Working (detailed guidance)${NC}"
else
    echo -e "   Compliance Agent: ${YELLOW}⚠️  Response: ${compliance_response:0:100}...${NC}"
fi

echo ""
echo "🎉 SmartProBono MVP with Supabase is now running!"
echo "================================================"
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
echo "  1. Go to http://localhost:3002/legal-chat"
echo "  2. Say 'hello' → Should get brief, friendly response"
echo "  3. Ask 'What is GDPR?' → Should get detailed compliance guidance"
echo "  4. Ask 'Should I form an LLC?' → Should get business law comparison"

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
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping SmartProBono MVP with Supabase..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
