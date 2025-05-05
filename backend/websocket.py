"""
Websocket module for compatibility

This file exists to make imports like `from backend.websocket import X` work
when the code is deployed in different environments.
"""

# Re-export everything from the websocket package
from backend.websocket import (
    socketio,
    init_websocket,
    send_notification,
    send_broadcast_notification,
    get_connected_users,
    get_connection_stats,
    is_user_connected,
    get_user_notifications,
    mark_notification_read,
    delete_notification,
    get_notification_stats,
    NOTIFICATION_TYPES,
    NOTIFICATION_TYPE_INFO,
    NOTIFICATION_TYPE_SUCCESS,
    NOTIFICATION_TYPE_WARNING,
    NOTIFICATION_TYPE_ERROR,
    CATEGORY_IMMIGRATION,
    CATEGORY_DOCUMENTS,
    CATEGORY_MESSAGES,
    CATEGORY_SYSTEM,
    CATEGORY_CASE,
    CATEGORY_APPOINTMENT,
    send_user_notification,
    send_case_status_update,
    send_document_request,
    send_document_uploaded_notification,
    send_appointment_reminder,
    send_message_notification,
    send_immigration_form_notification
) 