"""
Tests for authentication routes
"""
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash

def test_register(client):
    """Test user registration"""
    user_data = {
        'email': 'test@example.com',
        'password': 'Test123!@#',
        'name': 'Test User',
        'role': 'client'
    }
    
    response = client.post('/api/auth/register', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'user' in data
    assert data['user']['email'] == user_data['email']
    assert 'token' in data

def test_register_duplicate_email(client, regular_user):
    """Test registration with duplicate email"""
    user_data = {
        'email': regular_user['email'],
        'password': 'Test123!@#',
        'name': 'Test User',
        'role': 'client'
    }
    
    response = client.post('/api/auth/register', json=user_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'email already exists' in data['error'].lower()

def test_login_success(client, regular_user):
    """Test successful login"""
    credentials = {
        'email': regular_user['email'],
        'password': 'password123'  # Assuming this is the password set in fixtures
    }
    
    response = client.post('/api/auth/login', json=credentials)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'user' in data
    assert data['user']['email'] == regular_user['email']

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    credentials = {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
    
    response = client.post('/api/auth/login', json=credentials)
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data

def test_forgot_password(client, regular_user):
    """Test forgot password functionality"""
    data = {
        'email': regular_user['email']
    }
    
    response = client.post('/api/auth/forgot-password', json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'reset link' in data['message'].lower()

def test_reset_password(client, regular_user):
    """Test password reset"""
    # Assuming reset_token is generated and stored in user document
    reset_data = {
        'token': 'valid_reset_token',
        'new_password': 'NewPassword123!@#'
    }
    
    response = client.post('/api/auth/reset-password', json=reset_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'password updated' in data['message'].lower()

def test_change_password(client, auth_headers):
    """Test password change"""
    password_data = {
        'current_password': 'password123',
        'new_password': 'NewPassword123!@#'
    }
    
    response = client.post(
        '/api/auth/change-password',
        headers=auth_headers,
        json=password_data
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'password changed' in data['message'].lower()

def test_refresh_token(client, auth_headers):
    """Test token refresh"""
    response = client.post('/api/auth/refresh', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert data['token'] != auth_headers['Authorization'].split()[1]

def test_logout(client, auth_headers):
    """Test logout"""
    response = client.post('/api/auth/logout', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'logged out' in data['message'].lower()

def test_get_profile(client, auth_headers, regular_user):
    """Test getting user profile"""
    response = client.get('/api/auth/profile', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'user' in data
    assert data['user']['email'] == regular_user['email']

def test_update_profile(client, auth_headers):
    """Test updating user profile"""
    profile_data = {
        'name': 'Updated Name',
        'phone': '123-456-7890',
        'preferences': {
            'notifications_enabled': True,
            'theme': 'dark'
        }
    }
    
    response = client.put(
        '/api/auth/profile',
        headers=auth_headers,
        json=profile_data
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['name'] == profile_data['name']
    assert data['user']['phone'] == profile_data['phone']

def test_validate_token(client, auth_headers):
    """Test token validation"""
    response = client.get('/api/auth/validate', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid' in data
    assert data['valid'] is True

def test_invalid_token_format(client):
    """Test invalid token format"""
    headers = {'Authorization': 'Invalid Token Format'}
    response = client.get('/api/auth/validate', headers=headers)
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data 