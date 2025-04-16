import pytest
import json
import os
from services.user_service import UserService
from datetime import datetime

@pytest.fixture
def user_service(tmp_path):
    """Create a UserService instance with a temporary data file"""
    test_data = {
        'users': [
            {
                'id': 'test-1',
                'email': 'attorney1@test.com',
                'role': 'volunteer_attorney',
                'profile': {
                    'full_name': 'Test Attorney 1',
                    'specialties': ['housing', 'family'],
                    'availability': 'weekdays'
                }
            },
            {
                'id': 'test-2',
                'email': 'attorney2@test.com',
                'role': 'volunteer_attorney',
                'profile': {
                    'full_name': 'Test Attorney 2',
                    'specialties': ['immigration'],
                    'availability': 'weekends'
                }
            },
            {
                'id': 'test-3',
                'email': 'client@test.com',
                'role': 'client',
                'profile': {
                    'full_name': 'Test Client'
                }
            }
        ]
    }
    
    test_file = tmp_path / "test_users.json"
    with open(test_file, 'w') as f:
        json.dump(test_data, f)
    
    service = UserService()
    service.users_file = str(test_file)
    return service

def test_get_user_by_id(user_service):
    """Test getting a user by ID"""
    user = user_service.get_user_by_id('test-1')
    assert user is not None
    assert user['email'] == 'attorney1@test.com'
    
    # Test non-existent user
    assert user_service.get_user_by_id('non-existent') is None

def test_get_available_attorneys(user_service):
    """Test getting available attorneys with filters"""
    # Get all attorneys
    attorneys = user_service.get_available_attorneys({})
    assert len(attorneys) == 2
    
    # Filter by availability
    weekday_attorneys = user_service.get_available_attorneys({'availability': 'weekdays'})
    assert len(weekday_attorneys) == 1
    assert weekday_attorneys[0]['email'] == 'attorney1@test.com'
    
    # Filter by specialty
    immigration_attorneys = user_service.get_available_attorneys({'specialties': ['immigration']})
    assert len(immigration_attorneys) == 1
    assert immigration_attorneys[0]['email'] == 'attorney2@test.com'

def test_update_availability(user_service):
    """Test updating user availability"""
    new_availability = {'weekdays': True, 'weekends': False}
    updated_user = user_service.update_availability('test-1', new_availability)
    
    assert updated_user is not None
    assert updated_user['profile']['availability'] == new_availability
    assert 'updated_at' in updated_user
    
    # Test non-existent user
    assert user_service.update_availability('non-existent', {}) is None

def test_update_profile(user_service):
    """Test updating user profile"""
    profile_updates = {
        'full_name': 'Updated Name',
        'phone': '555-0123',
        'specialties': ['immigration', 'housing']
    }
    
    updated_user = user_service.update_profile('test-1', profile_updates)
    
    assert updated_user is not None
    assert updated_user['profile']['full_name'] == 'Updated Name'
    assert updated_user['profile']['phone'] == '555-0123'
    assert updated_user['profile']['specialties'] == ['immigration', 'housing']
    assert 'updated_at' in updated_user
    
    # Test non-existent user
    assert user_service.update_profile('non-existent', {}) is None
    
    # Test unauthorized field updates
    profile_updates['unauthorized_field'] = 'value'
    updated_user = user_service.update_profile('test-1', profile_updates)
    assert 'unauthorized_field' not in updated_user['profile'] 