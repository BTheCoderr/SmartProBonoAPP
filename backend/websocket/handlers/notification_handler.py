"""
Notification event handler for WebSockets.

This module handles WebSocket events related to notifications including
retrieval, marking as read, and responding to notification actions.
"""

import logging
from flask import current_app
from flask_socketio import emit

from ..services.notification_service import (
    send_notification,
    mark_notification_read,
    get_user_notifications,
    get_notification_stats
)
from ..services.connection_service import is_user_connected
from ..utils.auth import validate_jwt

# Configure logging
logger = logging.getLogger('websocket.handlers.notification')

def handle_get_notifications(data):
    """
    Handle event to retrieve a user's notifications.
    
    Args:
        data (dict): Contains user_id and optional filters
    """
    if not data or not isinstance(data, dict):
        emit('notifications_error', {'error': 'Invalid request format'})
        return
    
    # Extract user ID and validate
    user_id = data.get('user_id')
    token = data.get('token')
    
    if not user_id:
        emit('notifications_error', {'error': 'User ID is required'})
        return
    
    # Validate user access with JWT (if provided)
    if token:
        validation_result = validate_jwt(token, required_user_id=user_id)
        if not validation_result['valid']:
            emit('notifications_error', {'error': 'Unauthorized access to notifications'})
            logger.warning(f"Unauthorized attempt to access notifications for user {user_id}")
            return
    
    # Get filter parameters
    include_read = data.get('include_read', False)
    limit = data.get('limit', 50)
    
    # Retrieve notifications
    try:
        notifications = get_user_notifications(user_id, include_read, limit)
        emit('notifications', {
            'user_id': user_id,
            'notifications': notifications,
            'count': len(notifications)
        })
        logger.debug(f"Retrieved {len(notifications)} notifications for user {user_id}")
    except Exception as e:
        logger.error(f"Error retrieving notifications for user {user_id}: {str(e)}")
        emit('notifications_error', {'error': 'Error retrieving notifications'})

def handle_mark_notification_read(data):
    """
    Handle event to mark a notification as read.
    
    Args:
        data (dict): Contains notification_id and user_id
    """
    if not data or not isinstance(data, dict):
        emit('notification_read_error', {'error': 'Invalid request format'})
        return
    
    # Extract parameters
    notification_id = data.get('notification_id')
    user_id = data.get('user_id')
    
    if not notification_id or not user_id:
        emit('notification_read_error', {'error': 'Notification ID and User ID are required'})
        return
    
    # Optionally validate with JWT
    token = data.get('token')
    if token:
        validation_result = validate_jwt(token, required_user_id=user_id)
        if not validation_result['valid']:
            emit('notification_read_error', {'error': 'Unauthorized'})
            return
    
    # Process the mark as read request
    try:
        success = mark_notification_read(notification_id, user_id)
        if success:
            emit('notification_read_confirmed', {
                'notification_id': notification_id,
                'user_id': user_id,
                'status': 'read'
            })
            logger.debug(f"Notification {notification_id} marked as read by user {user_id}")
        else:
            emit('notification_read_error', {'error': 'Failed to mark notification as read'})
    except Exception as e:
        logger.error(f"Error marking notification {notification_id} as read: {str(e)}")
        emit('notification_read_error', {'error': 'Server error processing request'})

def handle_notification_action(data):
    """
    Handle event when a user takes action on a notification.
    
    Args:
        data (dict): Contains notification_id, user_id, and action
    """
    if not data or not isinstance(data, dict):
        emit('notification_action_error', {'error': 'Invalid request format'})
        return
    
    # Extract parameters
    notification_id = data.get('notification_id')
    user_id = data.get('user_id')
    action = data.get('action')
    
    if not notification_id or not user_id or not action:
        emit('notification_action_error', 
             {'error': 'Notification ID, User ID, and action are required'})
        return
    
    # Log the action
    logger.info(f"User {user_id} performed action '{action}' on notification {notification_id}")
    
    # Auto-mark as read when an action is taken
    try:
        mark_notification_read(notification_id, user_id)
    except Exception as e:
        logger.error(f"Error marking notification as read during action: {str(e)}")
    
    # Acknowledge the action
    emit('notification_action_confirmed', {
        'notification_id': notification_id,
        'user_id': user_id,
        'action': action,
        'status': 'processed'
    })

def handle_admin_get_notification_stats(data):
    """
    Handle admin request to get notification statistics.
    
    Args:
        data (dict): Contains admin token
    """
    if not data or not isinstance(data, dict):
        emit('notification_stats_error', {'error': 'Invalid request format'})
        return
    
    # Validate admin access
    admin_token = data.get('admin_token')
    if not admin_token:
        emit('notification_stats_error', {'error': 'Admin token required'})
        return
    
    # Validate the admin token
    validation_result = validate_jwt(admin_token, required_role='admin')
    if not validation_result['valid']:
        emit('notification_stats_error', {'error': 'Unauthorized access'})
        logger.warning("Unauthorized attempt to access notification stats")
        return
    
    # Get notification statistics
    try:
        stats = get_notification_stats()
        emit('notification_stats', {
            'stats': stats,
            'timestamp': stats.get('timestamp', None)
        })
        logger.debug("Notification stats retrieved by admin")
    except Exception as e:
        logger.error(f"Error retrieving notification stats: {str(e)}")
        emit('notification_stats_error', {'error': 'Server error processing request'})

def handle_test_notification(data):
    """
    Handle event to send a test notification.
    
    Args:
        data (dict): Contains user_id and optional message content
    """
    if not data or not isinstance(data, dict):
        emit('test_notification_error', {'error': 'Invalid request format'})
        return
    
    # Extract user ID
    user_id = data.get('user_id')
    if not user_id:
        emit('test_notification_error', {'error': 'User ID is required'})
        return
    
    # Check if user is connected
    if not is_user_connected(user_id):
        emit('test_notification_error', {
            'error': 'User is not connected',
            'user_id': user_id
        })
        return
    
    # Create test notification
    notification = {
        'title': data.get('title', 'Test Notification'),
        'message': data.get('message', 'This is a test notification from SmartProBono'),
        'type': data.get('type', 'info'),
        'category': 'test',
        'data': {
            'test': True,
            'timestamp': data.get('timestamp', None)
        }
    }
    
    # Send the notification
    try:
        result = send_notification(user_id, notification, message=notification['message'])
        
        if result['success']:
            emit('test_notification_sent', {
                'success': True,
                'notification_id': result['notification_id'],
                'delivered': result['delivered']
            })
            logger.info(f"Test notification sent to user {user_id}")
        else:
            emit('test_notification_error', {
                'error': 'Failed to send notification',
                'details': result.get('error', 'Unknown error')
            })
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        emit('test_notification_error', {'error': 'Server error processing request'})

# Register event handlers
def register_notification_handlers(socketio):
    """
    Register all notification handlers with SocketIO instance.
    
    Args:
        socketio: The SocketIO instance
    """
    socketio.on_event('get_notifications', handle_get_notifications)
    socketio.on_event('mark_notification_read', handle_mark_notification_read)
    socketio.on_event('notification_action', handle_notification_action)
    socketio.on_event('admin_get_notification_stats', handle_admin_get_notification_stats)
    socketio.on_event('test_notification', handle_test_notification)
    
    logger.info("Notification handlers registered") 