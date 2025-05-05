"""Routes package initialization"""
from flask import Blueprint

# Create blueprints
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
document_bp = Blueprint('documents', __name__, url_prefix='/api/documents')
immigration_bp = Blueprint('immigration', __name__, url_prefix='/api/immigration')
intake_bp = Blueprint('intake', __name__, url_prefix='/api/intake')
rights_bp = Blueprint('rights', __name__, url_prefix='/api/rights')
scanner_bp = Blueprint('scanner', __name__, url_prefix='/api/scanner')
template_bp = Blueprint('templates', __name__, url_prefix='/api/templates')
beta_bp = Blueprint('beta', __name__, url_prefix='/api/beta')

def register_blueprints(app):
    """Register all blueprints with the application"""
    try:
        # Skip potentially problematic imports and use our simplified admin module
        # Import the simplified admin module from the project root
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from admin import bp as admin_routes
        app.register_blueprint(admin_routes)
        
        try:
            from .auth import bp as auth_routes
            app.register_blueprint(auth_routes)
        except ImportError:
            app.logger.warning("Could not import auth routes")
            
        try:
            from .documents import bp as document_routes
            app.register_blueprint(document_routes)
        except ImportError:
            app.logger.warning("Could not import document routes")
            
        try:
            from .immigration import bp as immigration_routes
            app.register_blueprint(immigration_routes)
        except ImportError:
            app.logger.warning("Could not import immigration routes")
            
        try:
            from .intake import bp as intake_routes
            app.register_blueprint(intake_routes)
        except ImportError:
            app.logger.warning("Could not import intake routes")
            
        try:
            from .rights import bp as rights_routes
            app.register_blueprint(rights_routes)
        except ImportError:
            app.logger.warning("Could not import rights routes")
            
        try:
            from .document_scanner import bp as scanner_routes
            app.register_blueprint(scanner_routes)
        except ImportError:
            app.logger.warning("Could not import scanner routes")
            
        try:
            from .templates import bp as template_routes
            app.register_blueprint(template_routes)
        except ImportError:
            app.logger.warning("Could not import template routes")
            
        try:
            from .beta_routes_flask import bp as beta_routes
            app.register_blueprint(beta_routes)
        except ImportError:
            app.logger.warning("Could not import beta routes")
    
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {str(e)}")
        # Register a minimal health check blueprint at minimum
        from flask import Blueprint, jsonify
        
        health_bp = Blueprint('health', __name__, url_prefix='/api/health')
        
        @health_bp.route('/', methods=['GET'])
        def health_check():
            return jsonify({'status': 'ok', 'message': 'API is running with minimal functionality'})
        
        app.register_blueprint(health_bp)
