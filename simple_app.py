from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import secrets
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_mail import Mail
from logging.handlers import RotatingFileHandler

# Import database modules
from database import db, migrate, init_db

# Import utils
from utils.logging_setup import setup_logging
from utils.error_handlers import register_error_handlers

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    """
    Create and configure the Flask application
    
    Args:
        test_config: Configuration for testing
        
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_for_development_only'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'jwt_dev_key_for_development_only'),
        DATABASE_URI=os.environ.get('DATABASE_URI', None),
        JWT_ACCESS_TOKEN_EXPIRES=60 * 60,  # 1 hour
        JWT_REFRESH_TOKEN_EXPIRES=30 * 24 * 60 * 60,  # 30 days
        DEBUG=os.environ.get('FLASK_DEBUG', 'False') == 'True',
        SERVER_START_TIME=datetime.utcnow().isoformat(),
        CORS_ALLOWED_ORIGINS=os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:3100')
    )
    
    if test_config:
        app.config.update(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Set up CORS
    allowed_origins = app.config['CORS_ALLOWED_ORIGINS'].split(',')
    CORS(app, supports_credentials=True, origins=allowed_origins)
    
    # Set up JWT
    jwt = JWTManager(app)
    
    # Set up logging
    setup_logging(app)
    
    # Initialize database
    init_db(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Setup JWT blacklist for logout
    jwt_blacklist = set()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in jwt_blacklist
    
    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400
    
    @app.errorhandler(500)
    def server_error(error):
        app.logger.error(f"Server error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    # Simple ping endpoint for connection checking
    @app.route('/api/ping', methods=['GET'])
    def ping():
        """Simple endpoint to check if API server is running"""
        return jsonify({
            "status": "ok",
            "message": "API server is running",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    # Register blueprints
    try:
        from routes.auth import auth_bp  # type: ignore
        app.register_blueprint(auth_bp)
    except ImportError:
        app.logger.warning("Could not import auth blueprint")
    
    try:
        from routes.immigration import immigration_bp  # type: ignore
        app.register_blueprint(immigration_bp)
    except ImportError:
        app.logger.warning("Could not import immigration blueprint")
    
    try:
        from routes.documents import documents_bp  # type: ignore
        app.register_blueprint(documents_bp)
        app.logger.info("Successfully imported documents blueprint")
    except ImportError as e:
        app.logger.warning(f"Could not import documents blueprint: {str(e)}")
    
    # Register other blueprints
    try:
        from routes.expungement import expungement_bp  # type: ignore
        app.register_blueprint(expungement_bp)
    except ImportError:
        app.logger.warning("Could not import expungement blueprint")
    
    try:
        from routes.contracts import contracts_bp  # type: ignore
        app.register_blueprint(contracts_bp)
    except ImportError:
        app.logger.warning("Could not import contracts blueprint")
    
    try:
        from routes.legal_ai import legal_ai_bp  # type: ignore
        app.register_blueprint(legal_ai_bp)
    except ImportError:
        app.logger.warning("Could not import legal AI blueprint")
    
    try:
        from routes.admin import admin_bp
        app.register_blueprint(admin_bp)
    except ImportError:
        app.logger.warning("Could not import admin blueprint")
    
    try:
        from routes.paralegal import paralegal_bp
        app.register_blueprint(paralegal_bp)
        app.logger.info("Successfully imported paralegal blueprint")
    except ImportError:
        app.logger.warning("Could not import paralegal blueprint")
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint that matches the screenshot"""
        return jsonify({
            "message": "API is running",
            "status": "ok",
            "version": "1.0.0"
        })
    
    @app.route('/api/beta/signup', methods=['POST'])
    def signup():
        """Handle signup requests with email"""
        try:
            data = request.get_json()
            email = data.get('email', '')
            
            if not email or '@' not in email:
                return jsonify({"status": "error", "message": "Invalid email address"}), 400
            
            # In a real application, you would save this to a database
            print(f"Received signup for email: {email}")
            
            return jsonify({
                "status": "success", 
                "message": "Thank you for signing up! We'll be in touch soon."
            })
        except Exception as e:
            print(f"Error processing signup: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5003))
    
    # Run the app with Flask dev server instead of SocketIO
    app.run(host='0.0.0.0', port=port, debug=True) 