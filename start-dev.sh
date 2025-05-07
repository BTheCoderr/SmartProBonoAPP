#!/bin/bash

# Start development servers for SmartProBono

# Define color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}=======================================${NC}"
echo -e "${GREEN}  Starting SmartProBono Development   ${NC}"
echo -e "${GREEN}=======================================${NC}"

# Check if environment variables file exists
if [ -f .env ]; then
    echo -e "${GREEN}Loading environment variables from .env file${NC}"
    export $(cat .env | grep -v '#' | xargs)
else
    echo -e "${YELLOW}No .env file found. Using default environment variables.${NC}"
    # Set default environment variables
    export FLASK_APP=backend/app.py
    export FLASK_ENV=development
    export PORT=5003
    export FRONTEND_PORT=3003
    export APP_URL=http://localhost:3003
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${GREEN}Creating default .env file${NC}"
    cat > .env << EOL
FLASK_APP=backend/app.py
FLASK_ENV=development
PORT=5003
FRONTEND_PORT=3003
APP_URL=http://localhost:3003

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
# EMAIL_USERNAME=your-email@gmail.com
# EMAIL_PASSWORD=your-app-password
EMAIL_FROM=noreply@smartprobono.org
EMAIL_FROM_NAME=SmartProBono
EOL
    echo -e "${YELLOW}Created default .env file. Edit it to configure email sending.${NC}"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start backend server
echo -e "${GREEN}Starting backend server on port ${PORT:-5003}...${NC}"
cd backend && python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started with PID ${BACKEND_PID}${NC}"

# Wait for backend to initialize
sleep 2

# Start frontend server
echo -e "${GREEN}Starting frontend server on port ${FRONTEND_PORT:-3003}...${NC}"
cd ../frontend && npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend server started with PID ${FRONTEND_PID}${NC}"

# Print server URLs
echo -e "${GREEN}=======================================${NC}"
echo -e "${GREEN}Servers started:${NC}"
echo -e "${GREEN}Backend:${NC} http://localhost:${PORT:-5003}"
echo -e "${GREEN}Frontend:${NC} http://localhost:${FRONTEND_PORT:-3003}"
echo -e "${GREEN}=======================================${NC}"
echo -e "${YELLOW}Logs available in logs/ directory${NC}"
echo -e "${RED}Press Ctrl+C to stop both servers${NC}"

# Function to clean up processes on exit
cleanup() {
    echo -e "${YELLOW}Stopping servers...${NC}"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    echo -e "${GREEN}Servers stopped.${NC}"
    exit 0
}

# Set up cleanup on script exit
trap cleanup INT

# Wait for user to press Ctrl+C
wait 