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
    from .admin import bp as admin_routes
    from .auth import bp as auth_routes
    from .documents import bp as document_routes
    from .immigration import bp as immigration_routes
    from .intake import bp as intake_routes
    from .rights import bp as rights_routes
    from .document_scanner import bp as scanner_routes
    from .templates import bp as template_routes
    from .beta_routes_flask import bp as beta_routes
    
    app.register_blueprint(admin_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(document_routes)
    app.register_blueprint(immigration_routes)
    app.register_blueprint(intake_routes)
    app.register_blueprint(rights_routes)
    app.register_blueprint(scanner_routes)
    app.register_blueprint(template_routes)
    app.register_blueprint(beta_routes)
