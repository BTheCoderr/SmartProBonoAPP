"""
SmartProBono Backend Package
"""
from flask import Flask, g, current_app
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

from .extensions import db, mongo, mail, socketio, jwt, migrate, limiter
from .config import config
from .utils.template_filters import register_filters

# Initialize Redis client
redis_client = None

def get_redis():
    """Get Redis client instance"""
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(current_app.config.get('REDIS_URL', 'redis://localhost:6379/0'))
    return redis_client

def create_app(config_object=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    limiter.init_app(app)
    
    # Initialize Redis client
    global redis_client
    redis_client = redis.from_url(app.config.get('REDIS_URL', 'redis://localhost:6379/0'))
    
    # Register custom Jinja2 filters
    register_filters(app)
    
    # Register blueprints
    from .routes import register_blueprints
    register_blueprints(app)
    
    # Initialize middleware
    from .middleware import init_middleware
    init_middleware(app)
    
    # Initialize WebSocket notification service
    from backend.websocket.services.notification_service import init_redis_subscription
    init_redis_subscription()
    
    return app
