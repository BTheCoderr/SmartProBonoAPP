#!/bin/bash

# AI Tools Diagnostic Script
# Checks what's working and what's not

echo "🔍 SmartProBono AI Tools Diagnostic"
echo "===================================="
echo ""

# Check .env file
echo "1. Checking environment configuration..."
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
    
    # Check for API keys (without exposing them)
    if grep -q "GEMINI_API_KEY=AIzaSy" .env; then
        echo "   ✅ Gemini API key is configured"
    elif grep -q "GEMINI_API_KEY=$" .env || ! grep -q "GEMINI_API_KEY" .env; then
        echo "   ❌ Gemini API key is NOT configured"
    fi
    
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "   ✅ OpenAI API key is configured"
    elif grep -q "OPENAI_API_KEY=$" .env || ! grep -q "OPENAI_API_KEY" .env; then
        echo "   ❌ OpenAI API key is NOT configured"
    fi
    
    if grep -q "ANTHROPIC_API_KEY=sk-ant-" .env; then
        echo "   ✅ Anthropic API key is configured"
    elif grep -q "ANTHROPIC_API_KEY=$" .env || ! grep -q "ANTHROPIC_API_KEY" .env; then
        echo "   ❌ Anthropic API key is NOT configured"
    fi
else
    echo "   ❌ .env file NOT found"
fi

echo ""

# Check Ollama
echo "2. Checking Ollama (local AI)..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama is installed"
    
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "   ✅ Ollama is running"
        
        echo "   📦 Installed models:"
        ollama list | grep -v "NAME" | while read line; do
            echo "      - $line"
        done
    else
        echo "   ❌ Ollama is NOT running"
        echo "      Start with: ollama serve"
    fi
else
    echo "   ❌ Ollama is NOT installed"
    echo "      Install with: brew install ollama"
fi

echo ""

# Check Python dependencies
echo "3. Checking Python dependencies..."
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment exists"
    
    source venv/bin/activate
    
    if python -c "import google.generativeai" &> /dev/null; then
        echo "   ✅ google-generativeai is installed"
    else
        echo "   ❌ google-generativeai is NOT installed"
        echo "      Install with: pip install google-generativeai"
    fi
    
    if python -c "import openai" &> /dev/null; then
        echo "   ✅ openai is installed"
    else
        echo "   ⚠️  openai is NOT installed (optional)"
    fi
    
    if python -c "import anthropic" &> /dev/null; then
        echo "   ✅ anthropic is installed"
    else
        echo "   ⚠️  anthropic is NOT installed (optional)"
    fi
else
    echo "   ❌ Virtual environment NOT found"
    echo "      Create with: python3 -m venv venv"
fi

echo ""

# Check if servers are running
echo "4. Checking servers..."
if lsof -i :3001 &> /dev/null; then
    echo "   ✅ Backend is running (port 3001)"
    
    if curl -s http://localhost:3001/api/health &> /dev/null; then
        echo "   ✅ Backend health check passed"
    else
        echo "   ⚠️  Backend is running but health check failed"
    fi
else
    echo "   ❌ Backend is NOT running (port 3001)"
fi

if lsof -i :3002 &> /dev/null; then
    echo "   ✅ Frontend is running (port 3002)"
else
    echo "   ❌ Frontend is NOT running (port 3002)"
fi

echo ""

# Test AI endpoint
echo "5. Testing AI endpoint..."
if curl -s http://localhost:3001/api/health &> /dev/null; then
    response=$(curl -s -X POST http://localhost:3001/api/v1/ai/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello", "task_type": "legal"}' 2>&1)
    
    if echo "$response" | grep -q "text"; then
        echo "   ✅ AI endpoint is responding"
        
        if echo "$response" | grep -q "unable to access"; then
            echo "   ⚠️  Getting fallback message (AI not properly configured)"
        else
            echo "   ✅ AI is working properly!"
        fi
    else
        echo "   ❌ AI endpoint returned error"
        echo "   Response: $response"
    fi
else
    echo "   ❌ Cannot test - backend not running"
fi

echo ""
echo "======================================"
echo "📋 SUMMARY"
echo "======================================"
echo ""

# Determine the issue
ISSUES=0

if [ ! -f ".env" ]; then
    echo "❌ Missing .env file"
    ISSUES=$((ISSUES + 1))
fi

if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not installed"
    ISSUES=$((ISSUES + 1))
elif ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "❌ Ollama not running"
    ISSUES=$((ISSUES + 1))
fi

if [ -f ".env" ]; then
    if ! grep -q "GEMINI_API_KEY=AIzaSy" .env && ! grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "❌ No valid AI API keys configured"
        ISSUES=$((ISSUES + 1))
    fi
fi

if [ $ISSUES -eq 0 ]; then
    echo "✅ Everything looks good!"
    echo ""
    echo "If you're still having issues, check:"
    echo "  - Browser console for frontend errors"
    echo "  - Backend logs for API errors"
    echo "  - API key validity"
else
    echo ""
    echo "🔧 QUICK FIX:"
    echo ""
    echo "Run the quick fix script:"
    echo "  ./quick_fix_ai.sh"
    echo ""
    echo "Or follow the manual guide:"
    echo "  cat FIX_AI_TOOLS.md"
fi

echo ""

