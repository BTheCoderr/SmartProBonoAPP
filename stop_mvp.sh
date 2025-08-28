#!/bin/bash

# SmartProBono MVP Stop Script
echo "🛑 Stopping SmartProBono MVP..."

# Kill processes on our ports
echo "🔄 Stopping backend (port 8081)..."
lsof -ti:8081 | xargs kill -9 2>/dev/null || echo "No backend process found"

echo "🔄 Stopping frontend (port 3002)..."
lsof -ti:3002 | xargs kill -9 2>/dev/null || echo "No frontend process found"

# Also kill any remaining node/python processes related to our app
echo "🔄 Cleaning up any remaining processes..."
pkill -f "fix_api.py" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true

echo "✅ SmartProBono MVP stopped successfully"
