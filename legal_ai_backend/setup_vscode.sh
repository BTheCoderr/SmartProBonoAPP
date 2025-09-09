#!/bin/bash
# VSCode Setup Script for Legal AI Backend
# This script sets up the complete CourtListener + Claude pipeline for VSCode

set -e  # Exit on any error

echo "🚀 Setting up Legal AI Backend for VSCode..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this script from the legal_ai_backend directory"
    exit 1
fi

# Step 1: Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Step 2: Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Step 3: Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Step 5: Create .env file if it doesn't exist
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Legal AI Backend Configuration
ANTHROPIC_API_KEY=sk-your-claude-key-here
OPENAI_API_KEY=sk-your-openai-key-here

# Database Configuration
SUPABASE_URL=your-supabase-url-here
SUPABASE_KEY=your-supabase-key-here

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY=./vectorstore/chroma_data

# CourtListener API (free tier)
COURTLISTENER_API_URL=https://www.courtlistener.com/api/rest/v3/opinions/

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
EOF
    print_warning "Created .env file - please update with your API keys"
else
    print_warning ".env file already exists"
fi

# Step 6: Create vector store directory
print_status "Creating vector store directory..."
mkdir -p ../vectorstore/chroma_data
print_success "Vector store directory created"

# Step 7: Test imports
print_status "Testing Python imports..."
python3 -c "
try:
    import langgraph
    import chromadb
    import anthropic
    import requests
    print('✅ All required packages imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Step 8: Run basic tests
print_status "Running basic pipeline tests..."
python3 -c "
import sys
sys.path.append('.')
from agents.intake_agent import intake
from agents.courtlistener_agent import search_live
from agents.vector_agent import search_local

# Test intake agent
print('Testing intake agent...')
result = intake('I was charged with gun possession in Boston')
print(f'✅ Intake agent working: {result[\"topic\"]} case in {result[\"jurisdiction\"]}')

# Test CourtListener agent
print('Testing CourtListener agent...')
context = {'topic': 'criminal', 'jurisdiction': 'ri', 'keywords': ['gun'], 'original_input': 'test'}
try:
    result = search_live(context)
    print(f'✅ CourtListener agent working: {result[\"success\"]}')
except Exception as e:
    print(f'⚠️ CourtListener agent warning: {e}')

# Test vector agent
print('Testing vector agent...')
try:
    result = search_local(context)
    print(f'✅ Vector agent working: {result[\"success\"]}')
except Exception as e:
    print(f'⚠️ Vector agent warning: {e}')

print('✅ Basic tests completed')
"

# Step 9: Create VSCode workspace file
print_status "Creating VSCode workspace configuration..."
cat > ../SmartProBono.code-workspace << EOF
{
    "folders": [
        {
            "name": "SmartProBono Root",
            "path": "."
        },
        {
            "name": "Legal AI Backend",
            "path": "./legal_ai_backend"
        },
        {
            "name": "Frontend",
            "path": "./frontend"
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "./legal_ai_backend/.venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "python.linting.enabled": true,
        "python.formatting.provider": "black",
        "terminal.integrated.cwd": "\${workspaceFolder}",
        "files.exclude": {
            "**/__pycache__": true,
            "**/*.pyc": true,
            "**/node_modules": true
        }
    },
    "extensions": {
        "recommendations": [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-python.flake8",
            "ms-python.pylint",
            "ms-vscode.vscode-json",
            "bradlc.vscode-tailwindcss",
            "esbenp.prettier-vscode"
        ]
    }
}
EOF
print_success "VSCode workspace file created"

# Step 10: Create quick start script
print_status "Creating quick start script..."
cat > quick_start.sh << 'EOF'
#!/bin/bash
# Quick start script for Legal AI Backend

echo "🚀 Starting Legal AI Backend..."

# Activate virtual environment
source .venv/bin/activate

# Check if .env is configured
if grep -q "sk-your-claude-key-here" .env; then
    echo "⚠️ Please configure your Claude API key in .env file"
    echo "Edit .env and replace 'sk-your-claude-key-here' with your actual API key"
    exit 1
fi

# Start the API server
echo "Starting API server on http://localhost:5000"
python3 api_server.py
EOF

chmod +x quick_start.sh
print_success "Quick start script created"

# Final status
echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_success "Legal AI Backend is ready for VSCode"
echo ""
echo "Next steps:"
echo "1. Open VSCode: code ../SmartProBono.code-workspace"
echo "2. Configure your API keys in .env file"
echo "3. Run: ./quick_start.sh"
echo "4. Test the pipeline in VSCode terminal"
echo ""
echo "Available VSCode tasks:"
echo "- Setup Legal AI Backend"
echo "- Start Legal AI Backend"
echo "- Test Legal AI Pipeline"
echo "- Seed Case Law Data"
echo "- Start Frontend"
echo ""
print_status "Happy coding! 🚀"
