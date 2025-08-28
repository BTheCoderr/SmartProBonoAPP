"""
WebSocket module for SmartProBono
"""
from websocket.core import (
    socketio, 
    init_websocket
)
from websocket.services.notification_service import (
    send_notification,
    send_broadcast_notification,
    get_user_notifications,
    mark_notification_read,
    delete_notification,
    get_notification_stats,
    NOTIFICATION_TYPES
)
from websocket.services.connection_service import (
    get_connected_users,
    get_connection_stats,
    is_user_connected
)
from websocket.services.application_notifications import (
    send_user_notification,
    send_case_status_update,
    send_document_request,
    send_document_uploaded_notification,
    send_appointment_reminder,
    send_message_notification,
    send_immigration_form_notification,
    CATEGORY_IMMIGRATION,
    CATEGORY_DOCUMENTS,
    CATEGORY_MESSAGES,
    CATEGORY_SYSTEM,
    CATEGORY_CASE,
    CATEGORY_APPOINTMENT
)

# Define notification types as constants for external use
NOTIFICATION_TYPE_INFO = 'info'
NOTIFICATION_TYPE_SUCCESS = 'success'
NOTIFICATION_TYPE_WARNING = 'warning'
NOTIFICATION_TYPE_ERROR = 'error'

__all__ = [
    'socketio',
    'init_websocket',
    'send_notification',
    'send_broadcast_notification',
    'get_connected_users',
    'get_connection_stats',
    'is_user_connected',
    'get_user_notifications',
    'mark_notification_read',
    'delete_notification',
    'get_notification_stats',
    'NOTIFICATION_TYPES',
    'NOTIFICATION_TYPE_INFO',
    'NOTIFICATION_TYPE_SUCCESS',
    'NOTIFICATION_TYPE_WARNING',
    'NOTIFICATION_TYPE_ERROR',
    'CATEGORY_IMMIGRATION',
    'CATEGORY_DOCUMENTS',
    'CATEGORY_MESSAGES',
    'CATEGORY_SYSTEM',
    'CATEGORY_CASE',
    'CATEGORY_APPOINTMENT',
    'send_user_notification',
    'send_case_status_update',
    'send_document_request',
    'send_document_uploaded_notification',
    'send_appointment_reminder',
    'send_message_notification',
    'send_immigration_form_notification'
] 