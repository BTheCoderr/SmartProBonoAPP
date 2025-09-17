#!/usr/bin/env python3
"""
Test the Document Scanner with real PDF upload
"""

import requests
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    """Create a simple test PDF with legal content"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add some legal content
    p.drawString(100, 750, "SAMPLE LEGAL DOCUMENT")
    p.drawString(100, 720, "Contract Agreement")
    p.drawString(100, 690, "")
    p.drawString(100, 660, "This agreement is entered into between:")
    p.drawString(100, 630, "Party A: John Smith, 123 Main St, Anytown, USA")
    p.drawString(100, 600, "Party B: Jane Doe, 456 Oak Ave, Somewhere, USA")
    p.drawString(100, 570, "")
    p.drawString(100, 540, "Terms and Conditions:")
    p.drawString(100, 510, "1. This is a test contract for demonstration purposes")
    p.drawString(100, 480, "2. Payment terms: Net 30 days")
    p.drawString(100, 450, "3. Effective date: September 17, 2025")
    p.drawString(100, 420, "4. Termination clause: Either party may terminate with 30 days notice")
    p.drawString(100, 390, "")
    p.drawString(100, 360, "Signatures:")
    p.drawString(100, 330, "________________________")
    p.drawString(100, 300, "John Smith")
    p.drawString(300, 330, "________________________")
    p.drawString(300, 300, "Jane Doe")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def test_document_scanner():
    """Test the document scanner with a real PDF"""
    print("🧪 Testing Document Scanner")
    print("=" * 40)
    
    # Create test PDF
    print("📄 Creating test PDF...")
    pdf_buffer = create_test_pdf()
    
    # Test the scanner health first
    print("\n🔍 Testing scanner health...")
    try:
        health_response = requests.get('http://localhost:3001/api/scanner/health')
        print(f"   Scanner health: {health_response.status_code}")
        if health_response.ok:
            health_data = health_response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Message: {health_data.get('message')}")
        else:
            print(f"   Error: {health_response.text}")
            return
    except Exception as e:
        print(f"   Error connecting to scanner: {e}")
        return
    
    # Test document upload and analysis
    print("\n📤 Uploading test PDF for analysis...")
    try:
        files = {'file': ('test_contract.pdf', pdf_buffer, 'application/pdf')}
        response = requests.post('http://localhost:3001/api/scanner/analyze', files=files)
        
        print(f"   Upload status: {response.status_code}")
        
        if response.ok:
            result = response.json()
            print("   ✅ Analysis successful!")
            print(f"   Response keys: {list(result.keys())}")
            
            # Show analysis results
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"\n📊 Analysis Results:")
                print(f"   Document type: {analysis.get('document_type', 'Unknown')}")
                print(f"   Key terms found: {len(analysis.get('key_terms', []))}")
                print(f"   Parties identified: {len(analysis.get('parties', []))}")
                print(f"   Risk level: {analysis.get('risk_assessment', {}).get('level', 'Unknown')}")
            
            if 'extracted_text' in result:
                text = result['extracted_text'][:200]
                print(f"\n📝 Extracted Text (first 200 chars):")
                print(f"   {text}...")
                
        else:
            print(f"   ❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
    
    # Test the safe analysis endpoint
    print("\n🛡️ Testing safe analysis endpoint...")
    try:
        pdf_buffer.seek(0)  # Reset buffer
        files = {'file': ('test_contract.pdf', pdf_buffer, 'application/pdf')}
        response = requests.post('http://localhost:3001/api/scanner/analyze-safe', files=files)
        
        print(f"   Safe analysis status: {response.status_code}")
        if response.ok:
            result = response.json()
            print("   ✅ Safe analysis successful!")
            print(f"   Safety features: {result.get('safety_features', [])}")
        else:
            print(f"   ❌ Safe analysis failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Safe analysis error: {e}")

def test_pdf_generator():
    """Test the PDF generator"""
    print("\n📝 Testing PDF Generator")
    print("=" * 40)
    
    # Test generator health
    try:
        health_response = requests.get('http://localhost:3001/api/generator/health')
        print(f"Generator health: {health_response.status_code}")
        if health_response.ok:
            health_data = health_response.json()
            print(f"Status: {health_data.get('status')}")
        
        # Test template listing
        templates_response = requests.get('http://localhost:3001/api/generator/templates')
        print(f"Templates endpoint: {templates_response.status_code}")
        if templates_response.ok:
            templates = templates_response.json()
            print(f"Available templates: {len(templates.get('templates', []))}")
            
    except Exception as e:
        print(f"Generator test error: {e}")

def test_crm_system():
    """Test the CRM system endpoints"""
    print("\n👥 Testing CRM System")
    print("=" * 40)
    
    crm_endpoints = [
        '/api/v1/crm/health',
        '/api/v1/crm/dashboard/analytics',
        '/api/v1/crm/court-dates/upcoming',
        '/api/v1/crm/lawyer/cases',
        '/api/v1/crm/client/intake'
    ]
    
    for endpoint in crm_endpoints:
        try:
            response = requests.get(f'http://localhost:3001{endpoint}')
            status = "✅" if response.ok else f"❌ {response.status_code}"
            print(f"{status} {endpoint}")
            
            if response.ok and 'health' in endpoint:
                data = response.json()
                print(f"    {data.get('message', 'No message')}")
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

if __name__ == "__main__":
    print("🚀 SmartProBono Functional Testing")
    print("Testing real functionality with actual data")
    print("=" * 60)
    
    test_document_scanner()
    test_pdf_generator() 
    test_crm_system()
    
    print("\n" + "=" * 60)
    print("🎯 Testing Complete!")
    print("Check the results above to see what's actually working.")
