import unittest
import json
from flask import current_app

from backend.app import create_app
from database import db
from models.user import User

class NavigationFlowsTest(unittest.TestCase):
    """Test class for core navigation flows."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create different types of users
        # Client user
        self.client_user = User(
            email='client@example.com',
            first_name='Client',
            last_name='User',
            role='client'
        )
        self.client_user.set_password('Test1234!')
        
        # Attorney user
        self.attorney_user = User(
            email='attorney@example.com',
            first_name='Attorney',
            last_name='User',
            role='attorney'
        )
        self.attorney_user.set_password('Test1234!')
        
        # Admin user
        self.admin_user = User(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        self.admin_user.set_password('Test1234!')
        
        db.session.add_all([self.client_user, self.attorney_user, self.admin_user])
        db.session.commit()
        
    def tearDown(self):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _login_user(self, email, password):
        """Helper to login a user and get auth token."""
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': email,
                'password': password
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        return data['token']
    
    def test_health_endpoint(self):
        """Test API health endpoint."""
        response = self.client.get('/api/health')
        data = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_client_navigation_flow(self):
        """Test core navigation flow for client users."""
        # Login as client
        token = self._login_user('client@example.com', 'Test1234!')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Access profile - should be allowed
        profile_response = self.client.get(
            '/api/user/profile',
            headers=headers
        )
        self.assertEqual(profile_response.status_code, 200)
        
        # Access forms dashboard - should be allowed
        forms_response = self.client.get(
            '/api/forms',
            headers=headers
        )
        self.assertEqual(forms_response.status_code, 200)
        
        # Access documents - should be allowed
        docs_response = self.client.get(
            '/api/documents',
            headers=headers
        )
        self.assertEqual(docs_response.status_code, 200)
        
        # Try to access admin dashboard - should be denied
        admin_response = self.client.get(
            '/api/admin/dashboard',
            headers=headers
        )
        self.assertEqual(admin_response.status_code, 403)
    
    def test_attorney_navigation_flow(self):
        """Test core navigation flow for attorney users."""
        # Login as attorney
        token = self._login_user('attorney@example.com', 'Test1234!')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Access profile - should be allowed
        profile_response = self.client.get(
            '/api/user/profile',
            headers=headers
        )
        self.assertEqual(profile_response.status_code, 200)
        
        # Access case management - should be allowed
        cases_response = self.client.get(
            '/api/cases',
            headers=headers
        )
        self.assertEqual(cases_response.status_code, 200)
        
        # Access client list - should be allowed
        clients_response = self.client.get(
            '/api/clients',
            headers=headers
        )
        self.assertEqual(clients_response.status_code, 200)
        
        # Access templates - should be allowed
        templates_response = self.client.get(
            '/api/templates',
            headers=headers
        )
        self.assertEqual(templates_response.status_code, 200)
        
        # Try to access admin dashboard - should be denied
        admin_response = self.client.get(
            '/api/admin/dashboard',
            headers=headers
        )
        self.assertEqual(admin_response.status_code, 403)
    
    def test_admin_navigation_flow(self):
        """Test core navigation flow for admin users."""
        # Login as admin
        token = self._login_user('admin@example.com', 'Test1234!')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Access profile - should be allowed
        profile_response = self.client.get(
            '/api/user/profile',
            headers=headers
        )
        self.assertEqual(profile_response.status_code, 200)
        
        # Access admin dashboard - should be allowed
        admin_response = self.client.get(
            '/api/admin/dashboard',
            headers=headers
        )
        self.assertEqual(admin_response.status_code, 200)
        
        # Access user management - should be allowed
        users_response = self.client.get(
            '/api/admin/users',
            headers=headers
        )
        self.assertEqual(users_response.status_code, 200)
        
        # Access system settings - should be allowed
        settings_response = self.client.get(
            '/api/admin/settings',
            headers=headers
        )
        self.assertEqual(settings_response.status_code, 200)
    
    def test_unauthenticated_access(self):
        """Test accessing protected endpoints without authentication."""
        # Try to access profile without auth
        profile_response = self.client.get('/api/user/profile')
        self.assertEqual(profile_response.status_code, 401)
        
        # Try to access forms without auth
        forms_response = self.client.get('/api/forms')
        self.assertEqual(forms_response.status_code, 401)
        
        # Try to access documents without auth
        docs_response = self.client.get('/api/documents')
        self.assertEqual(docs_response.status_code, 401)
        
        # Public endpoints should still be accessible
        health_response = self.client.get('/api/health')
        self.assertEqual(health_response.status_code, 200)
    
    def test_navigation_between_pages(self):
        """Test navigation between key pages in the application."""
        # Login as client
        token = self._login_user('client@example.com', 'Test1234!')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Check dashboard first (simulates landing page after login)
        dashboard_response = self.client.get(
            '/api/dashboard',
            headers=headers
        )
        self.assertEqual(dashboard_response.status_code, 200)
        
        # Navigate to forms
        forms_response = self.client.get(
            '/api/forms',
            headers=headers
        )
        self.assertEqual(forms_response.status_code, 200)
        
        # Navigate to documents
        docs_response = self.client.get(
            '/api/documents',
            headers=headers
        )
        self.assertEqual(docs_response.status_code, 200)
        
        # Navigate to profile
        profile_response = self.client.get(
            '/api/user/profile',
            headers=headers
        )
        self.assertEqual(profile_response.status_code, 200)
        
        # Navigate back to dashboard
        dashboard_response = self.client.get(
            '/api/dashboard',
            headers=headers
        )
        self.assertEqual(dashboard_response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main() 