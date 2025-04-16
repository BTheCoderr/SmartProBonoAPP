from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import uuid
from datetime import datetime
import sys
import json
import logging
from flask_socketio import SocketIO, emit, join_room, leave_room

# Add the current directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize SocketIO
socketio = None

# Online users dictionary for WebSocket
online_users = {}

# Define a simple cache service for when Redis is not available
class MemoryCache:
    def __init__(self):
        self.cache = {}
        
    def get(self, key):
        return self.cache.get(key)
        
    def set(self, key, value, expire_seconds=None):
        self.cache[key] = value
        return True
        
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
        return True
        
    def clear_pattern(self, pattern):
        import fnmatch
        keys_to_delete = [k for k in self.cache.keys() if fnmatch.fnmatch(k, pattern)]
        for k in keys_to_delete:
            del self.cache[k]
        return True
        
    def get_stats(self):
        return {
            'type': 'in-memory',
            'keys': len(self.cache)
        }

# Create a global cache service
cache_service = MemoryCache()

def create_app():
    """Create a simple Flask application for testing purposes"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize SocketIO
    global socketio
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*",
        async_mode='eventlet',  # Use eventlet for better performance
        logger=True,  # Enable logging for debugging
        engineio_logger=True  # Enable engineio logging
    )
    
    # Try to load Redis if available
    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        try:
            import redis
            redis_client = redis.from_url(redis_url)
            redis_client.ping()  # Test connection
            logger.info(f"Connected to Redis at {redis_url}")
            
            # TODO: Replace in-memory cache with Redis
        except (ImportError, Exception) as e:
            logger.warning(f"Failed to connect to Redis: {e}. Using in-memory cache instead.")
    
    # ---- Models ----
    
    # Create a simple User model
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(120))
        role = db.Column(db.String(20), default='client')  
        first_name = db.Column(db.String(80))
        last_name = db.Column(db.String(80))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def __init__(self, email, password=None, first_name='', last_name='', role='client'):
            self.email = email
            self.password = password
            self.first_name = first_name
            self.last_name = last_name
            self.role = role

        def __repr__(self):
            return f'<User {self.email}>'
            
    # Create a Notification model
    class Notification(db.Model):
        __tablename__ = 'notifications'
        
        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        title = db.Column(db.String(200), nullable=False)
        message = db.Column(db.Text, nullable=False)
        type = db.Column(db.String(20), default='info')  # info, success, warning, error
        is_read = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relationship
        user = db.relationship('User', backref=db.backref('notifications', lazy=True))
        
        def __init__(self, user_id, title, message, type='info'):
            self.user_id = user_id
            self.title = title
            self.message = message
            self.type = type
            self.is_read = False
        
        def to_dict(self):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'title': self.title,
                'message': self.message,
                'type': self.type,
                'is_read': self.is_read,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        # Cache-related methods
        def cache_key(self):
            return f"notification:{self.id}"
            
        def user_notifications_key(self):
            return f"user:{self.user_id}:notifications"
            
        def save_to_cache(self):
            """Save notification to cache"""
            try:
                # Save individual notification
                cache_service.set(
                    self.cache_key(), 
                    json.dumps(self.to_dict()),
                    expire_seconds=3600  # 1 hour cache
                )
                
                # Update user's notifications list in cache
                user_notifs = cache_service.get(self.user_notifications_key())
                if user_notifs:
                    user_notifs = json.loads(user_notifs)
                    
                    # Check if this notification already exists
                    for i, notif in enumerate(user_notifs):
                        if notif.get('id') == self.id:
                            user_notifs[i] = self.to_dict()
                            break
                    else:
                        user_notifs.append(self.to_dict())
                else:
                    # First notification for user
                    user_notifs = [self.to_dict()]
                    
                # Save updated list
                cache_service.set(
                    self.user_notifications_key(),
                    json.dumps(user_notifs),
                    expire_seconds=3600
                )
                
                return True
            except Exception as e:
                logger.error(f"Error saving to cache: {e}")
                return False

    # ---- Routes ----
    
    # Basic route for testing
    @app.route('/')
    def index():
        return jsonify({
            'status': 'success',
            'message': 'Flask server is running with notification system'
        })
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'operational',
            'version': '1.0.0',
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'cache': 'active'
        })

    # Users API endpoint
    @app.route('/api/users')
    def get_users():
        users = User.query.all()
        result = [{'id': user.id, 'email': user.email, 'name': f"{user.first_name or ''} {user.last_name or ''}".strip()} for user in users]
        return jsonify(result)
    
    # Create a user
    @app.route('/api/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({'error': 'Missing email'}), 400
            
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
            
        # Create user with minimal required fields
        user = User(
            email=data['email'], 
            password=data.get('password', 'defaultpassword'),  # You should require password in production
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role=data.get('role', 'client')
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'id': user.id, 
            'email': user.email,
            'name': f"{user.first_name or ''} {user.last_name or ''}".strip(),
            'role': user.role
        }), 201
    
    # Notifications API
    @app.route('/api/users/<int:user_id>/notifications')
    def get_user_notifications(user_id):
        # Check if in cache first
        cache_key = f"user:{user_id}:notifications"
        cached_notifs = cache_service.get(cache_key)
        
        if cached_notifs:
            try:
                return jsonify(json.loads(cached_notifs))
            except:
                # If cache is invalid, continue to DB query
                pass
                
        # Fetch from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        notifications = Notification.query.filter_by(user_id=user_id).all()
        result = [notif.to_dict() for notif in notifications]
        
        # Cache the result
        cache_service.set(
            cache_key,
            json.dumps(result),
            expire_seconds=3600
        )
        
        return jsonify(result)
    
    # Create a notification
    @app.route('/api/users/<int:user_id>/notifications', methods=['POST'])
    def create_notification(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        if not data or not data.get('title') or not data.get('message'):
            return jsonify({'error': 'Missing title or message'}), 400
            
        notification = Notification(
            user_id=user_id,
            title=data['title'],
            message=data['message'],
            type=data.get('type', 'info')
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Cache the notification
        notification.save_to_cache()
        
        return jsonify(notification.to_dict()), 201
    
    # Mark notification as read
    @app.route('/api/notifications/<notification_id>/read', methods=['POST'])
    def mark_notification_read(notification_id):
        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
            
        notification.is_read = True
        db.session.commit()
        
        # Update cache
        notification.save_to_cache()
        
        return jsonify({'success': True, 'notification': notification.to_dict()})
    
    # Cache stats route
    @app.route('/api/cache/stats')
    def get_cache_stats():
        return jsonify(cache_service.get_stats())
    
    @app.route('/api/db-status')
    def db_status():
        try:
            user_count = User.query.count()
            notification_count = Notification.query.count()
            return jsonify({
                'status': 'connected',
                'database': app.config['SQLALCHEMY_DATABASE_URI'],
                'user_count': user_count,
                'notification_count': notification_count
            })
        except Exception as e:
            logger.error(f"Database error: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    # ---- SocketIO Event Handlers ----
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        try:
            # Get the request's sid safely
            sid = None
            if hasattr(request, 'sid'):  # type: ignore
                sid = request.sid  # type: ignore
            elif hasattr(request, 'environ') and request.environ.get('socketio'):
                sid = request.environ.get('socketio').sid  # type: ignore
            
            if sid:
                logger.info(f"Client connected: {sid}")
                emit('connection_success', {'message': 'Connected successfully'})
            else:
                logger.warning("Client connected but couldn't get SID")
                emit('connection_success', {'message': 'Connected but SID not available'})
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
            emit('connection_success', {'message': 'Connected with errors'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        try:
            # Get the request's sid safely
            sid = None
            if hasattr(request, 'sid'):  # type: ignore
                sid = request.sid  # type: ignore
            elif hasattr(request, 'environ') and request.environ.get('socketio'):
                sid = request.environ.get('socketio').sid  # type: ignore
            
            if sid:
                if sid in online_users:
                    user_data = online_users[sid]
                    logger.info(f"Client disconnected: {sid} (User: {user_data.get('user_id')})")
                    del online_users[sid]
                else:
                    logger.info(f"Client disconnected: {sid}")
            else:
                logger.warning("Client disconnected but couldn't get SID")
        except Exception as e:
            logger.error(f"Error handling disconnection: {e}")
    
    @socketio.on('authenticate')
    def handle_authentication(data):
        """Handle client authentication"""
        try:
            # Get the request's sid safely
            sid = None
            if hasattr(request, 'sid'):  # type: ignore
                sid = request.sid  # type: ignore
            elif hasattr(request, 'environ') and request.environ.get('socketio'):
                sid = request.environ.get('socketio').sid  # type: ignore
            
            if not sid:
                emit('auth_error', {'message': 'Could not identify connection'})
                return
                
            user_id = data.get('user_id')
            
            if not user_id:
                emit('auth_error', {'message': 'User ID is required'})
                return
            
            # Store user data
            online_users[sid] = {
                'user_id': user_id,
                'authenticated': True,
                'connected_at': datetime.utcnow().isoformat()
            }
            
            # Join user's room
            join_room(f"user_{user_id}")
            
            logger.info(f"User authenticated: {user_id} (SID: {sid})")
            emit('auth_success', {'message': 'Authenticated successfully'})
            
            # Send any unread notifications
            send_unread_notifications(user_id)
            
        except Exception as e:
            logger.error(f"Error handling authentication: {e}")
            emit('auth_error', {'message': f'Error handling authentication: {str(e)}'})
    
    @socketio.on('test_notification')
    def handle_test_notification(data):
        """Handle test notification request"""
        try:
            # Get the request's sid safely
            sid = None
            if hasattr(request, 'sid'):  # type: ignore
                sid = request.sid  # type: ignore
            elif hasattr(request, 'environ') and request.environ.get('socketio'):
                sid = request.environ.get('socketio').sid  # type: ignore
            
            if not sid:
                emit('error', {'message': 'Could not identify connection'})
                return
                
            if sid not in online_users:
                emit('error', {'message': 'Not authenticated'})
                return
                
            user_id = online_users[sid].get('user_id')
            
            # Create notification
            notification = Notification(
                user_id=user_id,
                title=data.get('title', 'Test Notification'),
                message=data.get('message', 'This is a test notification'),
                type=data.get('type', 'info')
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Cache the notification
            notification.save_to_cache()
            
            # Send notification via WebSocket
            emit('notification', notification.to_dict(), room=f"user_{user_id}")  # type: ignore
            
            logger.info(f"Test notification sent to user {user_id}")
            emit('success', {'message': 'Notification sent successfully'})
            
        except Exception as e:
            logger.error(f"Error sending test notification: {e}")
            emit('error', {'message': f'Error sending test notification: {str(e)}'})
    
    # Helper functions for WebSocket
    def send_unread_notifications(user_id):
        """Send unread notifications to the user"""
        try:
            notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
            if notifications:
                for notification in notifications:
                    # Use socketio.emit instead of emit for more reliability
                    if socketio is not None:
                        socketio.emit('notification', notification.to_dict(), room=f"user_{user_id}")  # type: ignore
                    else:
                        emit('notification', notification.to_dict(), room=f"user_{user_id}")  # type: ignore
                logger.info(f"Sent {len(notifications)} unread notifications to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending unread notifications: {e}")
    
    # Keep the original create_notification function
    original_create_notification = app.view_functions['create_notification']
    
    # Wrapper for notification with WebSocket
    def create_notification_with_websocket(user_id):
        """Create a notification and send it via WebSocket"""
        # Call the original function
        response = original_create_notification(user_id)
        
        # If the notification was created successfully, send it via WebSocket
        try:
            # Check if we have a tuple response (response, status_code)
            status_code = response[1] if isinstance(response, tuple) else 200
            
            if status_code == 201:
                # Get the JSON response object from the response tuple or directly
                response_data = response[0] if isinstance(response, tuple) else response
                
                # Extract notification data safely
                notification_data = None
                
                # Try different approaches to extract data, with type ignore to silence linter
                try:
                    # For Flask Response objects
                    if hasattr(response_data, 'get_data'):  # type: ignore
                        raw_data = response_data.get_data(as_text=True)  # type: ignore
                        notification_data = json.loads(raw_data)
                    # For string responses
                    elif isinstance(response_data, str):
                        notification_data = json.loads(response_data)
                    # For dict responses
                    elif isinstance(response_data, dict):
                        notification_data = response_data
                    # Fallback for other response types
                    elif hasattr(response_data, 'data'):  # type: ignore
                        data = response_data.data  # type: ignore
                        if isinstance(data, bytes):
                            notification_data = json.loads(data.decode('utf-8'))
                except (AttributeError, TypeError, ValueError) as e:
                    logger.error(f"Failed to extract notification data: {e}")
                
                # Send via WebSocket if we successfully extracted the data
                if notification_data and socketio is not None:
                    socketio.emit('notification', notification_data, room=f"user_{user_id}")  # type: ignore
                    logger.info(f"Notification sent via WebSocket to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending notification via WebSocket: {e}")
            # Don't re-raise - we still want to return the original response
        
        # Return the original response unchanged
        return response
    
    # Add type checking for the decorator and suppress the linter error
    create_notification_with_websocket.__annotations__ = original_create_notification.__annotations__
    app.view_functions['create_notification'] = create_notification_with_websocket  # type: ignore
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
    port = int(os.environ.get('PORT', 5003))
    logger.info(f"Starting Flask app on port {port}")
    
    # Access the application's socketio instance
    from flask import current_app
    
    try:
        # Get the socketio instance - since create_app() returns the app, we need
        # to get the socketio instance from the app context
        with app.app_context():
            # Access socketio from the global scope where it was defined
            if 'socketio' in globals() and socketio is not None:
                logger.info("Starting server with SocketIO support")
                socketio.run(app, host='0.0.0.0', port=port, debug=True)  # type: ignore
            else:
                logger.warning("SocketIO not properly initialized, falling back to regular Flask")
                app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        # Fall back to regular Flask server
        app.run(host='0.0.0.0', port=port, debug=True) 