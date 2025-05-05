"""
Websocket module for compatibility

This file exists to make imports like `from backend.websocket import X` work
when the code is deployed in different environments.

This version contains mock implementations to allow the app to start without
the actual websocket package.
"""

# Mock SocketIO instance
class MockSocketIO:
    def __init__(self):
        pass
    
    def run(self, app, **kwargs):
        print("MOCK: SocketIO.run called")
        return app
    
    def on(self, event, namespace=None):
        def decorator(f):
            print(f"MOCK: Registered event handler for {event}")
            return f
        return decorator
    
    def emit(self, event, data=None, room=None, namespace=None):
        print(f"MOCK: Emit {event} to {room or 'all'}")
        return True

# Create a mock SocketIO instance
socketio = MockSocketIO()

# Mock notification types
NOTIFICATION_TYPE_INFO = 'info'
NOTIFICATION_TYPE_SUCCESS = 'success'
NOTIFICATION_TYPE_WARNING = 'warning'
NOTIFICATION_TYPE_ERROR = 'error'

# Mock categories
CATEGORY_IMMIGRATION = 'immigration'
CATEGORY_DOCUMENTS = 'documents'
CATEGORY_MESSAGES = 'messages'
CATEGORY_SYSTEM = 'system'
CATEGORY_CASE = 'case'
CATEGORY_APPOINTMENT = 'appointment'

# Export all notification types and categories in a single dict
NOTIFICATION_TYPES = {
    'INFO': NOTIFICATION_TYPE_INFO,
    'SUCCESS': NOTIFICATION_TYPE_SUCCESS,
    'WARNING': NOTIFICATION_TYPE_WARNING,
    'ERROR': NOTIFICATION_TYPE_ERROR
}

# Mock functions
def init_websocket(app):
    """Mock function to initialize websocket"""
    print("MOCK: Websocket initialized")
    return app

def send_notification(user_id, title, message, notification_type, category='system', data=None):
    """Mock function for sending a notification to a specific user"""
    print(f"MOCK: Sending notification to {user_id}: {title} - {message}")
    return True

def send_broadcast_notification(title, message, notification_type, category='system', data=None, persist=True, exclude_users=None):
    """Mock function for sending broadcast notifications"""
    print(f"MOCK: Broadcasting notification: {title} - {message}")
    return True

def get_connected_users():
    """Mock function for getting connected users"""
    return []

def get_connection_stats():
    """Mock function for getting connection statistics"""
    return {
        'total_connections': 0,
        'active_users': 0,
        'connections_by_role': {}
    }

def is_user_connected(user_id):
    """Mock function to check if a user is connected"""
    return False

def get_user_notifications(user_id, limit=10, offset=0):
    """Mock function to get user notifications"""
    return []

def mark_notification_read(notification_id, user_id):
    """Mock function to mark a notification as read"""
    return True

def delete_notification(notification_id, user_id):
    """Mock function to delete a notification"""
    return True

def get_notification_stats():
    """Mock function for getting notification statistics"""
    return {
        'total': 0,
        'read': 0,
        'unread': 0
    }

# Specialized notification functions
def send_user_notification(user_id, title, message, notification_type, category='system', data=None):
    """Mock function for sending a user notification"""
    return send_notification(user_id, title, message, notification_type, category, data)

def send_case_status_update(user_id, case_id, new_status, details=None):
    """Mock function for sending a case status update"""
    title = f"Case #{case_id} Status Updated"
    message = f"Your case has been updated to: {new_status}"
    data = {'case_id': case_id, 'new_status': new_status, 'details': details}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_INFO, CATEGORY_CASE, data)

def send_document_request(user_id, document_name, case_id=None):
    """Mock function for sending a document request"""
    title = "Document Request"
    message = f"Please upload the following document: {document_name}"
    data = {'document_name': document_name, 'case_id': case_id}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_INFO, CATEGORY_DOCUMENTS, data)

def send_document_uploaded_notification(user_id, document_name, case_id=None):
    """Mock function for sending a document uploaded notification"""
    title = "Document Uploaded"
    message = f"The document {document_name} has been uploaded"
    data = {'document_name': document_name, 'case_id': case_id}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_SUCCESS, CATEGORY_DOCUMENTS, data)

def send_appointment_reminder(user_id, appointment_id, appointment_date, details=None):
    """Mock function for sending an appointment reminder"""
    title = "Appointment Reminder"
    message = f"You have an appointment scheduled for {appointment_date}"
    data = {'appointment_id': appointment_id, 'appointment_date': appointment_date, 'details': details}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_INFO, CATEGORY_APPOINTMENT, data)

def send_message_notification(user_id, from_user, subject=None):
    """Mock function for sending a message notification"""
    title = "New Message"
    message = f"You have received a new message from {from_user}"
    if subject:
        message += f" regarding {subject}"
    data = {'from_user': from_user, 'subject': subject}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_INFO, CATEGORY_MESSAGES, data)

def send_immigration_form_notification(user_id, form_name, status, details=None):
    """Mock function for sending an immigration form notification"""
    title = f"Immigration Form Update: {form_name}"
    message = f"The status of your {form_name} form is now: {status}"
    data = {'form_name': form_name, 'status': status, 'details': details}
    return send_notification(user_id, title, message, NOTIFICATION_TYPE_INFO, CATEGORY_IMMIGRATION, data) 