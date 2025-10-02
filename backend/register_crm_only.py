"""
Register only CRM routes to avoid import issues
"""
def register_crm_blueprints(app):
    """Register only CRM-related blueprints"""
    
    # CRM API - This is the main one we need
    try:
        from routes.crm_api import bp as crm_api_bp
        app.register_blueprint(crm_api_bp)
        print("✅ CRM API routes registered")
    except ImportError as e:
        print(f"⚠️ CRM API routes not available: {e}")
    
    # Virtual Paralegal CRM
    try:
        from routes.virtual_paralegal_crm import bp as virtual_paralegal_crm_bp
        app.register_blueprint(virtual_paralegal_crm_bp)
        print("✅ Virtual Paralegal CRM routes registered")
    except ImportError as e:
        print(f"⚠️ Virtual Paralegal CRM routes not available: {e}")
    
    # AI Virtual Paralegal
    try:
        from routes.ai_virtual_paralegal import bp as ai_virtual_paralegal_bp
        app.register_blueprint(ai_virtual_paralegal_bp)
        print("✅ AI Virtual Paralegal routes registered")
    except ImportError as e:
        print(f"⚠️ AI Virtual Paralegal routes not available: {e}")
    
    # Unified API
    try:
        from routes.unified_api import bp as unified_api_bp
        app.register_blueprint(unified_api_bp)
        print("✅ Unified API routes registered")
    except ImportError as e:
        print(f"⚠️ Unified API routes not available: {e}")
    
    # SmartProBono AI Agent
    try:
        from routes.smartprobono_agent import bp as smartprobono_agent_bp
        app.register_blueprint(smartprobono_agent_bp, url_prefix='/api')
        print("✅ SmartProBono AI Agent routes registered")
    except ImportError as e:
        print(f"⚠️ SmartProBono AI Agent routes not available: {e}")
    
    # Voice AI
    try:
        from routes.voice_ai import bp as voice_ai_bp
        app.register_blueprint(voice_ai_bp, url_prefix='/api')
        print("✅ Voice AI routes registered")
    except ImportError as e:
        print(f"⚠️ Voice AI routes not available: {e}")