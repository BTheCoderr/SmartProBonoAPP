"""
Connection handler for WebSocket events.

This module handles WebSocket connection events including:
- New connections
- User registration
- Disconnection
- Admin connection monitoring
"""

import logging
from flask import current_app
from flask_socketio import emit, disconnect

from ..services.connection_service import (
    register_connection,
    unregister_connection,
    get_user_sessions,
    get_connected_users,
    get_connection_stats
)

# Configure logging
logger = logging.getLogger('websocket.handlers.connection')

def register_connection_handlers(socketio):
    """
    Register all connection-related event handlers.
    
    Args:
        socketio: The SocketIO instance
    """
    @socketio.on('connect')
    def handle_connect():
        """Handle new client connections"""
        logger.info(f"New client connected: {socketio.request.sid}")
        emit('server_message', {
            'message': 'Connection established',
            'status': 'connected'
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnections"""
        session_id = socketio.request.sid
        user_id = unregister_connection(session_id)
        
        if user_id:
            logger.info(f"User {user_id} disconnected (session: {session_id})")
        else:
            logger.info(f"Unregistered client disconnected: {session_id}")
    
    @socketio.on('register_user')
    def handle_register_user(data):
        """
        Register a user with their connection.
        
        Expected data:
        {
            "user_id": "string",        # Required
            "auth_token": "string"      # Optional, for future token validation
        }
        """
        if not data or not isinstance(data, dict):
            logger.warning(f"Invalid registration data: {data}")
            emit('registration_error', {
                'message': 'Invalid data format',
                'code': 'invalid_format'
            })
            return
        
        user_id = data.get('user_id')
        
        if not user_id:
            logger.warning(f"Missing user_id in registration: {data}")
            emit('registration_error', {
                'message': 'Missing user_id',
                'code': 'missing_user_id'
            })
            return
        
        # Optional: Validate auth token here if provided
        # auth_token = data.get('auth_token')
        # if auth_token and not validate_token(auth_token, user_id):
        #     emit('registration_error', {'message': 'Invalid auth token'})
        #     return
        
        session_id = socketio.request.sid
        success = register_connection(user_id, session_id)
        
        if success:
            logger.info(f"Registered user {user_id} with session {session_id}")
            emit('registration_success', {
                'user_id': user_id,
                'session_id': session_id,
                'message': 'Registration successful'
            })
        else:
            logger.warning(f"Failed to register user {user_id}")
            emit('registration_error', {
                'message': 'Registration failed',
                'code': 'registration_failed'
            })
    
    @socketio.on('get_user_connections')
    def handle_get_user_connections(data):
        """
        Get connections for a user.
        
        Expected data:
        {
            "user_id": "string"  # Required
        }
        """
        if not data or not isinstance(data, dict):
            emit('error', {
                'message': 'Invalid data format',
                'code': 'invalid_format'
            })
            return
        
        user_id = data.get('user_id')
        
        if not user_id:
            emit('error', {
                'message': 'Missing user_id',
                'code': 'missing_user_id'
            })
            return
        
        connections = get_user_sessions(user_id)
        emit('user_connections', {
            'user_id': user_id,
            'connections': connections,
            'count': len(connections)
        })
    
    @socketio.on('admin_get_connections')
    def handle_admin_get_connections(data):
        """
        Admin endpoint to get all connections.
        
        Expected data:
        {
            "admin_token": "string"  # Required
        }
        """
        # Validate admin token
        admin_token = data.get('admin_token') if data else None
        
        # Simple validation - in production use proper validation
        if not admin_token or admin_token != current_app.config.get('ADMIN_SECRET', 'admin_secret'):
            logger.warning(f"Unauthorized access attempt to admin_get_connections")
            emit('error', {
                'message': 'Unauthorized access',
                'code': 'unauthorized'
            })
            return
        
        connections = get_connected_users()
        counts = get_connection_stats()
        
        emit('admin_connections', {
            'connections': connections,
            'counts': counts
        })
    
    logger.info("Registered connection handlers") 