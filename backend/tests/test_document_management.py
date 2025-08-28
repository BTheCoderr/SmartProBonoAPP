"""
Tests for document management functionality
"""
import pytest
import os
from datetime import datetime
from werkzeug.datastructures import FileStorage
from io import BytesIO
from models.document import Document
from models.case_sql import SQLCase
from models.user import User
from database import db
import unittest
import json
import io
from flask import current_app
from backend.app import create_app
from models.template import Template

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

class DocumentManagementTest(unittest.TestCase):
    """Test class for document management functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='attorney'
        )
        self.user.set_password('Test1234!')
        db.session.add(self.user)
        db.session.commit()
        
        # Login and get auth token
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'Test1234!'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.token = data['token']
        self.auth_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        # Create test file data
        self.test_file_content = "This is a test document content."
        
    def tearDown(self):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
        # Clean up test uploads
        uploads_dir = os.path.join(current_app.root_path, 'uploads')
        if os.path.exists(uploads_dir):
            for filename in os.listdir(uploads_dir):
                if filename.startswith('test_'):
                    os.remove(os.path.join(uploads_dir, filename))
    
    def test_document_upload(self):
        """Test uploading a document."""
        # Create test file
        file_data = io.BytesIO(self.test_file_content.encode('utf-8'))
        
        # Upload document
        response = self.client.post(
            '/api/documents',
            data={
                'file': (file_data, 'test_document.txt'),
                'title': 'Test Document',
                'description': 'A test document',
                'document_type': 'case_document'
            },
            headers={'Authorization': f'Bearer {self.token}'},
            content_type='multipart/form-data'
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Document uploaded successfully')
        self.assertTrue('document' in data)
        
        # Verify document in database
        document_id = data['document'].get('id')
        document = Document.query.get(document_id)
        self.assertIsNotNone(document)
        self.assertEqual(document.title, 'Test Document')
        self.assertEqual(document.document_type, 'case_document')
        self.assertEqual(document.uploaded_by, self.user.id)
    
    def test_document_download(self):
        """Test downloading a document."""
        # First upload a document
        file_data = io.BytesIO(self.test_file_content.encode('utf-8'))
        upload_response = self.client.post(
            '/api/documents',
            data={
                'file': (file_data, 'test_document.txt'),
                'title': 'Test Document',
                'description': 'A test document',
                'document_type': 'case_document'
            },
            headers={'Authorization': f'Bearer {self.token}'},
            content_type='multipart/form-data'
        )
        upload_data = json.loads(upload_response.data.decode())
        document_id = upload_data['document'].get('id')
        
        # Download document
        download_response = self.client.get(
            f'/api/documents/{document_id}/file',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        
        self.assertEqual(download_response.status_code, 200)
        self.assertEqual(download_response.data.decode(), self.test_file_content)
    
    def test_document_list(self):
        """Test retrieving a list of documents."""
        # Upload multiple documents
        for i in range(3):
            file_data = io.BytesIO(f"Test content {i}".encode('utf-8'))
            self.client.post(
                '/api/documents',
                data={
                    'file': (file_data, f'test_document_{i}.txt'),
                    'title': f'Test Document {i}',
                    'description': f'A test document {i}',
                    'document_type': 'case_document'
                },
                headers={'Authorization': f'Bearer {self.token}'},
                content_type='multipart/form-data'
            )
        
        # Get document list
        response = self.client.get(
            '/api/documents',
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('documents' in data)
        self.assertEqual(len(data['documents']), 3)
    
    def test_document_update(self):
        """Test updating document metadata."""
        # First upload a document
        file_data = io.BytesIO(self.test_file_content.encode('utf-8'))
        upload_response = self.client.post(
            '/api/documents',
            data={
                'file': (file_data, 'test_document.txt'),
                'title': 'Original Title',
                'description': 'Original description',
                'document_type': 'case_document'
            },
            headers={'Authorization': f'Bearer {self.token}'},
            content_type='multipart/form-data'
        )
        upload_data = json.loads(upload_response.data.decode())
        document_id = upload_data['document'].get('id')
        
        # Update document metadata
        update_response = self.client.put(
            f'/api/documents/{document_id}',
            data=json.dumps({
                'title': 'Updated Title',
                'description': 'Updated description'
            }),
            headers=self.auth_headers
        )
        
        update_data = json.loads(update_response.data.decode())
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_data['document']['title'], 'Updated Title')
        self.assertEqual(update_data['document']['description'], 'Updated description')
        
        # Verify in database
        document = Document.query.get(document_id)
        self.assertEqual(document.title, 'Updated Title')
        self.assertEqual(document.description, 'Updated description')
    
    def test_document_template_creation(self):
        """Test creating a document template."""
        # Create template
        response = self.client.post(
            '/api/templates',
            data=json.dumps({
                'title': 'Test Template',
                'description': 'A test template',
                'content': 'Hello ${name}, welcome to ${organization}!',
                'template_type': 'letter',
                'variables': ['name', 'organization']
            }),
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Template created successfully')
        self.assertTrue('template' in data)
        
        # Verify template in database
        template_id = data['template'].get('id')
        template = Template.query.get(template_id)
        self.assertIsNotNone(template)
        self.assertEqual(template.title, 'Test Template')
        self.assertEqual(template.template_type, 'letter')
    
    def test_document_generation_from_template(self):
        """Test generating a document from a template."""
        # First create a template
        template_response = self.client.post(
            '/api/templates',
            data=json.dumps({
                'title': 'Test Template',
                'description': 'A test template',
                'content': 'Hello ${name}, welcome to ${organization}!',
                'template_type': 'letter',
                'variables': ['name', 'organization']
            }),
            headers=self.auth_headers
        )
        template_data = json.loads(template_response.data.decode())
        template_id = template_data['template'].get('id')
        
        # Generate document from template
        generate_response = self.client.post(
            f'/api/templates/{template_id}/generate',
            data=json.dumps({
                'variables': {
                    'name': 'John Doe',
                    'organization': 'SmartProBono'
                },
                'title': 'Generated Document',
                'document_type': 'case_document'
            }),
            headers=self.auth_headers
        )
        
        generate_data = json.loads(generate_response.data.decode())
        self.assertEqual(generate_response.status_code, 201)
        self.assertEqual(generate_data['message'], 'Document generated successfully')
        self.assertTrue('document' in generate_data)
        
        # Verify generated document content
        document_id = generate_data['document'].get('id')
        document = Document.query.get(document_id)
        self.assertIsNotNone(document)
        self.assertEqual(document.title, 'Generated Document')
        self.assertEqual(document.content, 'Hello John Doe, welcome to SmartProBono!')
        
if __name__ == '__main__':
    unittest.main() 