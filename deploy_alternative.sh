#!/bin/bash

# ALTERNATIVE DEPLOYMENT - Use different approach
set -e

echo "🔄 ALTERNATIVE DEPLOYMENT - Bypassing PyMuPDF completely"
echo "======================================================="

# Create a clean virtual environment
echo "🧹 Creating clean virtual environment..."
python3 -m venv venv_clean
source venv_clean/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install ONLY our nuclear requirements
echo "📦 Installing nuclear requirements..."
pip install -r requirements-nuclear.txt

# Verify PyMuPDF is not installed
echo "🔍 Verifying PyMuPDF elimination..."
if python -c "import fitz" 2>/dev/null; then
    echo "❌ PyMuPDF is still installed!"
    exit 1
else
    echo "✅ PyMuPDF successfully eliminated"
fi

# Test PDF processing
echo "🧪 Testing PDF processing alternatives..."
python3 -c "
try:
    import pypdf
    import pdfplumber
    import PyPDF2
    print('✅ PDF alternatives working: pypdf, pdfplumber, PyPDF2')
except ImportError as e:
    print(f'❌ PDF alternative test failed: {e}')
    exit(1)
"

echo "🎉 ALTERNATIVE DEPLOYMENT SUCCESSFUL!"
echo "🚀 Starting application with clean environment..."

# Start the application
if [ -f "backend/app.py" ]; then
    cd backend && python app.py
else
    python app.py
fi
