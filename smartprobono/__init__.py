from flask import Flask
from .config import Config
from .extensions import init_extensions, socketio

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    init_extensions(app)

    # auth
    from smartprobono.auth.routes import init_app as auth_init, bp as auth_bp
    auth_init(app)

    # register delegated blueprints
    from smartprobono.documents import bp as documents_bp
    from smartprobono.document_scanner import bp as document_scanner_bp
    from smartprobono.contracts import bp as contracts_bp
    from smartprobono.expungement import bp as expungement_bp
    from smartprobono.form_templates import bp as form_templates_bp
    from smartprobono.immigration import bp as immigration_bp
    from smartprobono.immigration_notifications import bp as immigration_notifications_bp
    from smartprobono.intake import bp as intake_bp
    from smartprobono.legal_ai import bp as legal_ai_bp
    from smartprobono.legal_templates import bp as legal_templates_bp
    from smartprobono.notification import bp as notification_bp
    from smartprobono.notifications import bp as notifications_bp
    from smartprobono.paralegal import bp as paralegal_bp
    from smartprobono.rights import bp as rights_bp
    from smartprobono.uploads import bp as uploads_bp
    from smartprobono.users import bp as users_bp
    from smartprobono.admin import bp as admin_bp
    from smartprobono.performance import bp as performance_bp
    from smartprobono.templates import bp as templates_bp

    blueprints = [
        auth_bp, documents_bp, document_scanner_bp, contracts_bp,
        expungement_bp, form_templates_bp, immigration_bp,
        immigration_notifications_bp, intake_bp, legal_ai_bp,
        legal_templates_bp, notification_bp, notifications_bp,
        paralegal_bp, rights_bp, uploads_bp, users_bp,
        admin_bp, performance_bp, templates_bp
    ]
    for bp in blueprints:
        app.register_blueprint(bp)

    return app