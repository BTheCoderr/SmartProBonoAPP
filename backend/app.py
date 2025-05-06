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
    
    # Setup CORS
    try:
        from flask_cors import CORS
        default_origins = ['http://localhost:3000', 'https://smartprobono.org']
        allowed_origins = os.environ.get('ALLOWED_ORIGINS', ','.join(default_origins)).split(',')
        CORS(app, resources={r"/*": {"origins": allowed_origins}})
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

    return app

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


