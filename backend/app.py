"""
Flask application for the SmartProBono backend API
Simplified version that removes problematic imports
"""
import os
import logging
from flask import Flask, jsonify
from logging.handlers import RotatingFileHandler

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
    
    # Add a basic health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'API is running',
            'version': '1.0.0'
        })
    
    # Simplified blueprint registration
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
        app.logger.error(f"Error registering blueprints: {str(e)}")
    
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'SmartProBono API',
            'status': 'running',
            'endpoints': ['/api/health', '/api/admin/health']
        })

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

# Create the application instance
app = create_app('development')


