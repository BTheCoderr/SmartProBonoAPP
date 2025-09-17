#!/bin/bash

echo "🚀 Starting SmartProBono with CRM Integration Test"
echo "=================================================="

# Check if server is already running
if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "✅ Server is already running on port 3001"
else
    echo "🔄 Starting server..."
    cd backend
    python combined_server.py &
    SERVER_PID=$!
    echo "Server started with PID: $SERVER_PID"
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    sleep 5
    
    # Test if server is responding
    if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
        echo "✅ Server is now running!"
    else
        echo "❌ Server failed to start"
        exit 1
    fi
fi

echo ""
echo "🧪 Testing CRM Connection..."
cd ..
python test_crm_connection.py

echo ""
echo "🌐 Frontend should be available at: http://localhost:3002"
echo "🔗 CRM Test Page: http://localhost:3002/virtual-paralegal/crm"
echo ""
echo "Press Ctrl+C to stop the server"
