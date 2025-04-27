#!/bin/bash
# Script to set up SmartProBono development environment

# Colors for better visibility
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up SmartProBono development environment...${NC}"

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Determine Python command (python or python3)
PYTHON_CMD="python3"
if ! command -v python3 &>/dev/null; then
    if command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}Error: No Python command found. Please install Python 3.${NC}"
        exit 1
    fi
fi

# Set up the backend
echo -e "${YELLOW}Setting up backend...${NC}"
cd backend

# Check if Python 3 is installed
echo -e "${GREEN}Using Python command: ${PYTHON_CMD}${NC}"

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    ${PYTHON_CMD} -m venv venv
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -r requirements.txt
pip install cloudinary aiohttp

cd ..

# Set up the frontend
echo -e "${YELLOW}Setting up frontend...${NC}"
cd frontend

# Check if Node.js is installed
if command -v node &>/dev/null; then
    echo -e "${GREEN}Node.js is installed${NC}"
else
    echo -e "${RED}Node.js is not installed. Please install Node.js.${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
npm install

cd ..

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}You can now run ./start_servers.sh to start the application${NC}" 