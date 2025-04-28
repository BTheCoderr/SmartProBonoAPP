"""
Tests for user management functionality
"""
import pytest
from datetime import datetime
from backend.models.user import User
from backend.database import db

def test_user_registration(client):
    """Test user registration"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    response = client.post('/api/auth/register',
                          json=user_data)
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['email'] == user_data['email']
    
    # Verify user was created in database
    user = User.query.filter_by(email=user_data['email']).first()
    assert user is not None
    assert user.username == user_data['username']
    assert user.role == 'client'  # Default role

def test_user_login(client):
    """Test user login"""
    # Create a test user
    user = User(email='login@test.com')
    user.set_password('testpass123')
    user.role = 'client'
    db.session.add(user)
    db.session.commit()
    
    login_data = {
        'email': 'login@test.com',
        'password': 'testpass123'
    }
    
    response = client.post('/api/auth/login',
                          json=login_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_user_profile(client, auth_headers):
    """Test getting and updating user profile"""
    # Create a test user
    user = User(username='profiletest', email='profile@test.com')
    user.set_password('testpass123')
    user.role = 'client'
    db.session.add(user)
    db.session.commit()
    
    # Get profile
    response = client.get('/api/users/profile',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == 'profile@test.com'
    
    # Update profile
    update_data = {
        'first_name': 'Updated',
        'last_name': 'Name'
    }
    
    response = client.put('/api/users/profile',
                         json=update_data,
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == 'Updated'
    assert data['last_name'] == 'Name'

def test_password_reset(client):
    """Test password reset flow"""
    # Create a test user
    user = User(username='resettest', email='reset@test.com')
    user.set_password('oldpass123')
    user.role = 'client'
    db.session.add(user)
    db.session.commit()
    
    # Request password reset
    reset_request = {
        'email': 'reset@test.com'
    }
    
    response = client.post('/api/auth/reset-password-request',
                          json=reset_request)
    
    assert response.status_code == 200
    
    # Simulate reset token (in real app this would come via email)
    reset_data = {
        'token': 'simulated_reset_token',
        'new_password': 'newpass123'
    }
    
    response = client.post('/api/auth/reset-password',
                          json=reset_data)
    
    assert response.status_code == 200
    
    # Try logging in with new password
    login_data = {
        'email': 'reset@test.com',
        'password': 'newpass123'
    }
    
    response = client.post('/api/auth/login',
                          json=login_data)
    
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_email_verification(client, auth_headers):
    """Test email verification flow"""
    # Create an unverified test user
    user = User(
        username='verifytest',
        email='verify@test.com',
        active=True  # Explicitly set active
    )
    user.set_password('testpass123')
    user.role = 'client'
    # email_verified defaults to False in the model
    db.session.add(user)
    db.session.commit()
    
    # Request verification email
    response = client.post('/api/auth/request-verification',
                          headers=auth_headers)
    
    assert response.status_code == 200
    
    # Simulate verification (in real app this would be a token from email)
    verify_data = {
        'token': 'simulated_verify_token'
    }
    
    response = client.post('/api/auth/verify-email',
                          json=verify_data,
                          headers=auth_headers)
    
    assert response.status_code == 200
    
    # Check that user is now verified
    user = User.query.filter_by(email='verify@test.com').first()
    assert user is not None
    assert user.email_verified is True  # This field exists in the model

def test_role_management(client, auth_headers):
    """Test role-based access control"""
    # Create users with different roles
    roles = ['client', 'lawyer', 'admin']
    users = []
    for i, role in enumerate(roles):
        user = User(email=f'role{i}@test.com')
        user.set_password('testpass123')
        user.role = role
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    
    # Test access to admin-only endpoint
    response = client.get('/api/admin/users',
                         headers=auth_headers)
    
    if auth_headers['Authorization'].endswith('admin'):
        assert response.status_code == 200
    else:
        assert response.status_code in [401, 403]

def test_user_search(client, auth_headers):
    """Test searching for users"""
    # Create test users
    test_users = [
        ('John', 'Doe', 'lawyer'),
        ('Jane', 'Smith', 'client'),
        ('Bob', 'Johnson', 'lawyer')
    ]
    
    for first_name, last_name, role in test_users:
        username = f'{first_name.lower()}{last_name.lower()}'
        email = f'{first_name.lower()}@test.com'
        user = User(username=username, email=email)
        user.set_password('testpass123')
        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        db.session.add(user)
    
    db.session.commit()
    
    # Search for lawyers
    response = client.get('/api/users/search?role=lawyer',
                         headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 2
    assert all(user['role'] == 'lawyer' for user in data)

def test_user_deactivation(client, auth_headers):
    """Test deactivating and reactivating users"""
    # Create a test user
    user = User(email='deactivate@test.com')
    user.set_password('testpass123')
    user.role = 'client'
    user.active = True
    db.session.add(user)
    db.session.commit()
    
    # Deactivate user
    response = client.post(f'/api/admin/users/{user.id}/deactivate',
                          headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['active'] is False
    
    # Try to log in (should fail)
    login_data = {
        'email': 'deactivate@test.com',
        'password': 'testpass123'
    }
    
    response = client.post('/api/auth/login',
                          json=login_data)
    
    assert response.status_code == 401
    
    # Reactivate user
    response = client.post(f'/api/admin/users/{user.id}/activate',
                          headers=auth_headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['active'] is True
    
    # Try to log in again (should succeed)
    response = client.post('/api/auth/login',
                          json=login_data)
    
    assert response.status_code == 200
    assert 'access_token' in response.get_json() 