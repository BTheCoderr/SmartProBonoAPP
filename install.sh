#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo "SmartProBono Installation"
echo "========================="
echo "Project directory: $PROJECT_DIR"

# Install backend dependencies
echo "
Setting up backend..."
cd "$BACKEND_DIR"

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# Install core dependencies first (required)
echo "Installing core backend dependencies..."
python3 -m pip install -r requirements.txt

# Install optional dependencies (AI, documents, PDF)
echo "Installing optional backend dependencies..."
# AI module requirements
python3 -m pip install openai==1.0.0 numpy==1.26.4 || true
# Document processing 
python3 -m pip install docxtpl==0.16.7 phonenumbers==8.13.28 || true
# Try installing OpenCV (might fail on some systems)
python3 -m pip install opencv-python-headless==4.8.0.74 || true
# PDF processing
python3 -m pip install WeasyPrint==60.1 reportlab==4.1.0 pdfkit==1.0.0 PyPDF2==3.0.1 || true

echo "Backend setup complete!"

# Install frontend dependencies
echo "
Setting up frontend..."
cd "$FRONTEND_DIR"

# Use --legacy-peer-deps to avoid npm dependency conflicts
echo "Installing frontend dependencies..."
npm install --legacy-peer-deps

echo "
Installation complete!"
echo "To run the application, use: ./start.sh" 