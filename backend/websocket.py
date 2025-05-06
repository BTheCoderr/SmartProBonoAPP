"""
WebSocket module for real-time communication with graceful fallbacks

This module provides WebSocket functionality for real-time updates between
clients and the server. It includes fallback mechanisms for environments
where WebSockets aren't supported or when dependencies fail to load.
"""
import logging
import os
from flask import current_app

logger = logging.getLogger(__name__)

# Try to import SocketIO
try:
    from flask_socketio import SocketIO, emit, join_room, leave_room
    HAS_SOCKETIO = True
    logger.info("SocketIO imported successfully")
except ImportError:
    logger.warning("flask_socketio not available, using mock implementation")
    HAS_SOCKETIO = False

# Create a mock SocketIO class for fallback
class MockSocketIO:
    """Mock SocketIO implementation for environments without websocket support"""
    
    def __init__(self, app=None, **kwargs):
        self.app = app
        logger.warning("Using MockSocketIO - real-time updates will not work")
    
    def init_app(self, app, **kwargs):
        self.app = app
        logger.info("Initialized MockSocketIO with app")
    
    def run(self, app, **kwargs):
        logger.info("MockSocketIO.run called")
        return app
    
    def emit(self, event, data=None, to=None, room=None, namespace=None, **kwargs):
        logger.info(f"MockSocketIO.emit: {event} -> {room or 'all'}")
    
    def on(self, event, namespace=None):
        def decorator(f):
            logger.info(f"MockSocketIO registered event handler for {event}")
            return f
        return decorator
    
    def on_error(self, namespace=None):
        def decorator(f):
            logger.info(f"MockSocketIO registered error handler")
            return f
        return decorator
    
    def on_connect(self, namespace=None):
        def decorator(f):
            logger.info(f"MockSocketIO registered connect handler")
            return f
        return decorator
    
    def on_disconnect(self, namespace=None):
        def decorator(f):
            logger.info(f"MockSocketIO registered disconnect handler")
            return f
        return decorator

# Create either real or mock SocketIO instance
if HAS_SOCKETIO:
    socketio = SocketIO(cors_allowed_origins="*", async_mode=os.environ.get('SOCKETIO_ASYNC_MODE', 'eventlet'))
    logger.info(f"Real SocketIO initialized with async mode: {socketio.async_mode}")
else:
    socketio = MockSocketIO()
    logger.warning("Using MockSocketIO instead of real SocketIO")

# Re-export SocketIO functions or provide mocks
if HAS_SOCKETIO:
    # Use real emit, join_room, leave_room
    pass
else:
    # Create mock functions
    def emit(event, data=None, to=None, room=None, namespace=None, **kwargs):
        logger.info(f"Mock emit: {event} -> {room or 'all'}")
    
    def join_room(room, namespace=None, sid=None):
        logger.info(f"Mock join_room: {room}")
    
    def leave_room(room, namespace=None, sid=None):
        logger.info(f"Mock leave_room: {room}")

# Event handlers
def register_handlers(socketio_instance):
    """Register WebSocket event handlers"""
    
    @socketio_instance.on('connect')
    def handle_connect():
        logger.info("Client connected")
    
    @socketio_instance.on('disconnect')
    def handle_disconnect():
        logger.info("Client disconnected")
    
    @socketio_instance.on('join')
    def handle_join(data):
        """Handle client joining a room"""
        user_id = data.get('user_id')
        room = data.get('room')
        
        if not room:
            return {'error': 'Room name is required'}
        
        join_room(room)
        logger.info(f"User {user_id} joined room {room}")
        emit('status', {'message': f'Joined room: {room}'}, room=room)
    
    @socketio_instance.on('leave')
    def handle_leave(data):
        """Handle client leaving a room"""
        user_id = data.get('user_id')
        room = data.get('room')
        
        if not room:
            return {'error': 'Room name is required'}
        
        leave_room(room)
        logger.info(f"User {user_id} left room {room}")
    
    @socketio_instance.on('message')
    def handle_message(data):
        """Handle messages sent by clients"""
        room = data.get('room')
        message = data.get('message')
        
        if not room or not message:
            return {'error': 'Room and message are required'}
        
        logger.info(f"Message in room {room}: {message}")
        emit('message', data, room=room)
    
    @socketio_instance.on_error()
    def handle_error(e):
        """Handle WebSocket errors"""
        logger.error(f"SocketIO error: {str(e)}")

# Define functions to broadcast events
def broadcast_system_status(status):
    """Broadcast system status to all clients"""
    socketio.emit('system_status', status)

def notify_document_update(document_id, user_id=None):
    """Notify about document updates"""
    data = {'document_id': document_id, 'timestamp': from_app_import('datetime').now().isoformat()}
    
    # Broadcast to document room
    socketio.emit('document_update', data, room=f'document_{document_id}')
    
    # Also send to specific user if provided
    if user_id:
        socketio.emit('document_update', data, room=f'user_{user_id}')

def from_app_import(module_name):
    """Helper to import modules only when needed"""
    if module_name == 'datetime':
        from datetime import datetime
        return datetime
    return None

# Initialize handlers when imported
if HAS_SOCKETIO:
    try:
        register_handlers(socketio)
        logger.info("WebSocket event handlers registered")
    except Exception as e:
        logger.error(f"Error registering WebSocket handlers: {str(e)}")
        
# Monkey patch if using eventlet/gevent
if HAS_SOCKETIO and socketio.async_mode in ('eventlet', 'gevent'):
    try:
        if socketio.async_mode == 'eventlet':
            import eventlet
            eventlet.monkey_patch()
            logger.info("Eventlet monkey patching applied")
        elif socketio.async_mode == 'gevent':
            from gevent import monkey
            monkey.patch_all()
            logger.info("Gevent monkey patching applied")
    except ImportError:
        logger.warning(f"Could not apply {socketio.async_mode} monkey patching") 