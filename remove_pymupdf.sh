#!/bin/bash

# Script to completely remove PyMuPDF and install alternatives
echo "🧹 Removing PyMuPDF completely..."

# Uninstall PyMuPDF and related packages
pip uninstall -y PyMuPDF pymupdf4llm fitz || true

# Install PDF processing alternatives
echo "📦 Installing PDF processing alternatives..."
pip install pypdf==4.0.1 pdfplumber==0.10.3 PyPDF2==3.0.1

# Verify PyMuPDF is gone
echo "🔍 Verifying PyMuPDF is removed..."
if python -c "import fitz" 2>/dev/null; then
    echo "❌ PyMuPDF is still installed!"
    exit 1
else
    echo "✅ PyMuPDF successfully removed"
fi

# Test PDF processing
echo "🔍 Testing PDF processing with alternatives..."
python3 -c "
try:
    import pypdf
    import pdfplumber
    import PyPDF2
    print('✅ PDF processing alternatives installed successfully')
    print('📚 Available: pypdf, pdfplumber, PyPDF2')
except ImportError as e:
    print(f'❌ Error: {e}')
    exit(1)
"

echo "🎉 PyMuPDF removal completed successfully!"
