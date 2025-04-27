"""
WebSocket Notification Handlers.

This module contains event handlers for notification-related WebSocket events.
"""

import logging
from flask import request
from flask_socketio import emit

from backend.websocket.services.connection_service import get_connection_user
from backend.websocket.services.notification_service import (
    mark_notification_read,
    get_user_notifications,
    delete_notification
)

# Configure logging
logger = logging.getLogger('websocket.handlers.notification')

def register_notification_handlers(socketio):
    """
    Register all notification-related event handlers.
    
    Args:
        socketio (SocketIO): The SocketIO instance
    """
    @socketio.on('mark_read', namespace='/ws')
    def handle_mark_read(data):
        """
        Handle mark notification as read event.
        
        Expected data:
        {
            "notification_id": "id of notification to mark as read"
        }
        """
        # Flask-SocketIO adds sid attribute to request object
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        if not data or not isinstance(data, dict):
            emit('error', {'error': 'Invalid request data'})
            return
        
        notification_id = data.get('notification_id')
        if not notification_id:
            emit('error', {'error': 'Notification ID is required'})
            return
        
        success = mark_notification_read(notification_id, user_id)
        
        if success:
            emit('notification_updated', {
                'notification_id': notification_id,
                'read': True
            })
        else:
            emit('error', {'error': 'Failed to mark notification as read'})
    
    @socketio.on('get_notifications', namespace='/ws')
    def handle_get_notifications(data=None):
        """
        Handle request for retrieving user notifications.
        
        Expected data:
        {
            "include_read": true/false,
            "limit": 20
        }
        """
        # Flask-SocketIO adds sid attribute to request object
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        if not data or not isinstance(data, dict):
            data = {}
        
        include_read = data.get('include_read', False)
        limit = min(int(data.get('limit', 50)), 100)  # Cap at 100 notifications
        
        notifications = get_user_notifications(
            user_id=user_id,
            include_read=include_read,
            limit=limit
        )
        
        emit('notifications', {
            'notifications': notifications,
            'count': len(notifications)
        })
    
    @socketio.on('delete_notification', namespace='/ws')
    def handle_delete_notification(data):
        """
        Handle deletion of a notification.
        
        Expected data:
        {
            "notification_id": "id of notification to delete"
        }
        """
        # Flask-SocketIO adds sid attribute to request object
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        if not data or not isinstance(data, dict):
            emit('error', {'error': 'Invalid request data'})
            return
        
        notification_id = data.get('notification_id')
        if not notification_id:
            emit('error', {'error': 'Notification ID is required'})
            return
        
        success = delete_notification(notification_id, user_id)
        
        if success:
            emit('notification_deleted', {
                'notification_id': notification_id
            })
        else:
            emit('error', {'error': 'Failed to delete notification'}) 