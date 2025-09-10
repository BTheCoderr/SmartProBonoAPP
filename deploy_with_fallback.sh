#!/bin/bash

# Deployment script with PyMuPDF fallback handling
# This script tries to install PyMuPDF first, then falls back to alternatives

set -e

echo "🚀 Starting deployment with PyMuPDF fallback handling..."

# Function to install requirements with fallback
install_requirements() {
    local requirements_file=$1
    echo "📦 Installing requirements from $requirements_file..."
    
    # Try to install all requirements first
    if pip install -r "$requirements_file"; then
        echo "✅ All requirements installed successfully"
        return 0
    else
        echo "⚠️  Some requirements failed, trying fallback approach..."
        
        # Install core requirements first
        pip install Flask==2.3.3 Flask-CORS==4.0.0 python-dotenv==1.0.0 gunicorn==21.2.0
        pip install pymongo==4.5.0 flask-pymongo==2.3.0 psycopg2-binary==2.9.9
        pip install requests==2.31.0 flask-mail==0.9.1
        pip install openai==1.0.0 anthropic==0.34.2 langchain==0.3.7 langgraph==0.2.16
        pip install chromadb==0.4.24 pydantic==2.5.0
        pip install bcrypt==4.0.1 python-dateutil==2.8.2 cryptography>=41.0.0
        pip install numpy==1.26.4 psutil==5.9.6
        
        # Try PyMuPDF with specific version
        echo "🔧 Attempting to install PyMuPDF..."
        if pip install PyMuPDF==1.23.7; then
            echo "✅ PyMuPDF installed successfully"
        else
            echo "⚠️  PyMuPDF installation failed, using alternatives..."
            # Install PDF processing alternatives
            pip install pypdf==4.0.1 pdfplumber==0.10.3 PyPDF2==3.0.1
            echo "✅ PDF processing alternatives installed"
        fi
        
        # Install remaining requirements
        pip install reportlab==4.0.7 Werkzeug>=2.3.7 Jinja2>=3.1.2
        pip install itsdangerous>=2.1.2 click>=8.1.3 blinker>=1.6.2
        
        echo "✅ Fallback installation completed"
        return 0
    fi
}

# Check if we're in a deployment environment
if [ "$RENDER" = "true" ] || [ "$VERCEL" = "1" ] || [ "$HEROKU" = "true" ]; then
    echo "🌐 Detected deployment environment"
    
    # Use deployment-specific requirements
    if [ -f "requirements-deploy.txt" ]; then
        echo "📋 Using deployment-specific requirements"
        install_requirements "requirements-deploy.txt"
    else
        echo "📋 Using standard requirements with fallback"
        install_requirements "requirements.txt"
    fi
else
    echo "💻 Local development environment"
    install_requirements "requirements.txt"
fi

# Verify PDF processing capabilities
echo "🔍 Verifying PDF processing capabilities..."
python3 -c "
try:
    from utils.pdf_processor import pdf_processor
    print(f'✅ PDF processor initialized with: {pdf_processor.primary_lib}')
    print(f'📚 Available libraries: {pdf_processor.available_libraries}')
except Exception as e:
    print(f'❌ PDF processor initialization failed: {e}')
    exit(1)
"

echo "🎉 Deployment preparation completed successfully!"
