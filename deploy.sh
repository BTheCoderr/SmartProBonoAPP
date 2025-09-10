#!/bin/bash

# SmartProBono Deployment Script
# This script handles deployment with PyMuPDF fallback

set -e

echo "🚀 Starting SmartProBono deployment..."

# Check if we're in a deployment environment
if [ "$RENDER" = "true" ] || [ "$VERCEL" = "1" ] || [ "$HEROKU" = "true" ] || [ "$RAILWAY" = "true" ]; then
    echo "🌐 Detected deployment environment - using fallback requirements"
    
    # Use deployment-specific requirements
    if [ -f "requirements-deploy.txt" ]; then
        echo "📦 Installing deployment requirements..."
        pip install -r requirements-deploy.txt
    else
        echo "📦 Installing standard requirements with PyMuPDF alternatives..."
        pip install pypdf==4.0.1 pdfplumber==0.10.3 PyPDF2==3.0.1
        pip install -r requirements.txt --no-deps
    fi
else
    echo "💻 Local development environment"
    echo "📦 Installing all requirements..."
    pip install -r requirements.txt
fi

# Verify PDF processing capabilities
echo "🔍 Verifying PDF processing capabilities..."
python3 -c "
try:
    from backend.utils.pdf_processor import pdf_processor
    print(f'✅ PDF processor initialized with: {pdf_processor.primary_lib}')
    print(f'📚 Available libraries: {pdf_processor.available_libraries}')
except Exception as e:
    print(f'❌ PDF processor initialization failed: {e}')
    print('⚠️  Continuing with limited PDF functionality...')
"

echo "🎉 Deployment preparation completed successfully!"
echo "🚀 Starting application..."

# Start the application
if [ -f "backend/app.py" ]; then
    cd backend && python app.py
else
    python app.py
fi