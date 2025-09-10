#!/bin/bash

# Force deployment script - Aggressively removes PyMuPDF
set -e

echo "🚀 Starting FORCE deployment (PyMuPDF-free)..."

# Remove any existing PyMuPDF installations
echo "🧹 Removing any existing PyMuPDF installations..."
pip uninstall -y PyMuPDF pymupdf4llm || true

# Install only our deployment requirements
echo "📦 Installing deployment requirements..."
pip install -r requirements-deploy.txt

# Double-check PyMuPDF is not installed
echo "🔍 Verifying PyMuPDF is not installed..."
if python -c "import fitz" 2>/dev/null; then
    echo "❌ PyMuPDF is still installed! Removing it..."
    pip uninstall -y PyMuPDF pymupdf4llm
    echo "✅ PyMuPDF removed"
else
    echo "✅ PyMuPDF is not installed"
fi

# Verify PDF processing works with alternatives
echo "🔍 Testing PDF processing with alternatives..."
python3 -c "
try:
    from backend.utils.pdf_processor import pdf_processor
    print(f'✅ PDF processor initialized with: {pdf_processor.primary_lib}')
    print(f'📚 Available libraries: {pdf_processor.available_libraries}')
    if 'pymupdf' in pdf_processor.available_libraries and pdf_processor.available_libraries['pymupdf']:
        print('❌ ERROR: PyMuPDF is still available!')
        exit(1)
    else:
        print('✅ PyMuPDF is not available - using alternatives')
except Exception as e:
    print(f'❌ PDF processor test failed: {e}')
    exit(1)
"

echo "🎉 Force deployment completed successfully!"
echo "🚀 Starting application..."

# Start the application
if [ -f "backend/app.py" ]; then
    cd backend && python app.py
else
    python app.py
fi
