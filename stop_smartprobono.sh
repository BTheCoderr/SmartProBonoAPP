#!/bin/bash

# SmartProBono Stop Script
# This script stops all SmartProBono services

echo "🛑 Stopping SmartProBono System..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} ✅ $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')]${NC} ⚠️  $1"
}

# Stop backend server
print_status "Stopping backend server..."
pkill -f "combined_server.py"
if [ $? -eq 0 ]; then
    print_success "Backend server stopped"
else
    print_warning "Backend server was not running"
fi

# Stop frontend server
print_status "Stopping frontend server..."
pkill -f "npm start"
if [ $? -eq 0 ]; then
    print_success "Frontend server stopped"
else
    print_warning "Frontend server was not running"
fi

# Stop any Node.js processes on our ports
print_status "Cleaning up port 3002..."
lsof -ti:3002 | xargs kill -9 2>/dev/null || true

print_status "Cleaning up port 3001..."
lsof -ti:3001 | xargs kill -9 2>/dev/null || true

print_success "SmartProBono system stopped completely"
echo ""
echo "To start the system again, run:"
echo "  ./start_smartprobono_complete.sh"