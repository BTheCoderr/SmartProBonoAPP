"""Backend package initialization."""
from flask import Flask
from flask_cors import CORS
import os
import logging
import sys

logger = logging.getLogger(__name__)

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extensions import db, mongo, mail, socketio, jwt, migrate, limiter
from database import init_db

def create_app(config_object=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load config
    if config_object is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_object(config_object)
    
    # Initialize extensions
    jwt.init_app(app)
    logger.info("JWT Manager initialized")
    
    mail.init_app(app)
    logger.info("Mail initialized")
    
    init_db(app)
    logger.info("Database initialized")
    
    mongo.init_app(app)
    logger.info("MongoDB initialized")
    
    # Setup CORS
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "https://smartprobono.org",
                "https://www.smartprobono.org",
                "https://smartprobono.netlify.app",
                "https://smartprobono.netlify.com"
            ]
        }
    })
    logger.info("CORS configured with origins: %s", app.config.get('CORS_ORIGINS', []))
    
    # Register blueprints
    from backend.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    logger.info("Registered admin blueprint")
    
    # Try to register other blueprints - catching errors so app still starts
    try:
        from backend.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        logger.info("Registered auth blueprint")
    except Exception as e:
        logger.error("Error registering auth blueprint: %s", str(e))
    
    try:
        from backend.routes.documents import bp as documents_bp
        app.register_blueprint(documents_bp, url_prefix='/api/documents')
        logger.info("Registered documents blueprint")
    except Exception as e:
        logger.error("Error registering documents blueprint: %s", str(e))
    
    try:
        from backend.routes.immigration import bp as immigration_bp
        app.register_blueprint(immigration_bp, url_prefix='/api/immigration')
        logger.info("Registered immigration blueprint")
    except Exception as e:
        logger.error("Error registering routes.immigration blueprint: %s", str(e))
    
    try:
        from backend.routes.intake import bp as intake_bp
        app.register_blueprint(intake_bp, url_prefix='/api/intake')
        logger.info("Registered intake blueprint")
    except Exception as e:
        logger.error("Error registering routes.intake blueprint: %s", str(e))
    
    try:
        from backend.routes.legal_ai import bp as legal_ai_bp
        app.register_blueprint(legal_ai_bp, url_prefix='/api/legal-ai')
        logger.info("Registered legal_ai blueprint")
    except Exception as e:
        logger.error("Error registering routes.legal_ai blueprint: %s", str(e))
    
    try:
        from backend.routes.templates import bp as templates_bp
        app.register_blueprint(templates_bp, url_prefix='/api/templates')
        logger.info("Registered templates blueprint")
    except Exception as e:
        logger.error("Error registering routes.templates blueprint: %s", str(e))
    
    try:
        from backend.routes.document_scanner import bp as document_scanner_bp
        app.register_blueprint(document_scanner_bp, url_prefix='/api/document-scanner')
        logger.info("Registered document_scanner blueprint")
    except Exception as e:
        logger.error("Error registering routes.document_scanner blueprint: %s", str(e))
    
    return app 