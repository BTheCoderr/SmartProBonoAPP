"""
WebSocket Core Module.

This module provides the core functionality for the WebSocket server,
including initialization, event handlers, and integration with Flask.
"""

import logging
from flask import request, current_app
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect

from websocket.utils.auth import validate_jwt, authenticate_connection
from websocket.services.connection_service import (
    register_connection,
    unregister_connection,
    get_connection_user,
    update_connection_metadata
)

# Configure logging
logger = logging.getLogger('websocket.core')

# Create SocketIO instance
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

def init_websocket(app):
    """
    Initialize the WebSocket server.
    
    Args:
        app (Flask): The Flask application instance
        
    Returns:
        SocketIO: The initialized SocketIO instance
    """
    if not app:
        raise ValueError("Flask app is required to initialize WebSocket")
    
    # Configure CORS for Socket.IO based on app config
    if app.config.get('CORS_ALLOWED_ORIGINS'):
        allowed_origins = app.config.get('CORS_ALLOWED_ORIGINS')
        if isinstance(allowed_origins, str):
            allowed_origins = [origin.strip() for origin in allowed_origins.split(',')]
        
        socketio.init_app(app, cors_allowed_origins=allowed_origins, async_mode='eventlet')
        logger.info(f"WebSocket initialized with CORS origins: {allowed_origins}")
    else:
        socketio.init_app(app, async_mode='eventlet')
        logger.info("WebSocket initialized with default CORS settings (allow all)")
    
    # Register global event handlers
    register_event_handlers()
    
    logger.info("WebSocket server initialized successfully")
    return socketio

def register_event_handlers():
    """Register all event handlers for the WebSocket server."""
    # Register connect/disconnect handlers
    @socketio.on('connect', namespace='/ws')
    def handle_connect():
        """Handle new WebSocket connections."""
        # Flask-SocketIO adds sid attribute to request object
        client_id = getattr(request, 'sid', 'unknown')
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        logger.info(f"New connection: {client_id}, UA: {user_agent}")
        
        # Store connection info even before authentication
        register_connection(
            sid=client_id, 
            user_id=f"anonymous:{client_id}", 
            metadata={
                'user_agent': user_agent,
                'ip': request.remote_addr,
                'authenticated': False
            }
        )
        
        emit('connected', {
            'status': 'connected',
            'client_id': client_id,
            'requires_auth': True
        })
    
    @socketio.on('disconnect', namespace='/ws')
    def handle_disconnect():
        """Handle WebSocket disconnect events."""
        client_id = getattr(request, 'sid', 'unknown')
        user_id = get_connection_user(client_id)
        
        if user_id:
            logger.info(f"Client disconnected: {client_id} (user: {user_id})")
        else:
            logger.info(f"Client disconnected: {client_id} (not authenticated)")
        
        # Clean up connection tracking
        unregister_connection(client_id)
    
    # Import and register handlers from handler modules
    from websocket.handlers import (
        register_auth_handlers,
        register_notification_handlers,
        register_admin_handlers
    )
    
    # Register authentication handlers
    register_auth_handlers(socketio)
    
    # Register notification handlers
    register_notification_handlers(socketio)
    
    # Register admin handlers
    register_admin_handlers(socketio) 