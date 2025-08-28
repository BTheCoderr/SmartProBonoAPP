import unittest
import json
from flask import current_app

from backend.app import create_app
from database import db
from models.user import User
from models.form import Form

class FormSubmissionTest(unittest.TestCase):
    """Test class for form submission functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='client'
        )
        self.user.set_password('Test1234!')
        db.session.add(self.user)
        db.session.commit()
        
        # Login and get auth token
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'Test1234!'
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.token = data['token']
        self.auth_headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        # Test form data
        self.test_intake_form = {
            'form_type': 'client_intake',
            'data': {
                'personal_info': {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'johndoe@example.com',
                    'phone': '555-123-4567',
                    'address': '123 Main St',
                    'city': 'Anytown',
                    'state': 'CA',
                    'zip': '12345'
                },
                'legal_info': {
                    'issue_type': 'immigration',
                    'description': 'Need help with visa application',
                    'urgency': 'medium'
                }
            }
        }
        
    def tearDown(self):
        """Clean up test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_form_submission(self):
        """Test submitting a form and saving it to the database."""
        # Submit form
        response = self.client.post(
            '/api/forms',
            data=json.dumps(self.test_intake_form),
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'Form submitted successfully')
        self.assertTrue('form' in data)
        
        # Verify form in database
        form_id = data['form'].get('id')
        form = Form.query.get(form_id)
        self.assertIsNotNone(form)
        self.assertEqual(form.form_type, 'client_intake')
        self.assertEqual(form.user_id, self.user.id)
        self.assertEqual(form.status, 'submitted')
        self.assertEqual(form.data['personal_info']['first_name'], 'John')
    
    def test_form_draft(self):
        """Test saving a form as draft and then submitting it."""
        # Save as draft
        draft_form = dict(self.test_intake_form)
        draft_form['status'] = 'draft'
        
        draft_response = self.client.post(
            '/api/forms',
            data=json.dumps(draft_form),
            headers=self.auth_headers
        )
        
        draft_data = json.loads(draft_response.data.decode())
        self.assertEqual(draft_response.status_code, 201)
        self.assertEqual(draft_data['form']['status'], 'draft')
        form_id = draft_data['form'].get('id')
        
        # Update draft
        updated_form = dict(self.test_intake_form)
        updated_form['data']['personal_info']['first_name'] = 'Jane'
        updated_form['status'] = 'submitted'
        
        update_response = self.client.put(
            f'/api/forms/{form_id}',
            data=json.dumps(updated_form),
            headers=self.auth_headers
        )
        
        update_data = json.loads(update_response.data.decode())
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_data['form']['status'], 'submitted')
        
        # Verify updated form
        form = Form.query.get(form_id)
        self.assertEqual(form.status, 'submitted')
        self.assertEqual(form.data['personal_info']['first_name'], 'Jane')
        self.assertIsNotNone(form.submitted_at)
    
    def test_form_retrieval(self):
        """Test retrieving forms for a user."""
        # Submit multiple forms
        for i in range(3):
            form_data = dict(self.test_intake_form)
            form_data['data']['personal_info']['first_name'] = f'User{i}'
            
            self.client.post(
                '/api/forms',
                data=json.dumps(form_data),
                headers=self.auth_headers
            )
        
        # Get form list
        response = self.client.get(
            '/api/forms',
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('forms' in data)
        self.assertEqual(len(data['forms']), 3)
    
    def test_form_validation(self):
        """Test form validation."""
        # Create invalid form (missing required fields)
        invalid_form = {
            'form_type': 'client_intake',
            'data': {
                'personal_info': {
                    # Missing first_name and last_name
                    'email': 'incomplete@example.com'
                }
            }
        }
        
        response = self.client.post(
            '/api/forms',
            data=json.dumps(invalid_form),
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in data)
        self.assertTrue('validation_errors' in data)
    
    def test_form_processing(self):
        """Test form processing and status updates."""
        # Submit a form
        response = self.client.post(
            '/api/forms',
            data=json.dumps(self.test_intake_form),
            headers=self.auth_headers
        )
        
        data = json.loads(response.data.decode())
        form_id = data['form'].get('id')
        
        # Create attorney user to process the form
        attorney = User(
            email='attorney@example.com',
            first_name='Attorney',
            last_name='User',
            role='attorney'
        )
        attorney.set_password('Test1234!')
        db.session.add(attorney)
        db.session.commit()
        
        # Login as attorney
        attorney_login = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'email': 'attorney@example.com',
                'password': 'Test1234!'
            }),
            content_type='application/json'
        )
        attorney_token = json.loads(attorney_login.data.decode())['token']
        attorney_headers = {
            'Authorization': f'Bearer {attorney_token}',
            'Content-Type': 'application/json'
        }
        
        # Process form (attorney updates status)
        process_response = self.client.put(
            f'/api/forms/{form_id}/status',
            data=json.dumps({
                'status': 'approved',
                'notes': 'Form approved and processing'
            }),
            headers=attorney_headers
        )
        
        process_data = json.loads(process_response.data.decode())
        self.assertEqual(process_response.status_code, 200)
        self.assertEqual(process_data['form']['status'], 'approved')
        
        # Verify form status in database
        form = Form.query.get(form_id)
        self.assertEqual(form.status, 'approved')
        
if __name__ == '__main__':
    unittest.main() 