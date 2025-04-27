"""
End-to-end tests for WebSocket functionality
"""
import unittest
import socketio
import json
import time
import threading
import os
import sys
import requests
from typing import Any, List, Tuple, Optional, Dict, Union
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app  # Import the Flask app factory
from backend.websocket import socketio as server_socketio

class TestWebSocketE2E(unittest.TestCase):
    """End-to-end tests for WebSocket functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        # Configure the app for testing
        test_config = {
            'TESTING': True,
            'DEBUG': False,
            'SECRET_KEY': 'test_key',
            'JWT_SECRET_KEY': 'test_jwt_key'
        }
        cls.app = create_app(test_config)
        
        # Start the server in a thread
        cls.server_thread = threading.Thread(target=server_socketio.run, args=(cls.app,), 
                                           kwargs={'host': '127.0.0.1', 'port': 5005})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
        
        # Base URL for API requests
        cls.base_url = 'http://127.0.0.1:5005'
    
    def setUp(self):
        """Set up each test"""
        # Create a SocketIO client (simulating a browser)
        self.client = socketio.Client()
        self.received_messages: List[Tuple[str, Any]] = []
        
        # Set up callbacks
        @self.client.on('notification')  # type: ignore
        def on_notification(data: Dict[str, Any]) -> None:
            self.received_messages.append(('notification', data))
        
        @self.client.on('direct_message')  # type: ignore
        def on_direct_message(data: Dict[str, Any]) -> None:
            self.received_messages.append(('direct_message', data))
        
        # Connect to the server
        self.client.connect(f'{self.base_url}')
        
        # Clear received messages for each test
        self.received_messages = []
    
    def tearDown(self):
        """Clean up after each test"""
        # Disconnect the client
        self.client.disconnect()
    
    def test_e2e_form_submission_notification(self):
        """
        Test end-to-end form submission notification flow:
        1. Register a user via WebSocket
        2. Make an API call to submit a form
        3. Verify that a notification is received via WebSocket
        """
        # Register as a test user
        user_id = 'test_e2e_user'
        response = self.client.call('register', {'user_id': user_id})
        
        # Check successful registration
        if response is None:
            self.fail("Registration response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        
        # Prepare mock JWT token
        mock_token = f"Bearer mock_token_for_{user_id}"
        
        # Make API call to submit a form
        headers = {
            'Authorization': mock_token,
            'Content-Type': 'application/json'
        }
        form_data = {
            'form_id': 'test_form_e2e',
            'form_type': 'i485_application'
        }
        
        # Mock the JWT verify to always return our test user
        with patch('flask_jwt_extended.view_decorators.verify_jwt_in_request') as mock_jwt:
            with patch('flask_jwt_extended.utils.get_jwt_identity', return_value=user_id):
                # Make API call to submit a form notification
                response = requests.post(
                    f'{self.base_url}/api/notifications/immigration/form-submitted',
                    headers=headers,
                    json=form_data
                )
        
        # Check API response
        self.assertEqual(response.status_code, 200)
        
        # Wait for WebSocket notification
        time.sleep(0.5)
        
        # Verify that a notification was received
        self.assertGreaterEqual(len(self.received_messages), 1)
        
        # Find the form submission notification
        form_notification = None
        for msg_type, msg_data in self.received_messages:
            if msg_type == 'notification' and msg_data.get('category') == 'immigration':
                if msg_data.get('formId') == 'test_form_e2e':
                    form_notification = msg_data
                    break
        
        # Verify notification content
        self.assertIsNotNone(form_notification, "Form submission notification not received")
        if form_notification:
            self.assertEqual(form_notification.get('type'), 'success')
            self.assertIn('i485_application', form_notification.get('message', ''))
    
    def test_e2e_status_update(self):
        """
        Test end-to-end case status update notification flow:
        1. Register a user via WebSocket
        2. Make an API call to update a case status
        3. Verify that a notification is received via WebSocket
        """
        # Register as a test user
        user_id = 'test_e2e_status_user'
        response = self.client.call('register', {'user_id': user_id})
        
        # Check successful registration
        if response is None:
            self.fail("Registration response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        
        # Prepare mock JWT token
        mock_token = f"Bearer mock_token_for_{user_id}"
        
        # Make API call to update status
        headers = {
            'Authorization': mock_token,
            'Content-Type': 'application/json'
        }
        status_data = {
            'case_id': 'case_123',
            'old_status': 'pending',
            'new_status': 'approved'
        }
        
        # Mock the JWT verify to always return our test user
        with patch('flask_jwt_extended.view_decorators.verify_jwt_in_request') as mock_jwt:
            with patch('flask_jwt_extended.utils.get_jwt_identity', return_value=user_id):
                # Make API call to update status
                response = requests.post(
                    f'{self.base_url}/api/notifications/immigration/status-update',
                    headers=headers,
                    json=status_data
                )
        
        # Check API response
        self.assertEqual(response.status_code, 200)
        
        # Wait for WebSocket notification
        time.sleep(0.5)
        
        # Verify that a notification was received
        self.assertGreaterEqual(len(self.received_messages), 1)
        
        # Find the status update notification
        status_notification = None
        for msg_type, msg_data in self.received_messages:
            if msg_type == 'notification' and msg_data.get('category') == 'immigration':
                if msg_data.get('caseId') == 'case_123':
                    status_notification = msg_data
                    break
        
        # Verify notification content
        self.assertIsNotNone(status_notification, "Status update notification not received")
        if status_notification:
            self.assertEqual(status_notification.get('type'), 'success')
            self.assertIn('approved', status_notification.get('message', ''))
    
    def test_e2e_test_notification_endpoint(self):
        """
        Test the test notification endpoint:
        1. Register a user via WebSocket
        2. Make an API call to send a test notification
        3. Verify that a notification is received via WebSocket
        """
        # Register as a test user
        user_id = 'test_e2e_api_user'
        response = self.client.call('register', {'user_id': user_id})
        
        # Check successful registration
        if response is None:
            self.fail("Registration response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        
        # Make API call to send test notification
        response = requests.post(
            f'{self.base_url}/api/test/notification/{user_id}',
            json={
                'message': 'E2E test notification',
                'type': 'info'
            }
        )
        
        # Check API response
        self.assertEqual(response.status_code, 200)
        
        # Wait for WebSocket notification
        time.sleep(0.5)
        
        # Verify that a notification was received
        self.assertGreaterEqual(len(self.received_messages), 1)
        
        # Find the test notification
        test_notification = None
        for msg_type, msg_data in self.received_messages:
            if msg_type == 'notification' and msg_data.get('message') == 'E2E test notification':
                test_notification = msg_data
                break
        
        # Verify notification content
        self.assertIsNotNone(test_notification, "Test notification not received")
        if test_notification:
            self.assertEqual(test_notification.get('type'), 'info')

    def test_e2e_connection_stats(self):
        """
        Test WebSocket connection statistics API:
        1. Connect multiple clients
        2. Call the stats API
        3. Verify that the stats are accurate
        """
        # Register the first user (self.client is already connected)
        user_id_1 = 'test_stats_user1'
        response = self.client.call('register', {'user_id': user_id_1})
        
        # Check successful registration
        if response is None:
            self.fail("Registration response was None")
            return
            
        # Connect two more clients
        client2 = socketio.Client()
        client3 = socketio.Client()
        
        try:
            # Connect clients
            client2.connect(f'{self.base_url}')
            client3.connect(f'{self.base_url}')
            
            # Register users
            client2.call('register', {'user_id': 'test_stats_user2'})
            client3.call('register', {'user_id': 'test_stats_user3'})
            
            # Wait for registration to complete
            time.sleep(0.5)
            
            # Call the stats API
            response = requests.get(f'{self.base_url}/api/test/websocket-stats')
            
            # Check response
            self.assertEqual(response.status_code, 200)
            stats = response.json()
            
            # Validate stats
            self.assertIn('connected_users', stats)
            self.assertIn('total_connections', stats)
            
            # Should have at least our 3 test users
            self.assertGreaterEqual(stats['connected_users'], 3)
            self.assertGreaterEqual(stats['total_connections'], 3)
            
        finally:
            # Clean up
            if client2.connected:
                client2.disconnect()
            if client3.connected:
                client3.disconnect()

if __name__ == '__main__':
    unittest.main() 