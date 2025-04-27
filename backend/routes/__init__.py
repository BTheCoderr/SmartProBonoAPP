"""Routes package initialization."""
from .admin import bp as admin_bp
from .auth import bp as auth_bp
from .documents import bp as document_bp
from .immigration import bp as immigration_bp
from .intake import bp as intake_bp
from .rights import bp as rights_bp
from .document_scanner import scanner_bp
from .templates import bp as template_bp
from .notifications import bp as notifications_bp

__all__ = [
    'admin_bp',
    'auth_bp',
    'document_bp',
    'immigration_bp',
    'intake_bp',
    'rights_bp',
    'scanner_bp',
    'template_bp',
    'notifications_bp'
]
