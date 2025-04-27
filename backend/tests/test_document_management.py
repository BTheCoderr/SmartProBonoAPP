"""
Tests for document management functionality
"""
import pytest
import os
from datetime import datetime
from werkzeug.datastructures import FileStorage
from io import BytesIO
from backend.models.document import Document
from backend.models.case_sql import SQLCase
from backend.models.user import User
from backend.database import db

def test_upload_document(client, auth_headers, test_user):
    """Test uploading a document"""
    # Create a test file
    file_content = b'Test file content'
    file = FileStorage(
        stream=BytesIO(file_content),
        filename='test.pdf',
        content_type='application/pdf'
    )
    
    data = {
        'title': 'Test Document',
        'description': 'Test document description',
        'document_type': 'case_document',
        'file': file
    }
    
    response = client.post('/api/documents/upload',
                          data=data,
                          headers=auth_headers,
                          content_type='multipart/form-data')
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['title'] == 'Test Document'
    assert data['file_type'] == 'pdf'
    
    # Verify document was created in database
    document = Document.query.get(data['id'])
    assert document is not None
    assert document.title == 'Test Document'

def test_get_document(client, auth_headers):
    """Test retrieving a specific document"""
    # Create a test document
    document = Document()
    document.title = 'Test Document'
    document.description = 'Test description'
    document.file_url = 'http://test.com/test.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    response = client.get(f'/api/documents/{document.id}',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Document'
    assert data['file_type'] == 'pdf'

def test_update_document(client, auth_headers):
    """Test updating a document's metadata"""
    # Create a test document
    document = Document()
    document.title = 'Original Title'
    document.description = 'Original description'
    document.file_url = 'http://test.com/test.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated description'
    }
    
    response = client.put(f'/api/documents/{document.id}',
                         json=update_data,
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['description'] == 'Updated description'

def test_delete_document(client, auth_headers):
    """Test deleting a document"""
    # Create a test document
    document = Document()
    document.title = 'Test Document'
    document.description = 'Test description'
    document.file_url = 'http://test.com/test.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    response = client.delete(f'/api/documents/{document.id}',
                           headers=auth_headers)
    
    assert response.status_code == 200
    
    # Verify document was deleted
    deleted_document = Document.query.get(document.id)
    assert deleted_document is None

def test_list_documents(client, auth_headers):
    """Test listing all documents"""
    # Create multiple test documents
    for i in range(3):
        document = Document()
        document.title = f'Test Document {i}'
        document.description = f'Test description {i}'
        document.file_url = f'http://test.com/test{i}.pdf'
        document.file_type = 'pdf'
        document.document_type = 'case_document'
        document.uploaded_by = 1
        db.session.add(document)
    db.session.commit()
    
    response = client.get('/api/documents',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 3

def test_document_sharing(client, auth_headers):
    """Test sharing a document via email"""
    # Create a test document
    document = Document()
    document.title = 'Shared Document'
    document.description = 'Document to be shared'
    document.file_url = 'http://test.com/shared.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    share_data = {
        'email': 'recipient@test.com',
        'message': 'Please review this document'
    }
    
    response = client.post(f'/api/documents/{document.id}/share',
                          json=share_data,
                          headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'shared'
    
    # Verify share was recorded
    document = Document.query.get(document.id)
    assert document is not None, "Document not found after sharing"
    shares = document.email_shares
    assert len(shares) > 0, "No email shares recorded"
    assert shares[-1]['email'] == 'recipient@test.com'

def test_document_version_history(client, auth_headers):
    """Test document version history"""
    # Create a test document
    document = Document()
    document.title = 'Versioned Document'
    document.description = 'Document with versions'
    document.file_url = 'http://test.com/versioned.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    # Add versions
    versions = ['Version 1 content', 'Version 2 content']
    for content in versions:
        document.add_version(content, modified_by=1)
    db.session.commit()
    
    response = client.get(f'/api/documents/{document.id}/history',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert all('version' in version for version in data)

def test_document_search(client, auth_headers):
    """Test searching documents"""
    # Create test documents with different titles
    doc1 = Document()
    doc1.title = 'Immigration Form I-485'
    doc1.description = 'Application to Register Permanent Residence'
    doc1.file_url = 'http://test.com/i485.pdf'
    doc1.file_type = 'pdf'
    doc1.document_type = 'form'
    doc1.uploaded_by = 1
    db.session.add(doc1)
    
    doc2 = Document()
    doc2.title = 'Tax Return 2023'
    doc2.description = 'Annual tax return document'
    doc2.file_url = 'http://test.com/tax.pdf'
    doc2.file_type = 'pdf'
    doc2.document_type = 'supporting_document'
    doc2.uploaded_by = 1
    db.session.add(doc2)
    db.session.commit()
    
    # Search for immigration documents
    response = client.get('/api/documents/search?q=immigration',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert any('I-485' in doc['title'] for doc in data)

def test_document_tags(client, auth_headers):
    """Test adding and removing document tags"""
    # Create a test document
    document = Document()
    document.title = 'Tagged Document'
    document.description = 'Document with tags'
    document.file_url = 'http://test.com/tagged.pdf'
    document.file_type = 'pdf'
    document.document_type = 'case_document'
    document.uploaded_by = 1
    db.session.add(document)
    db.session.commit()
    
    # Add tags
    tags = ['important', 'immigration', 'pending']
    tag_data = {'tags': tags}
    
    response = client.post(f'/api/documents/{document.id}/tags',
                          json=tag_data,
                          headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert all(tag in data['tags'] for tag in tags)
    
    # Remove a tag
    remove_tag = {'tag': 'pending'}
    response = client.delete(f'/api/documents/{document.id}/tags',
                           json=remove_tag,
                           headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'pending' not in data['tags']
    assert len(data['tags']) == 2 