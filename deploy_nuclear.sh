#!/bin/bash

# NUCLEAR DEPLOYMENT - COMPLETELY ELIMINATE PyMuPDF
set -e

echo "💥 NUCLEAR DEPLOYMENT - PyMuPDF ELIMINATION"
echo "============================================="

# Step 1: Remove ALL PyMuPDF traces
echo "🧹 Step 1: Removing ALL PyMuPDF traces..."
pip uninstall -y PyMuPDF pymupdf4llm fitz || true
pip cache purge || true

# Step 2: Install ONLY our nuclear requirements
echo "📦 Step 2: Installing nuclear requirements (NO PyMuPDF)..."
pip install -r requirements-nuclear.txt

# Step 3: Verify PyMuPDF is completely gone
echo "🔍 Step 3: Verifying PyMuPDF elimination..."
if python -c "import fitz" 2>/dev/null; then
    echo "❌ CRITICAL: PyMuPDF is still installed!"
    echo "💥 NUCLEAR DEPLOYMENT FAILED!"
    exit 1
else
    echo "✅ PyMuPDF successfully eliminated"
fi

# Step 4: Test PDF processing with alternatives
echo "🧪 Step 4: Testing PDF processing alternatives..."
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

# Step 5: Test our PDF processor
echo "🔧 Step 5: Testing PDF processor..."
python3 -c "
try:
    from backend.utils.pdf_processor import pdf_processor
    print(f'✅ PDF processor initialized with: {pdf_processor.primary_lib}')
    print(f'📚 Available libraries: {list(pdf_processor.available_libraries.keys())}')
    if 'pymupdf' in pdf_processor.available_libraries and pdf_processor.available_libraries['pymupdf']:
        print('❌ ERROR: PyMuPDF is still available in processor!')
        exit(1)
    else:
        print('✅ PyMuPDF not available in processor - using alternatives')
except Exception as e:
    print(f'❌ PDF processor test failed: {e}')
    exit(1)
"

echo "🎉 NUCLEAR DEPLOYMENT SUCCESSFUL!"
echo "🚀 PyMuPDF completely eliminated!"
echo "📄 PDF processing using alternatives only"

# Start the application
echo "🚀 Starting application..."
if [ -f "backend/app.py" ]; then
    cd backend && python app.py
else
    python app.py
fi
