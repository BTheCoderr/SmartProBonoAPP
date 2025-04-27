"""
Tests for admin routes
"""
import pytest
from datetime import datetime
from bson import ObjectId

def test_get_users(client, test_admin):
    """Test getting all users"""
    response = client.get('/api/admin/users')
    assert response.status_code == 200
    data = response.json
    assert len(data) >= 2  # At least test_user and test_admin

def test_get_user(client, test_admin, test_user):
    """Test getting a specific user"""
    response = client.get(f'/api/admin/users/{test_user.id}')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_update_user(client, test_admin, test_user):
    """Test updating a user"""
    update_data = {
        'first_name': 'Updated',
        'last_name': 'Name',
        'email': 'updated@example.com'
    }
    response = client.put(f'/api/admin/users/{test_user.id}', json=update_data)
    assert response.status_code == 200
    assert response.json['first_name'] == 'Updated'
    assert response.json['email'] == 'updated@example.com'

def test_delete_user(client, test_admin, test_user):
    """Test deleting a user"""
    response = client.delete(f'/api/admin/users/{test_user.id}')
    assert response.status_code == 200

def test_get_user_stats(client, test_admin):
    """Test getting user statistics"""
    response = client.get('/api/admin/stats/users')
    assert response.status_code == 200
    data = response.json
    assert 'total_users' in data
    assert 'active_users' in data

def test_get_system_settings(client, test_admin):
    """Test getting system settings"""
    response = client.get('/api/admin/settings')
    assert response.status_code == 200
    data = response.json
    assert 'email_notifications' in data
    assert 'maintenance_mode' in data

def test_update_system_settings(client, test_admin):
    """Test updating system settings"""
    settings = {
        'email_notifications': True,
        'maintenance_mode': False
    }
    response = client.put('/api/admin/settings', json=settings)
    assert response.status_code == 200

def test_get_performance_metrics(client, test_admin):
    """Test getting performance metrics"""
    response = client.get('/api/admin/metrics')
    assert response.status_code == 200
    data = response.json
    assert 'average_response_time' in data
    assert 'active_cases' in data
    assert 'completed_cases' in data

def test_unauthorized_access(client):
    """Test unauthorized access to admin routes"""
    response = client.get('/api/admin/users')
    assert response.status_code == 401

def test_invalid_role(client, test_user):
    """Test access with invalid role"""
    response = client.get('/api/admin/users')
    assert response.status_code in [401, 403]

def test_broadcast_notification(client, test_admin):
    """Test broadcasting a notification"""
    notification = {
        'title': 'System Update',
        'message': 'The system will be down for maintenance',
        'type': 'info'
    }
    response = client.post('/api/admin/notifications/broadcast', json=notification)
    assert response.status_code == 200
    data = response.json
    assert data['title'] == 'System Update' 