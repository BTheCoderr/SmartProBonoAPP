"""Register all route blueprints"""

def register_blueprints(app):
    """Register all route blueprints with the Flask app"""
    
    # UNIFIED API - Single source of truth for all operations
    try:
        from .unified_api import bp as unified_api_bp
        app.register_blueprint(unified_api_bp)
        print("✅ Unified API routes registered")
    except ImportError as e:
        print(f"⚠️ Unified API routes not available: {e}")
    
    # LEGACY ROUTES - Keep for backward compatibility but mark as deprecated
    try:
        from .legal_ai import bp as legal_ai_bp
        app.register_blueprint(legal_ai_bp, url_prefix='/api/legal')
        print("✅ Legal AI routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Legal AI routes not available: {e}")
    
    try:
        from .documents import bp as documents_bp
        app.register_blueprint(documents_bp, url_prefix='/api/documents')
        print("✅ Document routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Document routes not available: {e}")
    
    try:
        from .templates import bp as templates_bp
        app.register_blueprint(templates_bp, url_prefix='/api/templates')
        print("✅ Template routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Template routes not available: {e}")
    
    try:
        from .intake import bp as intake_bp
        app.register_blueprint(intake_bp, url_prefix='/api/intake')
        print("✅ Intake routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Intake routes not available: {e}")
    
    try:
        from .immigration import bp as immigration_bp
        app.register_blueprint(immigration_bp, url_prefix='/api/immigration')
        print("✅ Immigration routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Immigration routes not available: {e}")
    
    try:
        from .document_scanner import bp as document_scanner_bp
        app.register_blueprint(document_scanner_bp, url_prefix='/api/scanner')
        print("✅ Document scanner routes registered (LEGACY)")
    except ImportError as e:
        print(f"⚠️ Document scanner routes not available: {e}")
    
    try:
        from .audit import audit_bp
        app.register_blueprint(audit_bp)
        print("✅ Audit routes registered")
    except ImportError as e:
        print(f"⚠️ Audit routes not available: {e}")
    
    try:
        from .contact import contact_bp
        app.register_blueprint(contact_bp)
        print("✅ Contact routes registered")
    except ImportError as e:
        print(f"⚠️ Contact routes not available: {e}")
    
    try:
        from .virtual_paralegal_crm import bp as virtual_paralegal_crm_bp
        app.register_blueprint(virtual_paralegal_crm_bp)
        print("✅ Virtual Paralegal CRM routes registered")
    except ImportError as e:
        print(f"⚠️ Virtual Paralegal CRM routes not available: {e}")
    
    try:
        from .ai_virtual_paralegal import bp as ai_virtual_paralegal_bp
        app.register_blueprint(ai_virtual_paralegal_bp)
        print("✅ AI Virtual Paralegal routes registered")
    except ImportError as e:
        print(f"⚠️ AI Virtual Paralegal routes not available: {e}")