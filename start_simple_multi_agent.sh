#!/bin/bash

# SmartProBono Simple Multi-Agent System Startup Script
echo "🚀 Starting SmartProBono Simple Multi-Agent System"
echo "=================================================="

# Set environment variables
export PORT=8081

echo ""
echo "🔧 Environment Variables Set:"
echo "  • Port: $PORT"
echo "  • System: Multi-Agent Legal AI"
echo "  • Database: Supabase PostgreSQL"

echo ""
echo "🐍 Starting Multi-Agent API Server..."

# Start the Flask server
python multi_agent_integration.py
