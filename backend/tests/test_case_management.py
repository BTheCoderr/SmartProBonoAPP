"""
Tests for case management functionality
"""
import pytest
from datetime import datetime
from bson import ObjectId
from backend.models.case_sql import SQLCase
from backend.models.user import User
from backend.database import db

def test_create_case(client, auth_headers, regular_user, mongo_client):
    """Test creating a new case"""
    case_data = {
        'title': 'Test Immigration Case',
        'description': 'Test case for immigration assistance',
        'category': 'Immigration',
        'priority': 'high'
    }
    
    response = client.post('/api/cases', 
                          json=case_data,
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['title'] == case_data['title']
    
    # Verify case was created in database
    case = SQLCase.query.get(data['id'])
    assert case is not None
    assert case.title == case_data['title']
    assert case.client_id == regular_user['id']

def test_get_case(client, auth_headers, mongo_client):
    """Test retrieving a specific case"""
    # Create a test case first
    case = SQLCase()
    case.title = 'Test Case'
    case.description = 'Test description'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    db.session.commit()
    
    response = client.get(f'/api/cases/{case.id}',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Case'
    assert data['status'] == 'open'

def test_update_case(client, auth_headers, mongo_client):
    """Test updating a case"""
    # Create a test case
    case = SQLCase()
    case.title = 'Original Title'
    case.description = 'Original description'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    db.session.commit()
    
    update_data = {
        'title': 'Updated Title',
        'status': 'in_progress'
    }
    
    response = client.put(f'/api/cases/{case.id}',
                         json=update_data,
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'
    assert data['status'] == 'in_progress'
    
    # Verify update in database
    updated_case = SQLCase.query.get(case.id)
    assert updated_case is not None, "Updated case not found in database"
    assert updated_case.title == 'Updated Title'
    assert updated_case.status == 'in_progress'

def test_delete_case(client, auth_headers, mongo_client):
    """Test deleting a case"""
    # Create a test case
    case = SQLCase()
    case.title = 'Test Case'
    case.description = 'Test description'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    db.session.commit()
    
    response = client.delete(f'/api/cases/{case.id}',
                           headers=auth_headers)
    
    assert response.status_code == 200
    
    # Verify case was deleted
    deleted_case = SQLCase.query.get(case.id)
    assert deleted_case is None

def test_list_cases(client, auth_headers, mongo_client):
    """Test listing all cases"""
    # Create multiple test cases
    for i in range(3):
        case = SQLCase()
        case.title = f'Test Case {i}'
        case.description = f'Test description {i}'
        case.client_id = 1
        case.category = 'Immigration'
        case.status = 'open'
        db.session.add(case)
    db.session.commit()
    
    response = client.get('/api/cases',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 3
    assert all(case['category'] == 'Immigration' for case in data)

def test_case_filtering(client, auth_headers, mongo_client):
    """Test filtering cases by various criteria"""
    # Create cases with different statuses
    statuses = ['open', 'in_progress', 'closed']
    for status in statuses:
        case = SQLCase()
        case.title = f'Test Case - {status}'
        case.description = f'Test description for {status} case'
        case.client_id = 1
        case.category = 'Immigration'
        case.status = status
        db.session.add(case)
    db.session.commit()
    
    # Test filtering by status
    response = client.get('/api/cases?status=open',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert all(case['status'] == 'open' for case in data)

def test_case_assignment(client, auth_headers, mongo_client):
    """Test assigning a case to a lawyer"""
    # Create a test case and lawyer
    case = SQLCase()
    case.title = 'Test Case'
    case.description = 'Test description'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    
    # Create lawyer with required parameters
    lawyer = User(
        username='testlawyer',
        email='lawyer@test.com',
        role='lawyer'
    )
    db.session.add(lawyer)
    db.session.commit()
    
    assignment_data = {
        'lawyer_id': lawyer.id
    }
    
    response = client.post(f'/api/cases/{case.id}/assign',
                          json=assignment_data,
                          headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['lawyer_id'] == lawyer.id
    assert data['status'] == 'assigned'

def test_case_status_workflow(client, auth_headers, mongo_client):
    """Test the complete case status workflow"""
    # Create a test case
    case = SQLCase()
    case.title = 'Workflow Test Case'
    case.description = 'Testing complete workflow'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    db.session.commit()
    
    # Test each status transition
    statuses = ['in_progress', 'under_review', 'approved', 'closed']
    for status in statuses:
        response = client.put(f'/api/cases/{case.id}',
                            json={'status': status},
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == status
        
        # Verify status in database
        updated_case = SQLCase.query.get(case.id)
        assert updated_case is not None, f"Case not found after updating status to {status}"
        assert updated_case.status == status

def test_case_document_association(client, auth_headers, mongo_client):
    """Test associating documents with a case"""
    # Create a test case
    case = SQLCase()
    case.title = 'Document Test Case'
    case.description = 'Testing document association'
    case.client_id = 1
    case.category = 'Immigration'
    case.status = 'open'
    db.session.add(case)
    db.session.commit()
    
    # Create a test document
    document_data = {
        'title': 'Test Document',
        'type': 'application_form'
    }
    
    response = client.post(f'/api/cases/{case.id}/documents',
                          json=document_data,
                          headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == document_data['title']
    assert data['case_id'] == case.id 