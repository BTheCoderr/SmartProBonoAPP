"""Tests for template functionality"""
import pytest
from io import BytesIO
from models.template import Template
from extensions import db

@pytest.fixture
def sample_template(app):
    """Create a sample template for testing"""
    template = Template(
        template_id='test_template',
        name='Test Template',
        title='Test Form',
        fields=['name', 'date', 'signature'],
        version='1.0',
        is_active=True
    )
    with app.app_context():
        db.session.add(template)
        db.session.commit()
        yield template
        db.session.delete(template)
        db.session.commit()

def test_list_templates(client, sample_template, auth_headers):
    """Test listing templates"""
    response = client.get('/api/templates', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'templates' in data
    assert len(data['templates']) >= 1
    template = data['templates'][0]
    assert all(key in template for key in ['template_id', 'name', 'title', 'fields'])

def test_create_template(client, auth_headers):
    """Test template creation"""
    data = {
        'template_id': 'test-template',
        'name': 'Test Template',
        'title': 'Test Title',
        'fields': {'field1': 'string', 'field2': 'number'},
        'version': '1.0'
    }
    
    response = client.post('/api/templates', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['name'] == data['name']

def test_get_template(client, sample_template, auth_headers):
    """Test getting a specific template"""
    response = client.get(f'/api/templates/{sample_template.template_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['name'] == sample_template.name

def test_update_template(client, sample_template, auth_headers):
    """Test updating a template"""
    data = {
        'name': 'Updated Template',
        'title': 'Updated Title',
        'fields': {'field1': 'string', 'field2': 'number', 'field3': 'date'},
        'version': '1.1'
    }
    
    response = client.put(
        f'/api/templates/{sample_template.template_id}',
        json=data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json['name'] == data['name']
    assert response.json['version'] == data['version']
    
    # Check old version is inactive
    with client.application.app_context():
        old_template = Template.query.filter_by(
            template_id=sample_template.template_id,
            version='1.0'
        ).first()
        assert old_template is not None, "Old template version not found"
        assert not old_template.is_active

def test_delete_template(client, sample_template, auth_headers):
    """Test deleting a template"""
    response = client.delete(
        f'/api/templates/{sample_template.template_id}',
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Verify template is deleted
    template = Template.query.filter_by(template_id=sample_template.template_id).first()
    assert template is None

def test_generate_pdf(client, sample_template, auth_headers):
    """Test PDF generation from template"""
    data = {
        'field1': 'Test Value',
        'field2': 42
    }
    
    response = client.post(
        f'/api/templates/{sample_template.template_id}/generate',
        json=data,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'

def test_template_validation(client, auth_headers):
    """Test template validation"""
    # Test with missing required fields
    data = {
        'name': 'Invalid Template'
    }
    
    response = client.post('/api/templates', json=data, headers=auth_headers)
    assert response.status_code == 400
    
    # Test with invalid field type
    data = {
        'template_id': 'test-template',
        'name': 'Test Template',
        'title': 'Test Title',
        'fields': 'not a dictionary',
        'version': '1.0'
    }
    
    response = client.post('/api/templates', json=data, headers=auth_headers)
    assert response.status_code == 400

def test_template_not_found(client, auth_headers):
    """Test handling of non-existent template"""
    response = client.get('/api/templates/nonexistent', headers=auth_headers)
    assert response.status_code == 404

def test_unauthorized_access(client):
    """Test unauthorized access to templates"""
    response = client.get('/api/templates')
    assert response.status_code == 401

@pytest.mark.websocket
def test_template_notifications(websocket, sample_template):
    """Test template update notifications via WebSocket"""
    websocket.connect()
    websocket.emit('subscribe', {'template_id': sample_template.template_id})
    
    # Update template
    sample_template.name = 'Updated via WebSocket'
    db.session.commit()
    
    received = websocket.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'template_updated'
    assert received[0]['args'][0]['template_id'] == sample_template.template_id 