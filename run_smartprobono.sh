#!/bin/bash

# Script to run the SmartProBono application (both frontend and backend)

# Define colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Define the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Default options
INIT_DB=false
RESET_DB=false
SKIP_INSTALLS=false
FRONTEND_PORT=4000
BACKEND_PORT=5005
DEBUG_MODE=false

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   SmartProBono Application Launcher    ${NC}"
echo -e "${BLUE}=========================================${NC}"

# Function to show usage
show_usage() {
  echo -e "${CYAN}Usage:${NC} $0 [options]"
  echo
  echo -e "${CYAN}Options:${NC}"
  echo "  --init-db         Initialize database with demo data"
  echo "  --reset-db        Reset database (warning: this deletes existing data)"
  echo "  --skip-installs   Skip dependency installation"
  echo "  --frontend-port N Set frontend port (default: 4000)"
  echo "  --backend-port N  Set backend port (default: 5005)"
  echo "  --debug           Run in debug mode with more verbose output"
  echo "  --help            Show this help message"
  echo
  exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --init-db)
      INIT_DB=true
      shift
      ;;
    --reset-db)
      RESET_DB=true
      shift
      ;;
    --skip-installs)
      SKIP_INSTALLS=true
      shift
      ;;
    --frontend-port)
      FRONTEND_PORT="$2"
      shift 2
      ;;
    --backend-port)
      BACKEND_PORT="$2"
      shift 2
      ;;
    --debug)
      DEBUG_MODE=true
      shift
      ;;
    --help)
      show_usage
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      show_usage
      ;;
  esac
done

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
is_port_in_use() {
  lsof -i:"$1" > /dev/null 2>&1
  return $?
}

# Function to find an available port
find_available_port() {
  local port=$1
  while is_port_in_use $port; do
    echo -e "${YELLOW}Port $port is already in use, trying $((port+1))...${NC}"
    port=$((port+1))
  done
  echo $port
}

# Function to install dependencies
install_dependencies() {
  if [ "$SKIP_INSTALLS" = true ]; then
    echo -e "${YELLOW}Skipping dependency installation...${NC}"
    
    # Still activate the virtual environment
    if [ -d ".venv" ]; then
      echo -e "${GREEN}Activating Python virtual environment...${NC}"
      source .venv/bin/activate
    else
      echo -e "${RED}Virtual environment not found but --skip-installs was specified.${NC}"
      echo -e "${RED}Please ensure your environment is properly set up.${NC}"
    fi
    
    return
  fi
  
  echo -e "${YELLOW}Checking and installing dependencies...${NC}"
  
  # Activate virtual environment for backend
  if [ -d ".venv" ]; then
    echo -e "${GREEN}Activating Python virtual environment...${NC}"
    source .venv/bin/activate
  else
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    source .venv/bin/activate
  fi
  
  # Install backend dependencies
  echo -e "${YELLOW}Installing backend dependencies...${NC}"
  pip3 install -r requirements.txt
  
  # Install frontend dependencies
  echo -e "${YELLOW}Installing frontend dependencies...${NC}"
  cd "$FRONTEND_DIR"
  npm install
  cd "$PROJECT_ROOT"
}

# Function to check for syntax errors in Python files
check_python_syntax() {
  echo -e "${YELLOW}Checking for syntax errors in Python files...${NC}"
  cd "$BACKEND_DIR"
  
  # Activate virtual environment if not already activated
  if [ -z "$VIRTUAL_ENV" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
  fi
  
  # Check routes/legal_ai.py specifically since it has errors
  echo -e "${YELLOW}Checking routes/legal_ai.py for syntax errors...${NC}"
  python3 -m py_compile routes/legal_ai.py 2>&1
  
  # Check general syntax errors in all Python files
  if [ "$DEBUG_MODE" = true ]; then
    echo -e "${YELLOW}Checking all Python files for syntax errors...${NC}"
    find . -name "*.py" -exec python3 -m py_compile {} \; 2>/dev/null
    if [ $? -ne 0 ]; then
      echo -e "${RED}Found syntax errors in Python files. Please fix them before continuing.${NC}"
    else
      echo -e "${GREEN}No syntax errors found.${NC}"
    fi
  fi
  
  cd "$PROJECT_ROOT"
}

# Function to initialize or reset database
setup_database() {
  if [ "$INIT_DB" = true ] || [ "$RESET_DB" = true ]; then
    echo -e "${YELLOW}Setting up database...${NC}"
    cd "$BACKEND_DIR"
    
    # Activate virtual environment if not already activated
    if [ -z "$VIRTUAL_ENV" ]; then
      source "$PROJECT_ROOT/.venv/bin/activate"
    fi
    
    if [ "$RESET_DB" = true ]; then
      echo -e "${RED}WARNING: This will delete all existing data!${NC}"
      read -p "Are you sure you want to reset the database? (y/n): " confirmation
      if [[ $confirmation == [yY] || $confirmation == [yY][eE][sS] ]]; then
        echo -e "${YELLOW}Resetting database...${NC}"
        
        # Remove SQLite database file if it exists
        if [ -f "instance/smartprobono.db" ]; then
          rm -f instance/smartprobono.db
          echo -e "${GREEN}Existing database removed.${NC}"
        fi
        
        # For PostgreSQL, we'll need to run the init script
        echo -e "${YELLOW}Initializing PostgreSQL...${NC}"
        python3 scripts/init_postgres.py
      else
        echo -e "${YELLOW}Database reset cancelled.${NC}"
      fi
    fi
    
    if [ "$INIT_DB" = true ] || [ "$RESET_DB" = true ]; then
      echo -e "${YELLOW}Initializing database...${NC}"
      python3 init_db.py
      echo -e "${GREEN}Database initialized with demo data!${NC}"
    fi
    
    cd "$PROJECT_ROOT"
  fi
}

# Function to start the backend
start_backend() {
  echo -e "${YELLOW}Starting backend server...${NC}"
  cd "$BACKEND_DIR"
  
  # Activate virtual environment if not already activated
  if [ -z "$VIRTUAL_ENV" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
  fi
  
  # Check if backend port is available, find an available one if not
  if is_port_in_use $BACKEND_PORT; then
    old_port=$BACKEND_PORT
    BACKEND_PORT=$(find_available_port $BACKEND_PORT)
    echo -e "${YELLOW}Backend port $old_port is in use, using port $BACKEND_PORT instead.${NC}"
  fi
  
  # Set the FLASK_PORT environment variable
  export FLASK_RUN_PORT=$BACKEND_PORT
  export FLASK_APP=app.py
  
  if [ "$DEBUG_MODE" = true ]; then
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    echo -e "${YELLOW}Running Flask in debug mode...${NC}"
    # Start the backend server with debug mode
    python3 -m flask run --port=$BACKEND_PORT &
  else
    # Start the backend server
    python3 -m flask run --port=$BACKEND_PORT &
  fi
  
  BACKEND_PID=$!
  echo -e "${GREEN}Backend server started with PID: $BACKEND_PID${NC}"
  cd "$PROJECT_ROOT"
}

# Function to start the frontend
start_frontend() {
  echo -e "${YELLOW}Starting frontend development server...${NC}"
  cd "$FRONTEND_DIR"
  
  # Create a temporary .env.local file to override the PORT
  echo "PORT=$FRONTEND_PORT" > .env.local
  echo -e "${YELLOW}Setting frontend to use port $FRONTEND_PORT via .env.local${NC}"
  
  # Start React with the specified port
  # The PORT environment variable needs to be set right before the command
  PORT=$FRONTEND_PORT npm start &
  FRONTEND_PID=$!
  echo -e "${GREEN}Frontend server started with PID: $FRONTEND_PID on port $FRONTEND_PORT${NC}"
  cd "$PROJECT_ROOT"
}

# Function to handle cleanup when script is terminated
cleanup() {
  echo -e "${YELLOW}Shutting down servers...${NC}"
  if [ ! -z "$BACKEND_PID" ]; then
    kill $BACKEND_PID 2>/dev/null
    echo -e "${GREEN}Backend server stopped.${NC}"
  fi
  if [ ! -z "$FRONTEND_PID" ]; then
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Frontend server stopped.${NC}"
  fi
  
  # Remove temporary .env.local file
  if [ -f "$FRONTEND_DIR/.env.local" ]; then
    rm -f "$FRONTEND_DIR/.env.local"
    echo -e "${GREEN}Removed temporary .env.local file.${NC}"
  fi
  
  exit 0
}

# Setup trap for cleanup
trap cleanup SIGINT SIGTERM

# Check if required tools are installed
echo -e "${YELLOW}Checking requirements...${NC}"
if ! command_exists python3; then
  echo -e "${RED}Python 3 is not installed. Please install it to continue.${NC}"
  exit 1
fi

if ! command_exists npm; then
  echo -e "${RED}npm is not installed. Please install Node.js and npm to continue.${NC}"
  exit 1
fi

if ! command_exists lsof; then
  echo -e "${YELLOW}lsof command not found. Port availability checking will be skipped.${NC}"
fi

# Install dependencies
install_dependencies

# Check for syntax errors
check_python_syntax

# Set up database if requested
setup_database

# Start the applications
start_backend
start_frontend

echo -e "${GREEN}SmartProBono is now running!${NC}"
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}Frontend:${NC} http://localhost:$FRONTEND_PORT"
echo -e "${YELLOW}Backend:${NC} http://localhost:$BACKEND_PORT"
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"

# Keep the script running
wait 