"""Authentication module"""
from .decorators import admin_required, paralegal_required, client_required

__all__ = ['admin_required', 'paralegal_required', 'client_required'] 