#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "⚡ SmartProBono Ultra-Lightweight Mode"
echo "====================================="
echo "🚀 Optimized for minimal resource usage"
echo "💡 Using only lightweight models (< 2GB)"
echo ""

# 1. Stop any existing services
echo "1. 🔄 Stopping any existing services..."
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
lsof -ti:8010 | xargs kill -9 2>/dev/null || true
lsof -ti:3002 | xargs kill -9 2>/dev/null || true
sleep 2

# Activate virtual environment
source venv/bin/activate

# 2. Start Backend (advanced_multi_agent_api.py)
echo "2. 🐍 Starting Backend (Ultra-Lightweight Mode)..."
python advanced_multi_agent_api.py > backend_lightweight.log 2>&1 &
BACKEND_PID=$!
sleep 3

if curl -s http://localhost:8081/api/health | grep -q "ok"; then
    echo -e "   Backend: ${GREEN}✅ Running${NC}"
else
    echo -e "   Backend: ${RED}❌ Failed to start${NC}"
    echo "   Check backend_lightweight.log for details"
    exit 1
fi

echo ""
echo "🎉 SmartProBono Ultra-Lightweight System is running!"
echo "=================================================="
echo "🌐 Access Your System:"
echo "  • Backend: http://localhost:8081"
echo "  • Health Check: http://localhost:8081/api/health"
echo ""
echo "⚡ Available Lightweight Models:"
echo "  • Qwen 2.5 (0.5B) - Ultra-fast (0.4 GB)"
echo "  • TinyLlama (1.1B) - Instant responses (0.6 GB)"
echo "  • Gemma 2B - Balanced (1.5 GB)"
echo "  • Llama 3.2 (3B) - Best quality (1.9 GB)"
echo ""
echo "🎯 Test Commands:"
echo "  # Test ultra-fast Qwen model:"
echo "  curl -X POST http://localhost:8081/api/legal/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"Hello!\", \"task_type\": \"qwen\"}'"
echo ""
echo "  # Test TinyLlama (fastest):"
echo "  curl -X POST http://localhost:8081/api/legal/chat \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"Quick test\", \"task_type\": \"tiny\"}'"
echo ""
echo "📊 System Status:"
echo "Backend PID: $BACKEND_PID"
echo ""
echo "📝 Logs:"
echo "  • Backend: backend_lightweight.log"
echo ""
echo -e "${YELLOW}💡 Ultra-Lightweight Tips:${NC}"
echo "   • Use 'qwen' model for fastest responses"
echo "   • Use 'tiny' model for instant responses"
echo "   • Perfect for development and testing"
echo "   • Minimal resource usage"
echo ""
echo -e "${YELLOW}🛑 To stop: kill $BACKEND_PID${NC}"

# Keep the script running until Ctrl+C is pressed
trap "kill $BACKEND_PID; echo -e '\n🛑 Ultra-lightweight system stopped.'; exit" INT
wait $BACKEND_PID
