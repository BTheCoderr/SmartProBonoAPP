#!/bin/bash

# Comprehensive Application Test Script
# Tests both frontend and backend for errors

echo "🧪 Testing SmartProBono Application..."
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Test 1: Check Python dependencies
echo "📦 Test 1: Checking Python dependencies..."
if python3 -c "import flask" 2>/dev/null; then
    echo -e "${GREEN}✅ Flask installed${NC}"
else
    echo -e "${RED}❌ Flask not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

if python3 -c "import flask_cors" 2>/dev/null; then
    echo -e "${GREEN}✅ Flask-CORS installed${NC}"
else
    echo -e "${RED}❌ Flask-CORS not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 2: Check Node dependencies
echo ""
echo "📦 Test 2: Checking Node dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✅ Frontend node_modules exists${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend node_modules not found - run 'cd frontend && npm install'${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Test 3: Check critical files exist
echo ""
echo "📁 Test 3: Checking critical files..."
FILES=(
    "app.py"
    "backend/combined_server.py"
    "frontend/src/App.js"
    "frontend/src/index.js"
    "frontend/src/design-system/index.js"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
    else
        echo -e "${RED}❌ $file missing${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Test 4: Check backend can import
echo ""
echo "🐍 Test 4: Testing backend imports..."
cd backend 2>/dev/null || cd .
if python3 -c "from combined_server import app" 2>/dev/null; then
    echo -e "${GREEN}✅ Backend imports successfully${NC}"
else
    echo -e "${RED}❌ Backend import failed${NC}"
    ERRORS=$((ERRORS + 1))
    echo "   Trying to see error:"
    python3 -c "from combined_server import app" 2>&1 | head -5
fi
cd .. 2>/dev/null

# Test 5: Check frontend syntax
echo ""
echo "⚛️  Test 5: Checking frontend syntax..."
if command -v node &> /dev/null; then
    if node -c frontend/src/App.js 2>/dev/null; then
        echo -e "${GREEN}✅ App.js syntax valid${NC}"
    else
        echo -e "${YELLOW}⚠️  App.js syntax check failed (may need build tools)${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️  Node.js not found - skipping syntax check${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Test 6: Check for common import errors
echo ""
echo "🔍 Test 6: Checking for common import issues..."
MISSING_IMPORTS=0

# Check if design-system exports are correct
if grep -q "export.*PageLayout" frontend/src/design-system/index.js 2>/dev/null; then
    echo -e "${GREEN}✅ design-system exports PageLayout${NC}"
else
    echo -e "${RED}❌ design-system missing PageLayout export${NC}"
    MISSING_IMPORTS=$((MISSING_IMPORTS + 1))
fi

if grep -q "export.*Section" frontend/src/design-system/index.js 2>/dev/null; then
    echo -e "${GREEN}✅ design-system exports Section${NC}"
else
    echo -e "${RED}❌ design-system missing Section export${NC}"
    MISSING_IMPORTS=$((MISSING_IMPORTS + 1))
fi

ERRORS=$((ERRORS + MISSING_IMPORTS))

# Test 7: Check environment variables
echo ""
echo "🔐 Test 7: Checking environment configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ .env file exists${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "======================================"
echo "📊 Test Summary"
echo "======================================"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All critical tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start backend: python3 app.py"
    echo "2. Start frontend: cd frontend && npm start"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS error(s) that need to be fixed${NC}"
    exit 1
fi

