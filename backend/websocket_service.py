from flask_socketio import SocketIO, emit, join_room, leave_room
import json
from datetime import datetime
from flask import request
# Note: request.sid is provided by Flask-SocketIO and not available in a regular Flask Request object

# Initialize SocketIO without specifying cors_allowed_origins
# This will be properly set up when the Flask app is available
socketio = SocketIO()

# Dictionary to track connected users
# Format: {user_id: set(session_ids)}
connected_users = {}

def init_socketio(app, cors_origins):
    """Initialize SocketIO with the Flask app and CORS settings"""
    socketio.init_app(app, 
                      cors_allowed_origins=cors_origins,
                      async_mode="eventlet",
                      logger=True, 
                      engineio_logger=True)
    
    # Register event handlers
    register_handlers()
    
    return socketio

def register_handlers():
    """Register all Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        print("Client connected")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")
        # Find and remove this session from any user tracking
        user_id = None
        session_id = request.sid  # type: ignore # Flask-SocketIO adds the sid attribute to request
        
        for uid, sessions in list(connected_users.items()):
            if session_id in sessions:
                user_id = uid
                sessions.remove(session_id)
                if not sessions:  # If no more sessions for this user
                    del connected_users[uid]
                break
                
        print(f"Removed session for user {user_id}, connected users: {connected_users}")
    
    @socketio.on('register')
    def handle_register(data):
        """Register a user for receiving notifications"""
        if 'user_id' not in data:
            return {'status': 'error', 'message': 'user_id is required'}
        
        user_id = str(data['user_id'])
        session_id = request.sid  # type: ignore # Flask-SocketIO adds the sid attribute to request
        
        if not user_id or not session_id:
            return {'status': 'error', 'message': 'Invalid user_id or session'}
        
        # Add user to a room with their user_id
        join_room(user_id)
        
        # Track this connection
        if user_id not in connected_users:
            connected_users[user_id] = set()
        connected_users[user_id].add(session_id)
        
        print(f"User {user_id} registered from session {session_id}")
        print(f"Connected users: {connected_users}")
        
        return {'status': 'success', 'message': f'User {user_id} registered for notifications'}

def send_notification(user_id, notification_data):
    """Send a notification to a specific user"""
    if not isinstance(notification_data, dict):
        notification_data = {'message': str(notification_data)}
    
    # Add timestamp if not present
    if 'timestamp' not in notification_data:
        notification_data['timestamp'] = datetime.utcnow().isoformat()
    
    # Send to the user's room
    socketio.emit('notification', notification_data, to=str(user_id), namespace='/')
    
    return True

def send_direct_message(session_id, message_data):
    """Send a message directly to a specific client by their session ID
    
    Args:
        session_id (str): The client's session ID (request.sid)
        message_data (dict): The message data to send
    
    Returns:
        bool: True if the message was sent
    """
    if not isinstance(message_data, dict):
        message_data = {'message': str(message_data)}
    
    # Add timestamp if not present
    if 'timestamp' not in message_data:
        message_data['timestamp'] = datetime.utcnow().isoformat()
    
    # Send directly to the specific client using their session ID as the room
    socketio.emit('direct_message', message_data, to=session_id, namespace='/')
    
    return True

def send_broadcast_notification(notification_data):
    """Send a notification to all connected users"""
    if not isinstance(notification_data, dict):
        notification_data = {'message': str(notification_data)}
    
    # Add timestamp if not present
    if 'timestamp' not in notification_data:
        notification_data['timestamp'] = datetime.utcnow().isoformat()
    
    # Broadcast to all connected clients
    socketio.emit('notification', notification_data, namespace='/')
    
    return True 