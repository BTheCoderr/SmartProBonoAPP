from flask import Blueprint
from .auth import auth_bp
from .cases import cases_bp
from .documents import documents_bp
from .legal_ai import legal_ai_bp
from .safety_monitor_routes import safety_monitor_bp
from .user_routes import user_bp
from .admin import admin_bp
from .contracts import contracts_bp
from .document_analysis import document_analysis_bp
from .document_generator import document_generator_bp
from .emergency_legal_support import emergency_legal_support_bp
from .immigration import immigration_bp
from .matching import matching_bp
from .notification_routes import notification_bp
from .performance import performance_bp
from .priority_queue_routes import priority_queue_bp
from .security_routes import security_bp
from .support import support_bp
from .availability_routes import availability_bp
from .encryption_routes import encryption_bp
from .case_routes import case_routes_bp
from .case_batch_routes import case_batch_bp
from .safety_monitor import safety_monitor_core_bp

def register_routes(app):
    """Register all route blueprints with the Flask app."""
    blueprints = [
        auth_bp,
        cases_bp,
        documents_bp,
        legal_ai_bp,
        safety_monitor_bp,
        user_bp,
        admin_bp,
        contracts_bp,
        document_analysis_bp,
        document_generator_bp,
        emergency_legal_support_bp,
        immigration_bp,
        matching_bp,
        notification_bp,
        performance_bp,
        priority_queue_bp,
        security_bp,
        support_bp,
        availability_bp,
        encryption_bp,
        case_routes_bp,
        case_batch_bp,
        safety_monitor_core_bp
    ]
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
