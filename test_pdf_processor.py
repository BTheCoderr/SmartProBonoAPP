#!/usr/bin/env python3
"""
Test script for PDF processor functionality
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_pdf_processor():
    """Test the PDF processor functionality"""
    try:
        from utils.pdf_processor import pdf_processor
        
        print("🔍 Testing PDF Processor...")
        print(f"📚 Available libraries: {pdf_processor.available_libraries}")
        print(f"🎯 Primary library: {pdf_processor.primary_lib}")
        
        # Test with a simple PDF (if available)
        test_pdf_path = "test.pdf"
        if os.path.exists(test_pdf_path):
            print(f"📄 Testing with {test_pdf_path}...")
            with open(test_pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            text = pdf_processor.extract_text(pdf_data)
            print(f"✅ Extracted {len(text)} characters")
            print(f"📖 First 200 characters: {text[:200]}...")
            
            page_count = pdf_processor.get_page_count(pdf_data)
            print(f"📄 Page count: {page_count}")
            
            metadata = pdf_processor.get_metadata(pdf_data)
            print(f"📋 Metadata: {metadata}")
        else:
            print("⚠️  No test PDF found, testing with empty data...")
            # Test with empty data
            try:
                text = pdf_processor.extract_text(b"")
                print("✅ Empty data handled gracefully")
            except Exception as e:
                print(f"⚠️  Empty data error (expected): {e}")
        
        print("🎉 PDF Processor test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ PDF Processor test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_processor()
    sys.exit(0 if success else 1)
