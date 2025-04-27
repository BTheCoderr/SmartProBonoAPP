import unittest
import json
import os
import time
import jwt
from flask import Flask
from backend.app import create_app
from backend.extensions import db, mongo
from backend.models.user import User

class AuthenticationTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test client and initialize database."""
        # Create test app instance
        flask_app = create_app()
        # Save the original database URI to restore it after tests
        self.original_db_uri = flask_app.config.get('SQLALCHEMY_DATABASE_URI')
        # Configure app for testing
        flask_app.config['TESTING'] = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.app = flask_app
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all tables in the in-memory database
        db.create_all()
        
        self.client = self.app.test_client()
        
        # Test user data
        self.test_user = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test@123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # JWT secret key
        self.jwt_secret_key = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key')

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        
        # Restore original database URI if it existed
        if self.original_db_uri:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.original_db_uri
            
        self.app_context.pop()

    def test_register_user(self):
        """Test user registration."""
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertTrue(data['user']['id'] > 0)
        self.assertEqual(data['user']['username'], self.test_user['username'])
        self.assertEqual(data['user']['email'], self.test_user['email'])
        self.assertNotIn('password', data['user'])

    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        # Register user first
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Try to register again with same email
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 409)
        self.assertEqual(data['message'], 'User with this email already exists')

    def test_login_user(self):
        """Test user login."""
        # Register user first
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Login with registered user
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Login successful')
        self.assertTrue(data['token'])
        self.assertEqual(data['user']['email'], self.test_user['email'])
        
        # Decode and verify token
        token_data = jwt.decode(data['token'], self.jwt_secret_key, algorithms=['HS256'])
        self.assertEqual(token_data['role'], 'client')
        self.assertTrue('exp' in token_data)
        self.assertTrue('user_id' in token_data)

    def test_login_incorrect_password(self):
        """Test login with incorrect password."""
        # Register user first
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Login with incorrect password
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': self.test_user['email'],
                'password': 'wrong_password'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], 'Invalid email or password')

    def test_get_user_profile(self):
        """Test getting user profile."""
        # Register user first
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Login to get token
        login_response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }),
            content_type='application/json'
        )
        login_data = json.loads(login_response.data.decode())
        token = login_data['token']
        
        # Get user profile with token
        response = self.client.get(
            '/api/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user']['email'], self.test_user['email'])
        self.assertEqual(data['user']['username'], self.test_user['username'])

    def test_update_profile(self):
        """Test updating user profile."""
        # Register user first
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Login to get token
        login_response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }),
            content_type='application/json'
        )
        login_data = json.loads(login_response.data.decode())
        token = login_data['token'] 