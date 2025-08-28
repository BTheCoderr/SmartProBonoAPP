import unittest
import json
import jwt
from datetime import datetime, timedelta
from flask import current_app

from backend.app import create_app
from database import db
from models.user import User

class AuthSystemTest(unittest.TestCase):
    """Test class for authentication system."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.test_user = {
            'email': 'test@example.com',
            'password': 'Test1234!',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'client'
        }
        
        # JWT secret key for token validation
        self.jwt_secret_key = self.app.config['JWT_SECRET_KEY']
        
    def tearDown(self):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_registration(self):
        """Test user registration."""
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertTrue(data['user_id'])
        
        # Verify user in database
        user = User.query.filter_by(email=self.test_user['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.test_user['email'])
        self.assertEqual(user.first_name, self.test_user['first_name'])
        self.assertEqual(user.role, self.test_user['role'])
        
    def test_login(self):
        """Test user login and JWT token generation."""
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
        self.assertTrue(data['user'])
        
        # Decode and verify token
        token = data['token']
        token_data = jwt.decode(token, self.jwt_secret_key, algorithms=['HS256'])
        self.assertTrue('exp' in token_data)
        self.assertTrue('sub' in token_data)
        self.assertTrue('roles' in token_data)
    
    def test_protected_route(self):
        """Test accessing protected route with JWT token."""
        # Register and login to get token
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
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
        
        # Access protected route with token
        protected_response = self.client.get(
            '/api/user/profile',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        
        self.assertEqual(protected_response.status_code, 200)
        
        # Access without token should fail
        unauth_response = self.client.get('/api/user/profile')
        self.assertEqual(unauth_response.status_code, 401)
    
    def test_token_expiration(self):
        """Test JWT token expiration."""
        # Create a user manually to have control over the token
        user = User(
            email=self.test_user['email'],
            first_name=self.test_user['first_name'],
            last_name=self.test_user['last_name'],
            role=self.test_user['role']
        )
        user.set_password(self.test_user['password'])
        db.session.add(user)
        db.session.commit()
        
        # Generate expired token
        exp_time = datetime.utcnow() - timedelta(hours=1)
        expired_token_payload = {
            'sub': str(user.id),
            'roles': [user.role],
            'exp': exp_time
        }
        expired_token = jwt.encode(
            expired_token_payload, 
            self.jwt_secret_key, 
            algorithm='HS256'
        )
        
        # Access protected route with expired token
        response = self.client.get(
            '/api/user/profile',
            headers={
                'Authorization': f'Bearer {expired_token}'
            }
        )
        
        self.assertEqual(response.status_code, 401)
        
    def test_token_refresh(self):
        """Test refreshing JWT token."""
        # Register and login to get token
        self.client.post(
            '/api/auth/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
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
        
        # Refresh token
        refresh_response = self.client.post(
            '/api/auth/refresh',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        
        refresh_data = json.loads(refresh_response.data.decode())
        self.assertEqual(refresh_response.status_code, 200)
        self.assertTrue('token' in refresh_data)
        self.assertNotEqual(token, refresh_data['token'])

if __name__ == '__main__':
    unittest.main() 