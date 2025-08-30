#!/bin/bash

# SmartProBono Multi-Agent System Startup Script
echo "🚀 Starting SmartProBono Multi-Agent System"
echo "============================================="

# Set environment variables
export PG_CONN_STR="postgresql://postgres.ewtcvsohdgkthuyajyyk:***REMOVED***@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
export SUPABASE_URL="https://ewtcvsohdgkthuyajyyk.supabase.co"
export SUPABASE_SERVICE_KEY="***REMOVED***"
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3:8b"
export HAYSTACK_TELEMETRY_ENABLED="false"
export LOG_LEVEL="INFO"

echo ""
echo "🔧 Environment Variables Set:"
echo "  • Database: Supabase PostgreSQL with pgvector"
echo "  • AI Model: Ollama (local)"
echo "  • Orchestration: LangGraph"
echo "  • RAG: Haystack 2.x"

echo ""
echo "🐍 Starting Multi-Agent API Server..."

# Start the FastAPI server
cd smartprobono_backend
source ../venv/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
