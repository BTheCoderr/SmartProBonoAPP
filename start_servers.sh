#!/bin/bash
# Script to start both frontend and backend servers

# Colors for better visibility
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting SmartProBono servers...${NC}"

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

# Start the backend server
echo -e "${GREEN}Starting backend server...${NC}"
cd backend
# Activate the virtual environment and start the Flask app
source venv/bin/activate
echo -e "${GREEN}Running Flask app with ${PYTHON_CMD}...${NC}"
${PYTHON_CMD} app.py &
BACKEND_PID=$!
cd ..

# Wait a bit for the backend to start
echo -e "${YELLOW}Waiting for backend to initialize...${NC}"
sleep 3

# Start the frontend server
echo -e "${GREEN}Starting frontend server...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}Both servers are starting!${NC}"
echo -e "${YELLOW}Backend PID: ${BACKEND_PID}${NC}"
echo -e "${YELLOW}Frontend PID: ${FRONTEND_PID}${NC}"
echo -e "${GREEN}Access the app at: http://localhost:3100${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"

# Handle Ctrl+C to properly kill both servers
trap "echo -e '${RED}Stopping servers...${NC}'; kill $BACKEND_PID; kill $FRONTEND_PID; exit" INT

# Keep the script running
wait 