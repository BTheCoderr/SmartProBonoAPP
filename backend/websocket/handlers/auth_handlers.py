"""
WebSocket Authentication Handlers.

This module contains event handlers for authentication-related WebSocket events.
"""

import logging
from flask import request, current_app
from flask_socketio import emit, join_room, leave_room

from backend.websocket.utils.auth import authenticate_connection
from backend.websocket.services.connection_service import (
    register_connection,
    unregister_connection,
    get_connection_user,
    update_connection_metadata
)

# Configure logging
logger = logging.getLogger('websocket.handlers.auth')

def register_auth_handlers(socketio):
    """
    Register all authentication-related event handlers.
    
    Args:
        socketio (SocketIO): The SocketIO instance
    """
    @socketio.on('authenticate', namespace='/ws')
    def handle_authenticate(data):
        """
        Handle authentication requests.
        
        Expected data:
        {
            "token": "JWT token",
            "client_info": {
                "device": "browser/mobile/etc",
                "platform": "web/ios/android/etc"
            }
        }
        """
        # Flask-SocketIO adds the sid attribute to the request
        if not hasattr(request, 'sid'):
            logger.error("Cannot access request.sid in authenticate handler")
            emit('auth_error', {'error': 'Internal server error'})
            return
            
        client_id = getattr(request, 'sid', 'unknown')
        
        if not data or not isinstance(data, dict):
            emit('auth_error', {'error': 'Invalid authentication data'})
            return
        
        # Extract token and validate
        token = data.get('token')
        client_info = data.get('client_info', {})
        
        if not token:
            emit('auth_error', {'error': 'No authentication token provided'})
            return
        
        # Authenticate the connection
        auth_result = authenticate_connection({'token': token})
        
        if not auth_result.get('authenticated'):
            error_msg = auth_result.get('error', 'Authentication failed')
            logger.warning(f"Authentication failed for {client_id}: {error_msg}")
            emit('auth_error', {'error': error_msg})
            return
        
        user_id = auth_result.get('user_id')
        
        # Update connection tracking with the authenticated user ID
        update_connection_metadata(
            client_id, 
            {
                'authenticated': True,
                'client_info': client_info
            }
        )
        
        # Re-register connection with proper user ID
        register_connection(
            sid=client_id,
            user_id=user_id,
            metadata={
                'user_agent': request.headers.get('User-Agent', 'Unknown'),
                'ip': request.remote_addr,
                'authenticated': True,
                'client_info': client_info
            }
        )
        
        # Join a room specific to this user for targeted messages
        join_room(f"user:{user_id}")
        
        logger.info(f"User {user_id} authenticated on connection {client_id}")
        
        emit('authenticated', {
            'user_id': user_id,
            'status': 'authenticated'
        })
    
    @socketio.on('deauthenticate', namespace='/ws')
    def handle_deauthenticate():
        """Handle requests to deauthenticate (logout) from WebSocket."""
        # Flask-SocketIO adds the sid attribute to the request
        if not hasattr(request, 'sid'):
            logger.error("Cannot access request.sid in deauthenticate handler")
            emit('error', {'error': 'Internal server error'})
            return
            
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if not user_id or user_id.startswith('anonymous:'):
            emit('error', {'error': 'Not authenticated'})
            return
        
        # Leave user-specific room
        leave_room(f"user:{user_id}")
        
        # Re-register as anonymous
        register_connection(
            sid=client_id,
            user_id=f"anonymous:{client_id}",
            metadata={
                'user_agent': request.headers.get('User-Agent', 'Unknown'),
                'ip': request.remote_addr,
                'authenticated': False
            }
        )
        
        logger.info(f"User {user_id} deauthenticated from connection {client_id}")
        
        emit('deauthenticated', {
            'status': 'success'
        }) 