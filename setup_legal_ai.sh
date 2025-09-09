#!/bin/bash

# Legal AI Integration Setup Script
# This script sets up the legal AI backend integration

echo "🚀 Setting up Legal AI Integration for SmartProBono"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: Please run this script from the SmartProBono root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install legal AI dependencies
echo "📚 Installing Legal AI dependencies..."
pip install --upgrade pip
pip install -r legal_ai_backend/requirements.txt

# Install additional dependencies for integration
echo "🔗 Installing integration dependencies..."
pip install langgraph langchain langchain-community langchain-anthropic langchain-openai
pip install chromadb anthropic pydantic

# Create .env file for legal AI if it doesn't exist
if [ ! -f "legal_ai_backend/.env" ]; then
    echo "📝 Creating .env file for legal AI backend..."
    cat > legal_ai_backend/.env << EOF
# Legal AI Backend Environment Variables
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Supabase configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key_here
EOF
    echo "⚠️  Please update legal_ai_backend/.env with your actual API keys"
fi

# Test the integration
echo "🧪 Testing Legal AI integration..."
python test_legal_ai_integration.py

echo ""
echo "✅ Legal AI Integration setup complete!"
echo ""
echo "Next steps:"
echo "1. Update legal_ai_backend/.env with your API keys"
echo "2. Start the backend: cd backend && python combined_server.py"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Visit http://localhost:3002/legal-chat to test the integration"
echo ""
echo "For testing, run: python test_legal_ai_integration.py"
