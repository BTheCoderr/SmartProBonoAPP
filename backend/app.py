from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room, rooms
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import logging
import json
import time
import uuid
from datetime import datetime
import random
from config.database import db, DatabaseConfig
from services.cache_service import get_cache_service
from routes import register_routes
from typing import Any, TYPE_CHECKING

# Type hint for Flask-SocketIO request
if TYPE_CHECKING:
    from flask_socketio.namespace import Namespace
    request: Any  # Type as Any to avoid linter errors with dynamic attributes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app-level variables that will be populated in create_app()
socketio = None
notification_service = None
online_users = {}  # sid -> { user_id, rooms }
typing_users = {}  # room_id -> {user_id: timestamp}
message_rate_limit = {}  # user_id -> list of timestamps
reconnect_rate_limit = {}  # ip -> list of timestamps
RATE_LIMIT_MAX_MESSAGES = 20  # max messages per minute
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_RECONNECT = 5  # max reconnections per minute

def check_rate_limit(user_id: str, rate_limits: dict, max_messages: int, window: int) -> bool:
    """Check if user has exceeded rate limit"""
    now = time.time()
    user_messages = rate_limits.get(user_id, [])
    
    # Remove old timestamps
    user_messages = [ts for ts in user_messages if now - ts < window]
    
    # Check if limit exceeded
    if len(user_messages) >= max_messages:
        return False
    
    # Update timestamps
    user_messages.append(now)
    rate_limits[user_id] = user_messages
    return True

def get_user_rooms(sid: str) -> set:
    """Get all rooms a user is in"""
    return online_users.get(sid, {}).get('rooms', set())

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration based on environment
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object('config.production')
    else:
        app.config.from_object('config.development')
    
    # Initialize CORS
    CORS(app)
    
    # Initialize database
    DatabaseConfig.init_app(app)
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize Socket.IO
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
    
    # Initialize cache service within app context
    with app.app_context():
        # Store cache service as a global variable instead of on app instance
        global cache_service
        cache_service = get_cache_service()
    
    # Register blueprints and routes here
    register_routes(app)
    # Socket.IO event handlers
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        try:
            sid = request.sid
            ip = request.remote_addr
            
            # Check reconnection rate limit
            if not check_rate_limit(ip, reconnect_rate_limit, RATE_LIMIT_RECONNECT, RATE_LIMIT_WINDOW):
                logger.warning(f"Connection rate limit exceeded for IP: {ip}")
                return False
            
            logger.info(f"Client connected: {sid} from {ip}")
            online_users[sid] = {'rooms': set(), 'ip': ip}
            emit('connection_response', {'status': 'connected', 'sid': sid})
            
        except Exception as e:
            logger.error(f"Error in connect handler: {str(e)}")
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        try:
            sid = request.sid
            user_data = online_users.get(sid)
            
            if user_data:
                # Leave all rooms
                for room in user_data['rooms']:
                    leave_room(room)
                    emit('user_left', {'user_id': user_data.get('user_id')}, to=room)
                
                # Clean up user data
                del online_users[sid]
                
                # Remove from typing status
                for room in typing_users:
                    typing_users[room].pop(sid, None)
                
                logger.info(f"Client disconnected: {sid}")
            
        except Exception as e:
            logger.error(f"Error in disconnect handler: {str(e)}")
    
    @socketio.on('authenticate')
    @jwt_required()
    def handle_authenticate(data):
        """Authenticate user and join rooms"""
        try:
            sid = request.sid
            user_id = get_jwt_identity()
            room = data.get('room')
            
            if not room:
                emit('error', {'message': 'Room ID is required'})
                return
                
            # Join room
            join_room(room)
            if sid not in online_users:
                online_users[sid] = {'user_id': user_id, 'rooms': set()}
            online_users[sid]['rooms'].add(room)
            
            # Notify room of new user
            emit('user_joined', {
                'user_id': user_id,
                'room': room,
                'timestamp': datetime.utcnow().isoformat()
            }, to=room)
            
            emit('authenticated', {
                'status': 'success',
                'user_id': user_id,
                'room': room
            })
            
            logger.info(f"User {user_id} authenticated and joined room {room}")
            
        except Exception as e:
            logger.error(f"Error in authenticate handler: {str(e)}")
            emit('error', {'message': 'Authentication failed'})
    
    @socketio.on('deauthenticate')
    def handle_deauthenticate(data):
        """Leave rooms and cleanup"""
        try:
            sid = request.sid
            room = data.get('room')
            
            if not room:
                emit('error', {'message': 'Room ID is required'})
                return
            
            user_data = online_users.get(sid)
            if user_data and room in user_data['rooms']:
                # Leave room
                user_data['rooms'].remove(room)
                leave_room(room)
                
                # Notify room
                emit('user_left', {
                    'user_id': user_data.get('user_id'),
                    'room': room,
                    'timestamp': datetime.utcnow().isoformat()
                }, to=room)
                
                emit('deauthenticated', {'status': 'success', 'room': room})
                logger.info(f"User left room {room}")
            
        except Exception as e:
            logger.error(f"Error in deauthenticate handler: {str(e)}")
            emit('error', {'message': 'Failed to leave room'})

    @socketio.on('message')
    def handle_message(data):
        """Handle chat messages with rate limiting"""
        try:
            sid = request.sid
            user_data = online_users.get(sid)
            
            if not user_data:
                emit('error', {'message': 'Not authenticated'})
                return
                
            # Check rate limit
            if not check_rate_limit(user_data['user_id'], message_rate_limit, RATE_LIMIT_MAX_MESSAGES, RATE_LIMIT_WINDOW):
                emit('error', {'message': 'Message rate limit exceeded'})
                return
            
            room = data.get('room')
            if not room or room not in user_data['rooms']:
                emit('error', {'message': 'Invalid room'})
                return
            
            # Broadcast message to room
            message_data = {
                'user_id': user_data['user_id'],
                'room': room,
                'content': data.get('content'),
                'timestamp': datetime.utcnow().isoformat()
            }
            emit('message', message_data, to=room)
                
        except Exception as e:
            logger.error(f"Error in message handler: {str(e)}")
            emit('error', {'message': 'Failed to send message'})

    @socketio.on('typing')
    def handle_typing(data):
        """Handle typing indicators"""
        try:
            sid = request.sid
            user_data = online_users.get(sid)
            
            if not user_data:
                return
            
            room = data.get('room')
            if not room or room not in user_data['rooms']:
                return
            
            is_typing = data.get('typing', False)
            
            if room not in typing_users:
                typing_users[room] = {}
            
            if is_typing:
                typing_users[room][sid] = time.time()
            else:
                typing_users[room].pop(sid, None)
            
            # Broadcast typing status
            typing_users_list = [
                online_users[s]['user_id']
                for s in typing_users[room]
                if time.time() - typing_users[room][s] < 5  # Clear after 5 seconds
            ]
            
            emit('typing_status', {
                'room': room,
                'users': typing_users_list
            }, to=room)
                
        except Exception as e:
            logger.error(f"Error in typing handler: {str(e)}")

    @socketio.on('test_notification')
    def handle_test_notification(data):
        room = data.get('room')
        if not room:
            emit('error', {'message': 'Room ID is required'})
            return
        
        notification = {
            'id': str(uuid.uuid4()),
            'type': 'test',
            'message': 'This is a test notification',
            'timestamp': datetime.utcnow().isoformat(),
            'room': room
        }
        emit('notification', notification, to=room)
        logger.info(f"Test notification sent to room {room}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    socketio = SocketIO(app)
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to run with Socket.IO: {e}")
        app.run(host='0.0.0.0', port=5000, debug=True)


