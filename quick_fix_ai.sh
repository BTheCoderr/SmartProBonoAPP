#!/bin/bash

# Quick AI Fix Script for SmartProBono
# This script sets up FREE AI tools (Gemini + Ollama)

set -e

echo "🔧 SmartProBono AI Quick Fix"
echo "=============================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the SmartProBono-main directory"
    exit 1
fi

# Step 1: Check for .env file
echo "📝 Step 1: Checking environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.template" ]; then
        cp .env.template .env
        echo "✅ Created .env file from template"
    else
        echo "❌ No .env.template found. Please create .env manually"
        exit 1
    fi
else
    echo "✅ .env file exists"
fi

# Step 2: Check for Ollama
echo ""
echo "🤖 Step 2: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "✅ Ollama is running"
    else
        echo "⚠️  Ollama is not running. Starting..."
        ollama serve &> /dev/null &
        sleep 3
        echo "✅ Ollama started"
    fi
else
    echo "❌ Ollama is not installed"
    echo ""
    echo "Install Ollama with:"
    echo "  brew install ollama"
    echo ""
    read -p "Would you like to install Ollama now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        brew install ollama
        ollama serve &> /dev/null &
        sleep 3
        echo "✅ Ollama installed and started"
    else
        echo "Please install Ollama manually: https://ollama.ai"
        exit 1
    fi
fi

# Step 3: Download AI models
echo ""
echo "📥 Step 3: Downloading AI models..."
MODELS=("tinyllama:1.1b" "gemma2:2b" "qwen2.5:0.5b")

for model in "${MODELS[@]}"; do
    if ollama list | grep -q "$model"; then
        echo "✅ $model already downloaded"
    else
        echo "📥 Downloading $model..."
        ollama pull "$model"
        echo "✅ $model downloaded"
    fi
done

# Step 4: Check Python dependencies
echo ""
echo "🐍 Step 4: Checking Python dependencies..."

if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

source venv/bin/activate

# Install google-generativeai
if python -c "import google.generativeai" &> /dev/null; then
    echo "✅ google-generativeai is installed"
else
    echo "📥 Installing google-generativeai..."
    pip install google-generativeai
    echo "✅ google-generativeai installed"
fi

# Step 5: Check for API keys
echo ""
echo "🔑 Step 5: Checking API keys..."

if grep -q "GEMINI_API_KEY=AIzaSy" .env; then
    echo "✅ Gemini API key is configured"
elif grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "✅ OpenAI API key is configured"
else
    echo "⚠️  No AI API keys found in .env"
    echo ""
    echo "You have two options:"
    echo ""
    echo "OPTION 1 (FREE): Get Google Gemini API key"
    echo "  1. Visit: https://makersuite.google.com/app/apikey"
    echo "  2. Click 'Get API Key'"
    echo "  3. Copy your key (starts with AIzaSy...)"
    echo "  4. Add to .env file: GEMINI_API_KEY=your_key_here"
    echo ""
    echo "OPTION 2 (PAID): Get OpenAI API key"
    echo "  1. Visit: https://platform.openai.com/api-keys"
    echo "  2. Create new key"
    echo "  3. Add to .env file: OPENAI_API_KEY=sk-your_key_here"
    echo ""
    echo "After adding your key, run this script again."
    exit 1
fi

# Step 6: Test configuration
echo ""
echo "🧪 Step 6: Testing configuration..."

# Test Ollama
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama is accessible"
else
    echo "❌ Ollama is not accessible"
    exit 1
fi

# Test Gemini (if configured)
if grep -q "GEMINI_API_KEY=AIzaSy" .env; then
    echo "Testing Gemini API..."
    python3 << 'EOF'
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content('Say hello!')
    print('✅ Gemini API is working')
except Exception as e:
    print(f'❌ Gemini API error: {e}')
    exit(1)
EOF
fi

# Step 7: Restart servers
echo ""
echo "🔄 Step 7: Restarting servers..."

# Stop existing servers
pkill -f "python.*combined_server.py" &> /dev/null || true
pkill -f "npm start" &> /dev/null || true

echo "✅ Stopped old servers"

# Start backend
cd backend
source ../venv/bin/activate
nohup python combined_server.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   Logs: backend.log"

sleep 3

# Check if backend is running
if curl -s http://localhost:3001/api/health &> /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend health check failed (may need more time to start)"
fi

# Start frontend
cd frontend
nohup npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   Logs: frontend.log"

# Final summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your AI tools are now configured:"
echo ""
echo "✅ Ollama (local AI) - Running on http://localhost:11434"
echo "✅ Backend server - Running on http://localhost:3001"
echo "✅ Frontend - Starting on http://localhost:3002"
echo ""
echo "Installed models:"
ollama list
echo ""
echo "Test your setup:"
echo "  curl -X POST http://localhost:3001/api/v1/ai/chat \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"message\": \"What are my tenant rights?\", \"task_type\": \"legal\"}'"
echo ""
echo "View logs:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "Access your app: http://localhost:3002"
echo ""

# Save PIDs for easy cleanup
echo "BACKEND_PID=$BACKEND_PID" > .server_pids
echo "FRONTEND_PID=$FRONTEND_PID" >> .server_pids

echo "To stop servers: pkill -f 'python.*combined_server.py' && pkill -f 'npm start'"
echo ""

