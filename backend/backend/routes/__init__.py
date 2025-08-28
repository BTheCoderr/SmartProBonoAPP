"""
Routes package initialization.
"""
import logging
from flask import Blueprint, jsonify

logger = logging.getLogger(__name__)

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
        # Register health check blueprint first so it's always available
        try:
            from .health import bp as health_bp
            app.register_blueprint(health_bp)
            app.logger.info("Registered health blueprint")
        except ImportError as e:
            app.logger.error(f"Error registering health blueprint: {str(e)}")
            
        # Register admin blueprint
        try:
            from .admin import bp as admin_bp
            app.register_blueprint(admin_bp)
            app.logger.info("Registered admin blueprint")
        except ImportError as e:
            app.logger.error(f"Error registering admin blueprint: {str(e)}")

        # Register auth blueprint - handle missing fastapi_mail
        try:
            # First check if the problematic dependency exists
            try:
                import fastapi_mail
            except ImportError:
                # Create a modified version of the auth module without the dependency
                auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
                
                @auth_bp.route('/login', methods=['POST'])
                def login():
                    return jsonify({"message": "Auth module disabled due to missing dependencies"})
                    
                app.register_blueprint(auth_bp)
                app.logger.warning("Registered minimal auth blueprint (fastapi_mail missing)")
            else:
                from .auth import bp as auth_bp
                app.register_blueprint(auth_bp)
                app.logger.info("Registered auth blueprint")
        except Exception as e:
            app.logger.error(f"Error registering auth blueprint: {str(e)}")

        # Register documents blueprint - handle missing fastapi_mail
        try:
            # First check if the problematic dependency exists
            try:
                import fastapi_mail
            except ImportError:
                # Create a modified version of the documents module
                documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')
                
                @documents_bp.route('/', methods=['GET'])
                def get_documents():
                    return jsonify({"message": "Documents module disabled due to missing dependencies"})
                    
                app.register_blueprint(documents_bp)
                app.logger.warning("Registered minimal documents blueprint (fastapi_mail missing)")
            else:
                from .documents import bp as documents_bp
                app.register_blueprint(documents_bp)
                app.logger.info("Registered documents blueprint")
        except Exception as e:
            app.logger.error(f"Error registering documents blueprint: {str(e)}")

        # Register other blueprints
        blueprint_modules = [
            ('routes.intake', '/api/intake'),
            ('routes.legal_ai', '/api/legal-ai'),
            ('routes.templates', '/api/templates'),
            ('routes.immigration', '/api/immigration'),
        ]

        for module_name, url_prefix in blueprint_modules:
            try:
                short_name = module_name.split('.')[-1]
                try:
                    # This will fail if there's a module import issue
                    module = __import__(module_name, fromlist=['bp'])
                    app.register_blueprint(module.bp, url_prefix=url_prefix)
                    app.logger.info(f"Registered {module_name} blueprint")
                except ImportError as e:
                    # Create a minimal blueprint
                    bp = Blueprint(short_name, __name__, url_prefix=url_prefix)
                    
                    @bp.route('/', methods=['GET'])
                    def index():
                        return jsonify({"message": f"{short_name} module disabled due to import error: {str(e)}"})
                        
                    app.register_blueprint(bp)
                    app.logger.warning(f"Registered minimal {short_name} blueprint (import error)")
            except Exception as e:
                app.logger.error(f"Error registering {module_name} blueprint: {str(e)}")

        # Handle document_scanner blueprint which requires pdf2image
        try:
            try:
                import pdf2image
                from .document_scanner import bp as scanner_bp
                app.register_blueprint(scanner_bp)
                app.logger.info("Registered scanner blueprint")
            except ImportError as e:
                # Create minimal scanner blueprint
                scanner_bp = Blueprint('scanner', __name__, url_prefix='/api/scanner')
                
                @scanner_bp.route('/', methods=['GET'])
                def scanner_status():
                    return jsonify({"message": "Scanner functionality disabled. Missing dependency: pdf2image"})
                    
                app.register_blueprint(scanner_bp)
                app.logger.warning(f"Registered minimal scanner blueprint (import error: {str(e)})")
        except Exception as e:
            app.logger.error(f"Error registering document_scanner blueprint: {str(e)}")

    except Exception as e:
        app.logger.error(f"Error registering blueprints: {str(e)}")
        # Register a minimal health check blueprint at minimum
        from flask import Blueprint, jsonify
        
        health_bp = Blueprint('health', __name__, url_prefix='/api/health')
        
        @health_bp.route('/', methods=['GET'])
        def health_check():
            return jsonify({'status': 'ok', 'message': 'API is running with minimal functionality'})
        
        app.register_blueprint(health_bp)
