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
  <meta charset="utf-8">
  <title>{{title}}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    .header { text-align: center; margin-bottom: 30px; }
    .content { line-height: 1.6; }
    .signature { margin-top: 50px; }
    .footer { margin-top: 50px; text-align: center; font-size: 12px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{title}}</h1>
    <p>Generated on {{current_date}}</p>
  </div>
  
  <div class="content">
    <p>This document certifies that <strong>{{client_name}}</strong> has received legal assistance from SmartProBono regarding <strong>{{matter_description}}</strong>.</p>
    
    <p>{{content}}</p>
    
    <div class="signature">
      <p>Signed:</p>
      <p>___________________________</p>
      <p>{{user_name}}</p>
      <p>Date: {{current_date}}</p>
    </div>
  </div>
  
  <div class="footer">
    <p>SmartProBono Legal Platform | Document ID: {{document_id}} | Confidential</p>
  </div>
</body>
</html>
EOL
fi

# Start backend server in the background
echo -e "${YELLOW}Starting backend server...${NC}"
(cd backend && python3 app.py > ../logs/backend.log 2>&1) &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started with PID: ${BACKEND_PID}${NC}"

# Wait a bit for backend to initialize
sleep 2

# Start frontend server in the background
echo -e "${YELLOW}Starting frontend server...${NC}"
(cd frontend && npm start > ../logs/frontend.log 2>&1) &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend server started with PID: ${FRONTEND_PID}${NC}"

# Output helpful info
echo -e "\n${GREEN}SmartProBono MVP is running!${NC}"
echo -e "Frontend: http://localhost:3003"
echo -e "Backend API: http://localhost:5000"
echo -e "\nKey pages to test:"
echo -e "- Homepage: http://localhost:3003/"
echo -e "- Legal Chat: http://localhost:3003/legal-chat"
echo -e "- Documents: http://localhost:3003/documents"
echo -e "- Expert Help: http://localhost:3003/expert-help"
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

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup INT

# Wait for user to press Ctrl+C
while true; do
  sleep 1
done 