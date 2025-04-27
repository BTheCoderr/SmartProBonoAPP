"""
Tests for rights and legal information functionality
"""
import pytest
from backend.models.rights import Rights
from backend.database import db
from backend.app import create_app

def test_create_rights_info(client, auth_headers):
    """Test creating new rights information"""
    rights_data = {
        'category': 'Immigration',
        'title': 'Right to Legal Representation',
        'description': 'Every person has the right to be represented by legal counsel in immigration proceedings.'
    }
    
    response = client.post('/api/rights',
                          json=rights_data,
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == rights_data['title']
    assert data['category'] == rights_data['category']
    
    # Verify in database
    rights = Rights.query.get(data['id'])
    assert rights is not None
    assert rights.title == rights_data['title']

def test_get_rights_info(client):
    """Test retrieving rights information"""
    # Create test rights info
    rights = Rights()
    rights.category = 'Immigration'
    rights.title = 'Right to Fair Hearing'
    rights.description = 'Every person has the right to a fair hearing in immigration court.'
    db.session.add(rights)
    db.session.commit()
    
    response = client.get(f'/api/rights/{rights.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Right to Fair Hearing'
    assert data['category'] == 'Immigration'

def test_list_rights_by_category(client):
    """Test listing rights information by category"""
    # Create multiple rights entries
    categories = ['Immigration', 'Employment', 'Housing']
    for category in categories:
        rights = Rights()
        rights.category = category
        rights.title = f'{category} Rights'
        rights.description = f'Basic rights related to {category.lower()}'
        db.session.add(rights)
    db.session.commit()
    
    # Test filtering by category
    response = client.get('/api/rights?category=Immigration')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert all(item['category'] == 'Immigration' for item in data)

def test_update_rights_info(client, auth_headers):
    """Test updating rights information"""
    # Create test rights info
    rights = Rights()
    rights.category = 'Immigration'
    rights.title = 'Original Title'
    rights.description = 'Original description'
    db.session.add(rights)
    db.session.commit()
    
    update_data = {
        'title': 'Updated Title',
        'description': 'Updated description'
    }
    
    response = client.put(f'/api/rights/{rights.id}',
                         json=update_data,
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['description'] == 'Updated description'

def test_delete_rights_info(client, auth_headers):
    """Test deleting rights information"""
    # Create test rights info
    rights = Rights()
    rights.category = 'Immigration'
    rights.title = 'Test Rights'
    rights.description = 'Test description'
    db.session.add(rights)
    db.session.commit()
    
    response = client.delete(f'/api/rights/{rights.id}',
                           headers=auth_headers)
    
    assert response.status_code == 200
    
    # Verify deletion
    deleted_rights = Rights.query.get(rights.id)
    assert deleted_rights is None

def test_search_rights_info(client):
    """Test searching rights information"""
    # Create test rights info with different content
    test_rights = [
        ('Immigration', 'Visa Application Rights', 'Rights during visa application process'),
        ('Immigration', 'Deportation Rights', 'Rights during deportation proceedings'),
        ('Employment', 'Worker Rights', 'Basic worker rights and protections')
    ]
    
    for category, title, description in test_rights:
        rights = Rights()
        rights.category = category
        rights.title = title
        rights.description = description
        db.session.add(rights)
    db.session.commit()
    
    # Search for visa-related rights
    response = client.get('/api/rights/search?q=visa')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert any('Visa' in item['title'] for item in data)

def test_bulk_rights_creation(client, auth_headers):
    """Test creating multiple rights entries at once"""
    bulk_data = [
        {
            'category': 'Immigration',
            'title': 'Right 1',
            'description': 'Description 1'
        },
        {
            'category': 'Immigration',
            'title': 'Right 2',
            'description': 'Description 2'
        }
    ]
    
    response = client.post('/api/rights/bulk',
                          json={'rights': bulk_data},
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert len(data['created']) == 2
    
    # Verify in database
    for rights_info in data['created']:
        rights = Rights.query.get(rights_info['id'])
        assert rights is not None
        assert rights.category == 'Immigration'

def test_rights_categories(client):
    """Test getting all available rights categories"""
    # Create rights in different categories
    categories = ['Immigration', 'Employment', 'Housing', 'Education']
    for category in categories:
        rights = Rights()
        rights.category = category
        rights.title = f'{category} Right'
        rights.description = f'Description for {category}'
        db.session.add(rights)
    db.session.commit()
    
    response = client.get('/api/rights/categories')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= len(categories)
    for category in categories:
        assert category in data 