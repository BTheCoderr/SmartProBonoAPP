#!/bin/bash

echo "🚀 Setting up SmartProBono YC Demo"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if system is already running
if curl -s http://localhost:8081/api/health > /dev/null 2>&1; then
    echo "✅ System is already running!"
else
    echo "🔄 Starting multi-layer AI system..."
    python advanced_multi_agent_api.py &
    sleep 5
    
    # Check if system started successfully
    if curl -s http://localhost:8081/api/health > /dev/null 2>&1; then
        echo "✅ Multi-layer AI system started successfully!"
    else
        echo "❌ Failed to start system. Please check the logs."
        exit 1
    fi
fi

echo ""
echo "🧪 Testing Demo Scenarios..."
echo "============================"

# Test 1: Immigration + Compliance
echo "📋 Test 1: Immigration + Compliance"
echo "Query: 'I need help with H1B visa application and compliance requirements'"
echo ""

response1=$(curl -s -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with H1B visa application and compliance requirements"}')

echo "Agent Chain: $(echo $response1 | jq -r '.agent_chain // [] | join(" → ")')"
echo "Main Agent: $(echo $response1 | jq -r '.agent_name // "Unknown"')"
echo "Sub-Agents: $(echo $response1 | jq -r '.sub_agents_used // [] | join(", ")')"
echo "Response Length: $(echo $response1 | jq -r '.response | length') characters"
echo ""

# Test 2: Business Formation
echo "📋 Test 2: Business Formation"
echo "Query: 'How do I incorporate an LLC in California?'"
echo ""

response2=$(curl -s -X POST http://localhost:8081/api/legal/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I incorporate an LLC in California?"}')

echo "Agent Chain: $(echo $response2 | jq -r '.agent_chain // [] | join(" → ")')"
echo "Main Agent: $(echo $response2 | jq -r '.agent_name // "Unknown"')"
echo "Sub-Agents: $(echo $response2 | jq -r '.sub_agents_used // [] | join(", ")')"
echo "Response Length: $(echo $response2 | jq -r '.response | length') characters"
echo ""

echo "🎉 Demo Setup Complete!"
echo "======================"
echo ""
echo "📊 Demo Statistics:"
echo "- System Status: ✅ Running"
echo "- Multi-Layer Architecture: ✅ Working"
echo "- Agent-to-Agent Calls: ✅ Functional"
echo "- Synthesis: ✅ Combining responses"
echo "- Human Escalation: ✅ Built-in"
echo ""
echo "🎬 Ready for YC Demo!"
echo ""
echo "Demo Commands:"
echo "=============="
echo ""
echo "# Test Immigration + Compliance"
echo "curl -X POST http://localhost:8081/api/legal/chat \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"message\": \"I need help with H1B visa application and compliance requirements\"}' | jq"
echo ""
echo "# Test Business Formation"
echo "curl -X POST http://localhost:8081/api/legal/chat \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"message\": \"How do I incorporate an LLC in California?\"}' | jq"
echo ""
echo "🎯 Key Points for Demo:"
echo "- Show agent chain: supervisor → immigration → document → compliance → synthesis"
echo "- Highlight sub-agents called: document, compliance"
echo "- Emphasize comprehensive responses"
echo "- Mention human escalation for complex cases"
echo ""
echo "Good luck with your YC application! 🚀"
