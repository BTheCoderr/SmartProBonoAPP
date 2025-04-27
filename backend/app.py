"""Flask application factory"""
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask
from logging.handlers import RotatingFileHandler
from backend.extensions import init_extensions
from backend.database.mongo import mongo
from backend.middleware.security import SecurityMiddleware
from typing import Dict, Any, Optional, Union

# Load environment variables
load_dotenv()

def configure_logging(app):
    """Configure logging for the application"""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/smartprobono.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('SmartProBono startup')

def create_app(test_config: Optional[Union[str, Dict[str, Any]]] = None):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure logging
    configure_logging(app)

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MONGO_URI=os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/smartprobono'),
        MAIL_SERVER=os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
        MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true',
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
        # Security settings
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=timedelta(days=1),
        REMEMBER_COOKIE_SECURE=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_SAMESITE='Lax',
        # CORS settings
        CORS_ORIGINS=['https://smartprobono.org', 'https://app.smartprobono.org'],
        CORS_METHODS=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        CORS_ALLOW_HEADERS=['Content-Type', 'Authorization'],
        CORS_EXPOSE_HEADERS=['Content-Range', 'X-Total-Count'],
        CORS_SUPPORTS_CREDENTIALS=True,
        # Rate limiting
        RATELIMIT_DEFAULT='100 per minute',
        RATELIMIT_STORAGE_URL='memory://',  # Use Redis in production
        # File upload
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
        UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads'),
        ALLOWED_EXTENSIONS={'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
    )

    # Override default configuration for testing
    if test_config is not None:
        if isinstance(test_config, dict):
            app.config.update(test_config)
        else:
            # If test_config is a string, assume it's a config filename
            app.config.from_pyfile(test_config)

    # Initialize extensions
    init_extensions(app)
    
    # Initialize security middleware
    SecurityMiddleware(app)
    
    # Initialize MongoDB with app context
    with app.app_context():
        try:
            mongo.init_client(app.config['MONGO_URI'])
            app.logger.info("MongoDB initialized successfully")
        except Exception as e:
            app.logger.warning(f"Failed to initialize MongoDB: {str(e)}")
            app.logger.warning("Continuing without MongoDB support")

    # Import blueprints after app creation
    from .routes.auth import bp as auth_bp
    from .routes.templates import bp as templates_bp
    from .routes.notifications import bp as notifications_bp
    from .routes.document_scanner import scanner_bp
    from .routes.legal_ai import bp as legal_ai_bp
    from .routes.admin import bp as admin_bp
    from .routes.paralegal import paralegal_bp
    from .routes.form_templates import form_templates_bp
    from .routes.intake import bp as intake_bp
    from .routes.rights import bp as rights_bp
    from .routes.legal_templates import bp as legal_templates_bp

    # Register blueprints
    blueprints = [
        auth_bp,
        templates_bp,
        notifications_bp,
        scanner_bp,
        legal_ai_bp,
        admin_bp,
        paralegal_bp,
        form_templates_bp,
        intake_bp,
        rights_bp,
        legal_templates_bp
    ]
    
    try:
        for blueprint in blueprints:
            if blueprint is not None:  # Type check to satisfy mypy
                app.register_blueprint(blueprint)
        app.logger.info('All blueprints registered successfully')
    except Exception as e:
        app.logger.error(f'Error registering blueprints: {str(e)}')
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)


