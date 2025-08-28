"""
WebSocket Handlers Package.

This package contains event handlers for WebSocket events.
"""

from websocket.handlers.auth_handlers import register_auth_handlers
from websocket.handlers.notification_handlers import register_notification_handlers
from websocket.handlers.admin_handlers import register_admin_handlers

__all__ = [
    'register_auth_handlers',
    'register_notification_handlers',
    'register_admin_handlers'
] 