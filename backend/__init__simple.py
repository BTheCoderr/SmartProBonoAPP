"""
SmartProBono Backend Package - Simplified Version
"""
from flask import Flask
import logging
import os
from dotenv import load_dotenv

from .extensions_simple import cors
from .config import config

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

def create_app(config_object=None):
    """Create and configure the Flask application - Simplified version"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_object(config_object)
    
    # Initialize only essential extensions
    cors.init_app(app)
    
    # Register blueprints
    from .routes import register_blueprints
    register_blueprints(app)
    
    return app
