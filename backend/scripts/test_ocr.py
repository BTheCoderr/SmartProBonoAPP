#!/usr/bin/env python3
"""
Test script for the OCR service
Usage: python test_ocr.py <image_file>
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path to import the OCR service
parent_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(parent_dir))

try:
    from services.ocr_service import ocr_service
    
    def test_ocr(image_path, document_type='general'):
        """Test the OCR service with an image file"""
        
        if not Path(image_path).exists():
            print(f"Error: File not found: {image_path}")
            return
            
        print(f"Testing OCR service with image: {image_path}")
        print(f"Document type: {document_type}")
        
        # Create a file-like object for the OCR service
        class DummyFile:
            def __init__(self, path):
                self.path = path
                self.filename = os.path.basename(path)
                
            def save(self, destination):
                import shutil
                shutil.copy(self.path, destination)
                
        # Process the image
        file_obj = DummyFile(image_path)
        result = ocr_service.process_image(file_obj, document_type)
        
        # Pretty print the results
        print("\nOCR Results:")
        print("=" * 50)
        print(f"Success: {result.get('success', False)}")
        
        if result.get('error'):
            print(f"Error: {result.get('error')}")
            return
            
        print(f"\nExtracted Text:\n{'-' * 50}")
        print(result.get('extractedText', ''))
        
        print(f"\nExtracted Data:\n{'-' * 50}")
        print(json.dumps(result.get('extractedData', {}), indent=2))
        
    if __name__ == "__main__":
        if len(sys.argv) < 2:
            print("Usage: python test_ocr.py <image_file> [document_type]")
            sys.exit(1)
            
        image_path = sys.argv[1]
        document_type = sys.argv[2] if len(sys.argv) > 2 else 'general'
        
        test_ocr(image_path, document_type)
        
except ImportError as e:
    print(f"Error importing OCR service: {e}")
    print("Make sure you're running this script from the backend directory.")
    print("If the OCR service is not found, make sure you've installed all requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1) 