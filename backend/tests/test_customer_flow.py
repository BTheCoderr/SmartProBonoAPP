"""
End-to-end tests for customer flow
"""
import unittest
import json
import time
from io import BytesIO
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import pytest
from bson import ObjectId
from pymongo.database import Database
from pymongo.collection import Collection
from flask import Flask

from backend.app import create_app
from database.mongo import mongo
from websocket import socketio
from models.user import User

def init_mongo(app) -> Database:
    """Initialize MongoDB connection"""
    with app.app_context():
        mongo.init_client()
        if not isinstance(mongo.db, Database):
            raise RuntimeError("Failed to initialize MongoDB")
        return mongo.db

def clear_collections(db: Database) -> None:
    """Clear all test collections"""
    collections = ['users', 'cases', 'documents', 'notifications', 'intakes']
    for collection in collections:
        db[collection].delete_many({})

@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    test_config = {
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/smartprobono_test',
        'SECRET_KEY': 'test_secret_key',
        'JWT_SECRET_KEY': 'test_jwt_secret',
        'MAIL_SUPPRESS_SEND': True
    }
    app = create_app(test_config)
    
    # Initialize MongoDB for testing
    db = init_mongo(app)
    clear_collections(db)
    
    yield app
    
    # Cleanup after all tests
    with app.app_context():
        db = init_mongo(app)  # Re-initialize to ensure we have a valid connection
        clear_collections(db)
        mongo.close()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    # Register and login a test user
    test_user = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'firstName': 'Test',
        'lastName': 'User'
    }
    
    # Register
    client.post('/api/auth/register', json=test_user)
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': test_user['email'],
        'password': test_user['password']
    })
    
    token = json.loads(response.data)['access_token']
    return {'Authorization': f'Bearer {token}'}

class TestCustomerFlow(unittest.TestCase):
    """Test the entire customer journey"""
    
    def setUp(self):
        """Set up test environment"""
        test_config = {
            'TESTING': True,
            'MONGO_URI': 'mongodb://localhost:27017/smartprobono_test',
            'SECRET_KEY': 'test_secret_key',
            'JWT_SECRET_KEY': 'test_jwt_secret',
            'MAIL_SUPPRESS_SEND': True
        }
        
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Initialize MongoDB
        self.db = init_mongo(self.app)
        clear_collections(self.db)
        
        # Create test user
        self.test_user = {
            '_id': ObjectId(),
            'email': f'test_{ObjectId()}@example.com',
            'password': 'testpass123',
            'firstName': 'Test',
            'lastName': 'User',
            'role': 'user',
            'active': True,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow()
        }
        self.db.users.insert_one(self.test_user)
    
    def tearDown(self):
        """Clean up after tests"""
        if isinstance(self.db, Database):
            clear_collections(self.db)
        self.app_context.pop()
    
    def test_registration_and_login(self):
        """Test user registration and login process"""
        # Test registration
        registration_data = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'firstName': 'New',
            'lastName': 'User'
        }
        
        response = self.client.post('/api/auth/register', json=registration_data)
        self.assertEqual(response.status_code, 201)
        
        # Verify user was created in MongoDB
        user = self.db.users.find_one({'email': registration_data['email']})
        self.assertIsNotNone(user)
        self.assertEqual(user['firstName'], registration_data['firstName'])
        
        # Test login
        login_data = {
            'email': registration_data['email'],
            'password': registration_data['password']
        }
        
        response = self.client.post('/api/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        
        # Test invalid login
        response = self.client.post('/api/auth/login', json={
            'email': registration_data['email'],
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)
    
    def test_profile_completion(self):
        """Test profile completion flow"""
        # Register and login
        auth_headers = self._get_auth_headers()
        
        # Update profile
        profile_data = {
            'phone': '123-456-7890',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip': '12345',
            'preferredLanguage': 'en',
            'notificationPreferences': {
                'email': True,
                'sms': False
            }
        }
        
        response = self.client.put(
            '/api/users/profile',
            headers=auth_headers,
            json=profile_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify profile update
        response = self.client.get('/api/users/profile', headers=auth_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['phone'], profile_data['phone'])
    
    def test_immigration_intake_flow(self):
        """Test immigration intake form submission and processing"""
        auth_headers = self._get_auth_headers()
        
        # Submit intake form
        intake_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'dateOfBirth': '1990-01-01',
            'immigrationStatus': 'permanent_resident',
            'visaType': 'employment',
            'urgency': 'medium',
            'caseDescription': 'Need assistance with citizenship application',
            'hasLegalRepresentation': 'no',
            'priorApplications': False
        }
        
        response = self.client.post(
            '/api/intake/immigration',
            headers=auth_headers,
            json=intake_data
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        intake_id = data['id']
        
        # Verify intake creation
        response = self.client.get(
            f'/api/intake/{intake_id}',
            headers=auth_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Test document upload for intake
        test_file = (BytesIO(b'test file content'), 'test.pdf')
        response = self.client.post(
            f'/api/intake/{intake_id}/documents',
            headers=auth_headers,
            data={'file': test_file, 'document_type': 'identification'}
        )
        self.assertEqual(response.status_code, 201)
    
    def test_document_management(self):
        """Test document upload and management"""
        auth_headers = self._get_auth_headers()
        
        # Upload document
        test_file = (BytesIO(b'test file content'), 'test.pdf')
        response = self.client.post(
            '/api/documents/upload',
            headers=auth_headers,
            data={'file': test_file, 'documentType': 'identification'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        document_id = data['id']
        
        # Get document
        response = self.client.get(
            f'/api/documents/{document_id}',
            headers=auth_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Test document scanning
        response = self.client.post(
            '/api/documents/scan',
            headers=auth_headers,
            data={'file': test_file, 'documentType': 'identification'}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_notification_system(self):
        """Test notification delivery and management"""
        auth_headers = self._get_auth_headers()
        
        # Connect to WebSocket
        socketio_client = socketio.test_client(self.app)
        self.assertTrue(socketio_client.is_connected())
        
        # Register for notifications
        user_id = self._get_user_id_from_headers(auth_headers)
        socketio_client.emit('register', {'user_id': user_id})
        
        # Send a test notification
        notification_data = {
            'title': 'Test Notification',
            'message': 'This is a test notification',
            'type': 'info'
        }
        response = self.client.post(
            '/api/notifications/send',
            headers=auth_headers,
            json=notification_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Wait for notification
        time.sleep(0.5)
        
        # Check received notifications
        received = socketio_client.get_received()
        self.assertTrue(any(msg['name'] == 'notification' for msg in received))
        
        # Mark notification as read
        response = self.client.put(
            '/api/notifications/mark-read',
            headers=auth_headers,
            json={'notification_ids': [notification_data['id']]}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_case_status_updates(self):
        """Test case status updates and notifications"""
        auth_headers = self._get_auth_headers()
        
        # Create a test case
        case_data = {
            'type': 'immigration',
            'subtype': 'citizenship',
            'status': 'new',
            'priority': 'medium',
            'description': 'Test case'
        }
        
        response = self.client.post(
            '/api/cases',
            headers=auth_headers,
            json=case_data
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        case_id = data['id']
        
        # Update case status
        update_data = {
            'status': 'in_progress',
            'notes': 'Case is being processed'
        }
        
        response = self.client.put(
            f'/api/cases/{case_id}/status',
            headers=auth_headers,
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify status update
        response = self.client.get(
            f'/api/cases/{case_id}',
            headers=auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'in_progress')
    
    def _get_auth_headers(self):
        """Helper method to get authentication headers"""
        # Register and login a test user
        test_user = {
            'email': f'test_{ObjectId()}@example.com',
            'password': 'testpass123',
            'firstName': 'Test',
            'lastName': 'User'
        }
        
        self.client.post('/api/auth/register', json=test_user)
        response = self.client.post('/api/auth/login', json={
            'email': test_user['email'],
            'password': test_user['password']
        })
        
        token = json.loads(response.data)['access_token']
        return {'Authorization': f'Bearer {token}'}
    
    def _get_user_id_from_headers(self, headers):
        """Helper method to get user ID from auth headers"""
        token = headers['Authorization'].split(' ')[1]
        # In a real app, you would decode the JWT token
        # For testing, we can get the user from the database
        if not isinstance(self.db, Database) or not hasattr(self.db, 'users'):
            return None
        user = self.db.users.find_one({'email': self.test_user['email']})
        return str(user['_id']) if user else None

if __name__ == '__main__':
    unittest.main() 