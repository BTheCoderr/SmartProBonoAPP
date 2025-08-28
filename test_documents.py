#!/usr/bin/env python3
"""
Test script for document API endpoints
"""

import requests
import json
import os
import sys
import time
from datetime import datetime
import mimetypes
import base64

def test_document_endpoints(test_file_path=None):
    """
    Test the document API endpoints
    """
    if not test_file_path:
        print("Error: Please provide a test file path")
        print("Usage: python test_documents.py path/to/test/file.pdf")
        return False
    
    if not os.path.exists(test_file_path):
        print(f"Error: File not found: {test_file_path}")
        return False
    
    # API base URL
    api_url = "http://localhost:8081/api"
    
    # Test document history endpoint
    print("\n1. Testing GET /api/documents/history")
    history_response = requests.get(f"{api_url}/documents/history")
    
    if history_response.status_code == 200:
        print(f"✅ Documents history endpoint returned {history_response.status_code}")
        documents = history_response.json().get('documents', [])
        print(f"   Found {len(documents)} documents")
        
        for doc in documents[:2]:  # Show first 2 documents
            print(f"   - {doc.get('title')} ({doc.get('type')}, {doc.get('format')})")
    else:
        print(f"❌ Documents history endpoint failed: {history_response.status_code}")
        print(f"   Error: {history_response.text}")
    
    # Test templates endpoint
    print("\n2. Testing GET /api/documents/templates")
    templates_response = requests.get(f"{api_url}/documents/templates")
    
    if templates_response.status_code == 200:
        print(f"✅ Templates endpoint returned {templates_response.status_code}")
        templates = templates_response.json().get('templates', [])
        print(f"   Found {len(templates)} templates")
        
        for template in templates[:2]:  # Show first 2 templates
            print(f"   - {template.get('title')} ({template.get('category')})")
    else:
        print(f"❌ Templates endpoint failed: {templates_response.status_code}")
        print(f"   Error: {templates_response.text}")
    
    # Test upload signature endpoint
    print("\n3. Testing GET /api/uploads/signature")
    signature_response = requests.get(f"{api_url}/uploads/signature?type=document")
    
    if signature_response.status_code == 200:
        print(f"✅ Upload signature endpoint returned {signature_response.status_code}")
        signature_data = signature_response.json()
        print(f"   Got signature: {signature_data.get('signature')[:10]}...")
    else:
        print(f"❌ Upload signature endpoint failed: {signature_response.status_code}")
        print(f"   Error: {signature_response.text}")
    
    # Test document upload
    print("\n4. Testing POST /api/documents")
    
    # Get file info
    file_name = os.path.basename(test_file_path)
    file_size = os.path.getsize(test_file_path)
    file_extension = os.path.splitext(file_name)[1][1:].lower()
    
    # In a real world scenario, we'd upload to Cloudinary first
    # For this test, we'll create a mock document directly
    document_data = {
        "title": f"Test Document - {file_name}",
        "type": "legal",
        "format": file_extension,
        "size": file_size,
        "content": f"mock_content_url_for_{file_name}",
        "tags": ["test", "document", file_extension]
    }
    
    document_response = requests.post(f"{api_url}/documents", json=document_data)
    
    if document_response.status_code == 200:
        print(f"✅ Document upload endpoint returned {document_response.status_code}")
        new_document = document_response.json()
        document_id = new_document.get('_id')
        print(f"   Created document with ID: {document_id}")
        print(f"   Title: {new_document.get('title')}")
        print(f"   Type: {new_document.get('type')}")
        print(f"   Format: {new_document.get('format')}")
        print(f"   Size: {new_document.get('size')} bytes")
        
        # Test getting a single document
        print("\n5. Testing GET /api/documents/{document_id}")
        get_doc_response = requests.get(f"{api_url}/documents/{document_id}")
        
        if get_doc_response.status_code == 200:
            print(f"✅ Get document endpoint returned {get_doc_response.status_code}")
            document = get_doc_response.json()
            print(f"   Retrieved document: {document.get('title')}")
        else:
            print(f"❌ Get document endpoint failed: {get_doc_response.status_code}")
            print(f"   Error: {get_doc_response.text}")
        
        # Test deleting a document
        print("\n6. Testing DELETE /api/documents/{document_id}")
        delete_response = requests.delete(f"{api_url}/documents/{document_id}")
        
        if delete_response.status_code == 200:
            print(f"✅ Delete document endpoint returned {delete_response.status_code}")
            print(f"   Successfully deleted document with ID: {document_id}")
        else:
            print(f"❌ Delete document endpoint failed: {delete_response.status_code}")
            print(f"   Error: {delete_response.text}")
    else:
        print(f"❌ Document upload endpoint failed: {document_response.status_code}")
        print(f"   Error: {document_response.text}")
    
    print("\nDocument API testing completed!")
    return True

if __name__ == "__main__":
    test_file_path = sys.argv[1] if len(sys.argv) > 1 else None
    test_document_endpoints(test_file_path) 