"""
Tests for WebSocket functionality
"""
import unittest
import socketio
import json
import time
import threading
import os
import sys
from typing import Any, List, Tuple, Optional, Dict, Union
from unittest.mock import patch, MagicMock
import pytest
from flask import url_for
from flask_socketio import SocketIOTestClient

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app  # Import the Flask app factory
from backend.websocket import (
    socketio as server_socketio,
    send_notification,
    send_broadcast_notification,
    get_connected_users,
    send_user_notification,
    send_immigration_form_notification,
    NOTIFICATION_TYPE_SUCCESS,
    CATEGORY_IMMIGRATION
)
from backend.websocket.utils.persistence import (
    save_notification,
    get_notifications_for_user,
    mark_as_read
)

# Test fixtures
@pytest.fixture
def socket_client(app, client):
    """Create a test socket client"""
    from backend.websocket import socketio
    return SocketIOTestClient(app, socketio)

@pytest.fixture
def mock_emit():
    """Mock the socketio emit function"""
    with patch('flask_socketio.emit') as mock:
        yield mock

@pytest.fixture
def connected_socket_client(socket_client):
    """Create and connect a socket client"""
    socket_client.connect()
    yield socket_client
    socket_client.disconnect()

@pytest.fixture
def notification_data():
    """Sample notification data for tests"""
    return {
        'title': 'Test Notification',
        'message': 'This is a test notification',
        'type': 'info'
    }

class TestWebSocket(unittest.TestCase):
    """Test WebSocket functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        # Create and configure the app for testing
        cls.app = create_app('testing')
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG'] = False
        
        # Start the server in a thread
        cls.server_thread = threading.Thread(target=server_socketio.run, args=(cls.app,), 
                                           kwargs={'host': '127.0.0.1', 'port': 5004})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
    
    def setUp(self):
        """Set up each test"""
        # Create a SocketIO client
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
        self.client.connect('http://127.0.0.1:5004')
        
        # Clear received messages for each test
        self.received_messages = []
    
    def tearDown(self):
        """Clean up after each test"""
        # Disconnect the client
        self.client.disconnect()
    
    def test_connection(self):
        """Test basic connection to the server"""
        self.assertTrue(self.client.connected)
    
    def test_registration(self):
        """Test registering a user for notifications"""
        # Register as a test user
        response = self.client.call('register', {'user_id': 'test_user'})
        
        # Check the response
        if response is None:
            self.fail("Registration response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        self.assertEqual(response.get('message'), 'User test_user registered for notifications')
        
        # Verify that the user is connected
        connected_users = get_connected_users()
        self.assertIn('test_user', connected_users)
    
    def test_notification(self):
        """Test sending and receiving a notification"""
        # Register as a test user
        self.client.call('register', {'user_id': 'test_user_notification'})
        
        # Clear received messages
        self.received_messages = []
        
        # Send a notification
        notification_data = {
            'message': 'Test notification',
            'type': 'info'
        }
        result = send_notification(
            user_id='test_user_notification',
            title='Test Notification',
            message='Test notification',
            notification_type='info'
        )
        
        # Check that notification was sent successfully
        self.assertTrue(result)
        
        # Wait for notification to be received
        time.sleep(0.5)
        
        # Check that notification was received
        self.assertEqual(len(self.received_messages), 1)
        message_type, message_data = self.received_messages[0]
        
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('message'), 'Test notification')
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('type'), 'info')
    
    """def test_direct_message(self):
        \"\"\"Test sending and receiving a direct message\"\"\"
        # Connect and get session ID
        self.client.call('register', {'user_id': 'test_user_direct'})
        session_id = self.client.get_sid()
        
        # Clear received messages
        self.received_messages = []
        
        # Send a direct message
        message_data = {
            'message': 'Test direct message'
        }
        
        # Skip test if session_id is None
        if session_id is None:
            self.skipTest("Session ID is None, cannot proceed with test")
            return
            
        result = send_direct_message(session_id, message_data)
        
        # Check that message was sent successfully
        self.assertTrue(result)
        
        # Wait for message to be received
        time.sleep(0.5)
        
        # Check that message was received
        self.assertEqual(len(self.received_messages), 1)
        message_type, message_data = self.received_messages[0]
        
        self.assertEqual(message_type, 'direct_message')
        self.assertEqual(message_data.get('message'), 'Test direct message')
    """
    
    def test_mark_read(self):
        """Test marking notifications as read"""
        # Register as a test user
        self.client.call('register', {'user_id': 'test_user_mark_read'})
        
        # Send a notification
        notification_data = {
            'id': 'test_notification',
            'message': 'Test notification for marking read',
            'type': 'info'
        }
        send_notification(
            user_id='test_user_mark_read',
            title='Test Mark Read',
            message='Test notification for marking read',
            notification_type='info',
            data={'id': 'test_notification'}
        )
        
        # Mark notification as read
        response = self.client.call('mark_read', {'notification_id': 'test_notification'})
        
        # Check the response
        if response is None:
            self.fail("Mark read response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        
        # Get notifications and verify that it's marked as read
        response = self.client.call('get_notifications', {})
        
        if response is None:
            self.fail("Get notifications response was None")
            return
            
        self.assertEqual(response.get('status'), 'success')
        
        # Check if the notification is in the list and is marked as read
        notifications = response.get('notifications', [])
        for notification in notifications:
            if notification.get('id') == 'test_notification':
                self.assertTrue(notification.get('read'))
                break
        else:
            self.fail("Notification not found in user's notifications")

    def test_send_user_notification(self):
        """Test the send_user_notification function"""
        # Register as a test user
        self.client.call('register', {'user_id': 'test_user_custom'})
        
        # Clear received messages
        self.received_messages = []
        
        # Send a custom notification
        notification = send_user_notification(
            user_id='test_user_custom',
            title='Test Title',
            message='Test custom notification',
            notification_type=NOTIFICATION_TYPE_SUCCESS,
            data={'test_key': 'test_value'}
        )
        
        # Wait for notification to be received
        time.sleep(0.5)
        
        # Check that notification was received
        self.assertEqual(len(self.received_messages), 1)
        message_type, message_data = self.received_messages[0]
        
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('title'), 'Test Title')
        self.assertEqual(message_data.get('message'), 'Test custom notification')
        self.assertEqual(message_data.get('type'), NOTIFICATION_TYPE_SUCCESS)
        self.assertEqual(message_data.get('category'), CATEGORY_IMMIGRATION)
        self.assertEqual(message_data.get('test_key'), 'test_value')
    
    def test_immigration_form_notification(self):
        """Test the send_immigration_form_notification function"""
        # Register as a test user
        self.client.call('register', {'user_id': 'test_user_form'})
        
        # Clear received messages
        self.received_messages = []
        
        # Send a form notification
        notification = send_immigration_form_notification(
            user_id='test_user_form',
            form_type='i485',
            status='submitted',
            case_id='test_form_123'
        )
        
        # Wait for notification to be received
        time.sleep(0.5)
        
        # Check that notification was received
        self.assertEqual(len(self.received_messages), 1)
        message_type, message_data = self.received_messages[0]
        
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('title'), 'Immigration Form i485 Submitted')
        self.assertIn('i485', message_data.get('message', ''))
        self.assertEqual(message_data.get('type'), NOTIFICATION_TYPE_SUCCESS)
        self.assertEqual(message_data.get('form_type'), 'i485')
        self.assertEqual(message_data.get('case_id'), 'test_form_123')
    
    def test_broadcast_notification(self):
        """Test broadcasting a notification to all users"""
        # Register two test users
        self.client.call('register', {'user_id': 'test_user_broadcast1'})
        
        # Create a second client
        client2 = socketio.Client()
        received_messages2 = []
        
        @client2.on('notification')  # type: ignore
        def on_notification(data: Dict[str, Any]) -> None:
            received_messages2.append(('notification', data))
        
        # Connect and register the second client
        client2.connect('http://127.0.0.1:5004')
        client2.call('register', {'user_id': 'test_user_broadcast2'})
        
        # Clear received messages
        self.received_messages = []
        
        # Broadcast a notification
        result = send_broadcast_notification(
            title='Broadcast Test',
            message='Broadcast test message',
            notification_type='warning'
        )
        
        # Check that notification was sent successfully
        self.assertTrue(result)
        
        # Wait for notifications to be received
        time.sleep(0.5)
        
        # Check that both clients received the notification
        self.assertEqual(len(self.received_messages), 1)
        self.assertEqual(len(received_messages2), 1)
        
        # Check notification content for first client
        message_type, message_data = self.received_messages[0]
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('message'), 'Broadcast test message')
        self.assertEqual(message_data.get('type'), 'warning')
        
        # Check notification content for second client
        message_type, message_data = received_messages2[0]
        self.assertEqual(message_type, 'notification')
        self.assertEqual(message_data.get('message'), 'Broadcast test message')
        self.assertEqual(message_data.get('type'), 'warning')
        
        # Clean up second client
        client2.disconnect()
    
    def test_notification_error_handling(self):
        """Test error handling in notification sending"""
        # Test sending to non-existent user
        result = send_notification(
            user_id='non_existent_user',
            title='Test Error',
            message='Test message',
            notification_type='info'
        )
        
        # Should still return True because the message was persisted
        self.assertTrue(result)
        
        # Test sending with invalid notification data
        with patch('websocket.services.notification_service.save_notification', side_effect=Exception('Test error')):
            result = send_notification(
                user_id='test_user',
                title='Test Error',
                message='Test with error',
                notification_type='info'
            )
            # Should return False because there was an error
            self.assertFalse(result)
    
    def test_persistence(self):
        """Test notification persistence"""
        # Save a notification
        user_id = 'test_persistence_user'
        notification_data = {
            'id': 'persist_test_notification',
            'message': 'Test persistence',
            'type': 'info',
            'timestamp': '2023-01-01T00:00:00',
            'read': False
        }
        
        # Save the notification
        notification_id = save_notification(user_id, notification_data)
        
        # Get notifications for the user
        notifications = get_notifications_for_user(user_id)
        
        # Check that the notification was saved
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].get('id'), 'persist_test_notification')
        self.assertEqual(notifications[0].get('message'), 'Test persistence')
        
        # Mark as read
        result = mark_as_read(user_id, ['persist_test_notification'])
        self.assertTrue(result)
        
        # Check that it's now marked as read
        notifications = get_notifications_for_user(user_id)
        self.assertEqual(len(notifications), 1)
        self.assertTrue(notifications[0].get('read'))

@pytest.mark.websocket
def test_websocket_connection(socketio_client):
    """Test basic WebSocket connection"""
    assert socketio_client.connected

@pytest.mark.websocket
def test_notification_broadcast_http(socketio_client, client, auth_headers, notification_data):
    """Test broadcasting notifications via HTTP endpoint"""
    received_data = []
    
    @socketio_client.on('notification')
    def handle_notification(data):
        received_data.append(data)
    
    response = client.post(
        '/api/notifications/broadcast',
        json=notification_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    
    # Wait for WebSocket event
    time.sleep(1)
    
    # Verify notification was received
    assert len(received_data) == 1
    assert received_data[0]['title'] == notification_data['title']
    assert received_data[0]['message'] == notification_data['message']

@pytest.mark.websocket
def test_chat_message(socketio_client):
    """Test sending and receiving chat messages"""
    received_messages = []
    
    @socketio_client.on('chat_message')
    def handle_message(data):
        received_messages.append(data)
    
    message_data = {
        'room': 'test_room',
        'message': 'Hello, World!',
        'sender': 'test_user'
    }
    socketio_client.emit('send_message', message_data)
    
    time.sleep(1)
    
    assert len(received_messages) == 1
    assert received_messages[0]['message'] == message_data['message']
    assert received_messages[0]['sender'] == message_data['sender']

@pytest.mark.websocket
def test_room_join_leave(socketio_client):
    """Test joining and leaving chat rooms"""
    room_events = []
    
    @socketio_client.on('room_event')
    def handle_room_event(data):
        room_events.append(data)
    
    socketio_client.emit('join_room', {'room': 'test_room'})
    time.sleep(0.5)
    
    socketio_client.emit('leave_room', {'room': 'test_room'})
    time.sleep(0.5)
    
    assert len(room_events) == 2
    assert room_events[0]['action'] == 'join'
    assert room_events[1]['action'] == 'leave'
    assert all(event['room'] == 'test_room' for event in room_events)

@pytest.mark.websocket
def test_websocket_error_handling(socketio_client):
    """Test WebSocket error handling for invalid message data"""
    error_messages = []
    
    @socketio_client.on('error')
    def handle_error(data):
        error_messages.append(data)
    
    socketio_client.emit('send_message', {})
    time.sleep(0.5)
    
    assert len(error_messages) == 1
    assert 'error' in error_messages[0]
    assert 'message' in error_messages[0]['error']

# Socket client tests
def test_socket_client_connection(connected_socket_client):
    """Test client connection and disconnection"""
    assert connected_socket_client.is_connected()

def test_socket_client_notification(connected_socket_client, mock_emit, notification_data):
    """Test receiving notifications with socket client"""
    connected_socket_client.emit('notification', notification_data)
    
    received = connected_socket_client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'notification'
    assert received[0]['args'][0]['message'] == notification_data['message']

def test_socket_client_broadcast(connected_socket_client, mock_emit, notification_data):
    """Test broadcasting notifications to all clients"""
    connected_socket_client.emit('broadcast', notification_data)
    mock_emit.assert_called_with('notification', notification_data, broadcast=True)

def test_socket_client_room_notification(connected_socket_client, mock_emit, notification_data):
    """Test sending notifications to specific rooms"""
    room = 'test_room'
    connected_socket_client.emit('join', {'room': room})
    connected_socket_client.emit('room_notification', {'room': room, 'data': notification_data})
    mock_emit.assert_called_with('notification', notification_data, room=room)

def test_socket_client_error_handling(connected_socket_client):
    """Test error handling in WebSocket communications with invalid notification format"""
    invalid_data = {'invalid': 'data'}
    connected_socket_client.emit('notification', invalid_data)
    
    received = connected_socket_client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'error'
    assert 'Invalid notification format' in received[0]['args'][0]['message']

if __name__ == '__main__':
    unittest.main() 