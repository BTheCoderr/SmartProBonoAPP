#!/bin/bash
# Install dependencies for database optimization scripts

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}      Installing Dependencies for Database Scripts         ${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    echo ""
    echo "Install Python 3:"
    echo "  macOS:   brew install python3"
    echo "  Ubuntu:  sudo apt-get install python3 python3-pip"
    echo "  Windows: Download from https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Install supabase-py
echo ""
echo -e "${BLUE}📦 Installing supabase-py...${NC}"

if python3 -c "import supabase" 2>/dev/null; then
    echo -e "${GREEN}✅ supabase-py already installed${NC}"
else
    echo "Installing..."
    pip3 install supabase
    
    if python3 -c "import supabase" 2>/dev/null; then
        echo -e "${GREEN}✅ supabase-py installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install supabase-py${NC}"
        exit 1
    fi
fi

# Check environment variables
echo ""
echo -e "${BLUE}🔧 Checking environment configuration...${NC}"

if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file found${NC}"
    
    # Check if required variables are set
    if grep -q "SUPABASE_URL" .env && grep -q "SUPABASE_KEY\|SUPABASE_ANON_KEY" .env; then
        echo -e "${GREEN}✅ Supabase configuration found${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file exists but may be incomplete${NC}"
        echo "Make sure it contains:"
        echo "  SUPABASE_URL=https://ewtcvsohdgkthuyajyyk.supabase.co"
        echo "  SUPABASE_KEY=your-anon-key-here"
    fi
else
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo ""
    echo "Create .env file with:"
    echo "  echo 'SUPABASE_URL=https://ewtcvsohdgkthuyajyyk.supabase.co' > .env"
    echo "  echo 'SUPABASE_KEY=your-anon-key-here' >> .env"
    echo ""
    echo "Get your API key from:"
    echo "  https://app.supabase.com/project/ewtcvsohdgkthuyajyyk/settings/api"
fi

# Make scripts executable
echo ""
echo -e "${BLUE}🔧 Making scripts executable...${NC}"

chmod +x scripts/*.sh scripts/*.py database/migrations/*.py 2>/dev/null || true

echo -e "${GREEN}✅ Scripts are now executable${NC}"

# Summary
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo "Next steps:"
echo "1. If you haven't already, create .env with your Supabase keys"
echo "2. Run: ./scripts/quick_fix_database.sh"
echo "3. Follow the prompts to fix your database"
echo ""
echo "For more info: cat START_HERE.md"
echo ""

