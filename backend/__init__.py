"""
SmartProBono backend application
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from .extensions import db, mongo, mail, socketio, jwt
from .config import config

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if isinstance(config_name, dict):
        app.config.update(config_name)
    else:
        app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
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
    
    return app
