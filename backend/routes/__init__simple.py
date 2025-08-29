"""Register all route blueprints"""

def register_blueprints(app):
    """Register all route blueprints with the Flask app"""
    try:
        from .legal_ai import bp as legal_ai_bp
        app.register_blueprint(legal_ai_bp, url_prefix='/api/legal')
        print("✅ Legal AI routes registered")
    except ImportError as e:
        print(f"⚠️ Legal AI routes not available: {e}")
    
    try:
        from .documents import bp as documents_bp
        app.register_blueprint(documents_bp, url_prefix='/api/documents')
        print("✅ Document routes registered")
    except ImportError as e:
        print(f"⚠️ Document routes not available: {e}")
    
    try:
        from .templates import bp as templates_bp
        app.register_blueprint(templates_bp, url_prefix='/api/templates')
        print("✅ Template routes registered")
    except ImportError as e:
        print(f"⚠️ Template routes not available: {e}")
    
    try:
        from .intake import bp as intake_bp
        app.register_blueprint(intake_bp, url_prefix='/api/intake')
        print("✅ Intake routes registered")
    except ImportError as e:
        print(f"⚠️ Intake routes not available: {e}")
    
    try:
        from .immigration import bp as immigration_bp
        app.register_blueprint(immigration_bp, url_prefix='/api/immigration')
        print("✅ Immigration routes registered")
    except ImportError as e:
        print(f"⚠️ Immigration routes not available: {e}")
    
    try:
        from .document_scanner import bp as document_scanner_bp
        app.register_blueprint(document_scanner_bp, url_prefix='/api/scanner')
        print("✅ Document scanner routes registered")
    except ImportError as e:
        print(f"⚠️ Document scanner routes not available: {e}")
    
    try:
        from .audit import audit_bp
        app.register_blueprint(audit_bp)
        print("✅ Audit routes registered")
    except ImportError as e:
        print(f"⚠️ Audit routes not available: {e}")