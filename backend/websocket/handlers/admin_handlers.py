"""
WebSocket Admin Handlers.

This module contains event handlers for admin-related WebSocket events.
"""

import logging
from flask import request, current_app
from flask_socketio import emit

from websocket.utils.auth import authenticate_connection, check_authorization
from websocket.services.connection_service import (
    get_connection_user,
    get_connected_users,
    get_connection_stats
)
from websocket.services.notification_service import (
    get_notification_stats,
    send_broadcast_notification
)

# Configure logging
logger = logging.getLogger('websocket.handlers.admin')

def register_admin_handlers(socketio):
    """
    Register all admin-related event handlers.
    
    Args:
        socketio (SocketIO): The SocketIO instance
    """
    @socketio.on('admin_stats', namespace='/ws')
    def handle_admin_stats():
        """
        Handle requests for admin statistics about connections and notifications.
        Only accessible to admin users.
        """
        # Flask-SocketIO adds sid attribute to request object
        if not hasattr(request, 'sid'):
            logger.error("Cannot access request.sid in admin_stats handler")
            emit('error', {'error': 'Internal server error'})
            return
            
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        # Check if user has admin privileges
        if not check_authorization(user_id, 'admin', 'view_stats'):
            logger.warning(f"Unauthorized admin stats request from user {user_id}")
            emit('error', {'error': 'Unauthorized access'})
            return
        
        # Get statistics
        connection_stats = get_connection_stats()
        notification_stats = get_notification_stats()
        
        emit('admin_stats_result', {
            'connection_stats': connection_stats,
            'notification_stats': notification_stats
        })
    
    @socketio.on('admin_broadcast', namespace='/ws')
    def handle_admin_broadcast(data):
        """
        Handle admin broadcast notification requests.
        Only accessible to admin users.
        
        Expected data:
        {
            "title": "Notification title",
            "message": "Notification message",
            "type": "info|success|warning|error",
            "category": "Optional category",
            "data": {}  # Optional additional data
        }
        """
        # Flask-SocketIO adds sid attribute to request object
        if not hasattr(request, 'sid'):
            logger.error("Cannot access request.sid in admin_broadcast handler")
            emit('error', {'error': 'Internal server error'})
            return
            
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        # Check if user has admin privileges
        if not check_authorization(user_id, 'admin', 'send_broadcast'):
            logger.warning(f"Unauthorized broadcast attempt from user {user_id}")
            emit('error', {'error': 'Unauthorized access'})
            return
        
        if not data or not isinstance(data, dict):
            emit('error', {'error': 'Invalid request data'})
            return
        
        # Required fields
        title = data.get('title')
        message = data.get('message')
        
        if not title or not message:
            emit('error', {'error': 'Title and message are required'})
            return
        
        # Optional fields
        notification_type = data.get('type', 'info')
        category = data.get('category')
        additional_data = data.get('data', {})
        exclude_users = data.get('exclude_users', [])
        
        # Send broadcast notification
        result = send_broadcast_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            category=category,
            data=additional_data,
            exclude_users=exclude_users
        )
        
        emit('admin_broadcast_result', result)
    
    @socketio.on('admin_connected_users', namespace='/ws')
    def handle_admin_connected_users():
        """
        Handle requests for list of connected users.
        Only accessible to admin users.
        """
        # Flask-SocketIO adds sid attribute to request object
        if not hasattr(request, 'sid'):
            logger.error("Cannot access request.sid in admin_connected_users handler")
            emit('error', {'error': 'Internal server error'})
            return
            
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Authentication required'})
            return
        
        # Check if user has admin privileges
        if not check_authorization(user_id, 'admin', 'view_users'):
            logger.warning(f"Unauthorized connected users request from user {user_id}")
            emit('error', {'error': 'Unauthorized access'})
            return
        
        # Get connected users
        users = get_connected_users()
        
        emit('admin_connected_users_result', {
            'users': users,
            'count': len(users)
        }) 