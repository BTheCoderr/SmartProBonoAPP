"""
SmartProBono backend application
"""
from flask import Flask, g, current_app
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
import redis

from .extensions import db, mongo, mail, socketio, jwt
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

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if isinstance(config_name, dict):
        app.config.update(config_name)
    else:
        app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')
    
    # Initialize Redis client
    global redis_client
    redis_client = redis.from_url(app.config.get('REDIS_URL', 'redis://localhost:6379/0'))
    
    # Register custom Jinja2 filters
    register_filters(app)
    
    # Register blueprints
    from .routes import (
        admin_bp, auth_bp, document_bp, immigration_bp,
        intake_bp, rights_bp, scanner_bp, template_bp
    )
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(immigration_bp)
    app.register_blueprint(intake_bp)
    app.register_blueprint(rights_bp)
    app.register_blueprint(scanner_bp)
    app.register_blueprint(template_bp)
    
    # Initialize WebSocket notification service
    from backend.websocket.services.notification_service import init_redis_subscription
    init_redis_subscription()
    
    return app
