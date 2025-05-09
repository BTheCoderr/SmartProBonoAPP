#!/bin/bash

# Script to run the SmartProBono MVP
# Starts both frontend and backend servers

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting SmartProBono MVP...${NC}"

# Check if fix script exists and run it first
if [ -f "./fix_mvp_critical_issues.sh" ]; then
  echo -e "${YELLOW}Running critical fixes script...${NC}"
  bash ./fix_mvp_critical_issues.sh
fi

# Create required directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p backend/templates
mkdir -p backend/instance/documents
mkdir -p frontend/src/components/documents

# Check and create sample document template if needed
if [ ! -f "backend/templates/sample_template.html" ]; then
  echo -e "${YELLOW}Creating sample document template...${NC}"
  cat > backend/templates/sample_template.html << 'EOL'
<!DOCTYPE html>
<html>
<head>
  <title>{{title}}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    h1 { color: #333366; }
    .section { margin-bottom: 20px; }
    .footer { margin-top: 50px; font-size: 0.8em; color: #666; }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{title}}</h1>
    <p>Generated on: {{current_date}}</p>
  </div>
  
  <div class="section">
    <h2>Document Information</h2>
    <p><strong>Client Name:</strong> {{client_name}}</p>
    <p><strong>Document Type:</strong> {{document_type}}</p>
    <p><strong>Reference Number:</strong> {{reference_number}}</p>
  </div>
  
  <div class="section">
    <h2>Content</h2>
    <p>{{content}}</p>
  </div>
  
  <div class="footer">
    <p>SmartProBono Legal Platform - Confidential Document</p>
  </div>
</body>
</html>
EOL
fi

# Start backend server
echo -e "${YELLOW}Starting backend server...${NC}"
cd backend
python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo -e "${GREEN}Backend server started with PID: $BACKEND_PID${NC}"

# Start frontend server
echo -e "${YELLOW}Starting frontend server...${NC}"
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo -e "${GREEN}Frontend server started with PID: $FRONTEND_PID${NC}"

# Success message
echo -e "\n${GREEN}SmartProBono MVP is running!${NC}"
echo -e "Frontend: http://localhost:3000"
echo -e "Backend API: http://localhost:5000"

echo -e "\nKey pages to test:"
echo -e "- Homepage: http://localhost:3000/"
echo -e "- Legal Chat: http://localhost:3000/legal-chat"
echo -e "- Documents: http://localhost:3000/documents"
echo -e "- Expert Help: http://localhost:3000/expert-help"
echo -e "- Login (Demo): http://localhost:3000/login"
echo -e "- Register (Demo): http://localhost:3000/register"

echo -e "\nCheck MVP_COMPLETION_PLAN.md for next steps"
echo -e "\nPress Ctrl+C to stop servers"

# Function to handle cleanup on exit
cleanup() {
  echo -e "\n${YELLOW}Stopping servers...${NC}"
  kill $BACKEND_PID $FRONTEND_PID
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
  echo -e "${GREEN}Servers stopped${NC}"
  exit 0
}

# Set trap for clean exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 