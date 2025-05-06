"""
Flask application for the SmartProBono backend API
"""
import os
import logging
import json
from datetime import datetime
from flask import Flask, jsonify, request
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    """
    Create Flask application with the given configuration
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask application
    """
    app = Flask(__name__)
    
    # Configure logging
    setup_logging(app)
    
    # Log startup information
    app.logger.info(f"Starting application in {config_name or 'default'} mode")
    
    # Set up configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Configure the app with basic security settings
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-for-testing-only'),
        SESSION_COOKIE_SECURE=config_name == 'production',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    
    # Database configuration
    configure_database(app)
    
    # Setup extensions
    setup_extensions(app)
    
    # Setup CORS
    try:
        from flask_cors import CORS
        default_origins = [
            'http://localhost:3000',
            'https://smartprobono.org',
            'https://www.smartprobono.org',
            'https://smartprobono.netlify.app',
            'https://smartprobono.netlify.com'
        ]
        allowed_origins = os.environ.get('ALLOWED_ORIGINS', ','.join(default_origins)).split(',')
        CORS(app, resources={r"/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
        }})
        app.logger.info(f"CORS configured with origins: {allowed_origins}")
    except ImportError:
        app.logger.warning("Flask-CORS not available, CORS not configured")
    
    # Create required directories
    create_required_dirs()
    
    # Add a basic health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'API is running',
            'version': '1.0.0'
        })
    
    # Add root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'SmartProBono API',
            'status': 'running',
            'endpoints': ['/api/health', '/api/admin/health']
        })
    
    # Add feedback endpoints
    @app.route('/api/feedback', methods=['POST'])
    def submit_feedback():
        try:
            feedback_data = request.json
            if not feedback_data:
                return jsonify({'error': 'No feedback data provided'}), 400
                
            # Add timestamp
            feedback_data['timestamp'] = datetime.now().isoformat()
            
            # Save feedback to a JSON file
            filename = f"data/feedback/feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(feedback_data, f, indent=2)
                
            return jsonify({'message': 'Feedback submitted successfully'}), 200
        except Exception as e:
            app.logger.error(f"Error submitting feedback: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    # Register blueprints
    register_blueprints(app)

    return app

def configure_database(app):
    """Configure database connections"""
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///smartprobono.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configure MongoDB if used
    app.config['MONGO_URI'] = os.environ.get(
        'MONGO_URI', 'mongodb://localhost:27017/smartprobono'
    )
    
    # Configure Redis if available
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    app.config['REDIS_URL'] = redis_url

def setup_extensions(app):
    """Set up Flask extensions"""
    try:
        # Mail configuration
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@smartprobono.org')
        
        # JWT configuration
        app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY', 'dev-key'))
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
        
        # Initialize extensions with error handling
        try:
            from flask_jwt_extended import JWTManager
            jwt = JWTManager(app)
            app.logger.info("JWT Manager initialized")
        except ImportError:
            app.logger.warning("JWT Manager not available")
            
        try:
            from flask_mail import Mail
            mail = Mail(app)
            app.logger.info("Mail initialized")
        except ImportError:
            app.logger.warning("Mail not available")
            
        try:
            from flask_sqlalchemy import SQLAlchemy
            from flask_migrate import Migrate
            db = SQLAlchemy(app)
            migrate = Migrate(app, db)
            app.logger.info("Database initialized")
        except ImportError:
            app.logger.warning("SQLAlchemy not available")
            
        try:
            from flask_pymongo import PyMongo
            mongo = PyMongo(app)
            app.logger.info("MongoDB initialized")
        except ImportError:
            app.logger.warning("PyMongo not available")
        
    except Exception as e:
        app.logger.error(f"Error setting up extensions: {str(e)}")

def register_blueprints(app):
    """Register blueprints with error handling"""
    # Try to register admin blueprint
    try:
        # Create a simple admin blueprint
        from flask import Blueprint
        admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
        
        @admin_bp.route('/health', methods=['GET'])
        def admin_health():
            return jsonify({
                'status': 'ok',
                'message': 'Admin API is running',
                'version': '1.0.0'
            })
            
        app.register_blueprint(admin_bp)
        app.logger.info("Registered admin blueprint")
        
    except Exception as e:
        app.logger.error(f"Error registering admin blueprint: {str(e)}")
    
    # Try to register auth blueprint
    try:
        from routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.logger.info("Registered auth blueprint")
    except Exception as e:
        app.logger.error(f"Error registering auth blueprint: {str(e)}")
        
    # Try to register documents blueprint
    try:
        from routes.documents import bp as documents_bp
        app.register_blueprint(documents_bp, url_prefix='/api/documents')
        app.logger.info("Registered documents blueprint")
    except Exception as e:
        app.logger.error(f"Error registering documents blueprint: {str(e)}")
    
    # Try to register other blueprints
    blueprints = [
        ('routes.immigration', '/api/immigration'),
        ('routes.intake', '/api/intake'),
        ('routes.legal_ai', '/api/legal-ai'),
        ('routes.templates', '/api/templates'),
        ('routes.document_scanner', '/api/scanner'),
    ]
    
    for module_name, url_prefix in blueprints:
        try:
            module = __import__(module_name, fromlist=['bp'])
            app.register_blueprint(module.bp, url_prefix=url_prefix)
            app.logger.info(f"Registered {module_name} blueprint")
        except Exception as e:
            app.logger.error(f"Error registering {module_name} blueprint: {str(e)}")

def setup_logging(app):
    """Set up logging for the application"""
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

def create_required_dirs():
    """Create required directories for the application"""
    directories = [
        'data',
        'data/feedback',
        'data/conversations',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Create the application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))


