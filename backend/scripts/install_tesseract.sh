#!/bin/bash

# Script to install Tesseract OCR on different operating systems
# Usage: ./install_tesseract.sh

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux system"
    # Check for package manager
    if command -v apt-get &> /dev/null; then
        echo "Installing Tesseract OCR using apt..."
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr
        sudo apt-get install -y libtesseract-dev
    elif command -v yum &> /dev/null; then
        echo "Installing Tesseract OCR using yum..."
        sudo yum update -y
        sudo yum install -y tesseract
        sudo yum install -y tesseract-devel
    else
        echo "Unsupported Linux distribution. Please install Tesseract OCR manually."
        echo "Visit: https://tesseract-ocr.github.io/tessdoc/Installation.html"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS system"
    # Check if homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing Tesseract OCR using Homebrew..."
        brew install tesseract
    else
        echo "Homebrew not found. Please install Homebrew first:"
        echo "ruby -e \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\""
        exit 1
    fi
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "Detected Windows system"
    echo "Please install Tesseract OCR manually on Windows:"
    echo "1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "2. Run the installer and follow the instructions"
    echo "3. Add the Tesseract installation directory to your PATH environment variable"
    exit 0
else
    echo "Unknown operating system. Please install Tesseract OCR manually."
    echo "Visit: https://tesseract-ocr.github.io/tessdoc/Installation.html"
    exit 1
fi

# Check installation
if command -v tesseract &> /dev/null; then
    echo "Tesseract OCR installed successfully!"
    tesseract --version
else
    echo "Tesseract OCR installation may have failed. Please check the logs above."
    exit 1
fi

# Verify pytesseract installation with pip
echo "Installing/Verifying pytesseract Python package..."
pip install pytesseract Pillow

echo "Installation complete! You may need to update the pytesseract path in:"
echo "backend/services/ocr_service.py"
echo ""
echo "Example path configurations:"
echo "- Linux: pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'"
echo "- macOS: pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'"
echo "- Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'" 