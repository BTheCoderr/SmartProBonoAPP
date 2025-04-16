import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Notification types
NOTIFICATION_TYPE_INFO = 'info'
NOTIFICATION_TYPE_SUCCESS = 'success'
NOTIFICATION_TYPE_WARNING = 'warning'
NOTIFICATION_TYPE_ERROR = 'error'

# Event categories
EVENT_CATEGORY_CASE = 'case'
EVENT_CATEGORY_DOCUMENT = 'document'
EVENT_CATEGORY_APPOINTMENT = 'appointment'
EVENT_CATEGORY_MESSAGE = 'message'
EVENT_CATEGORY_SYSTEM = 'system'

# Entity types
ENTITY_TYPE_CASE = 'case'
ENTITY_TYPE_DOCUMENT = 'document'
ENTITY_TYPE_APPOINTMENT = 'appointment'
ENTITY_TYPE_MESSAGE = 'message'
ENTITY_TYPE_LEGAL_AI = 'legal_ai'
ENTITY_TYPE_SYSTEM = 'system'

def create_case_status_notification(user_id, case_id, case_title, old_status, new_status):
    """
    Create a notification for a case status change
    
    Args:
        user_id (str): The ID of the user to notify
        case_id (str): The ID of the case
        case_title (str): The title of the case
        old_status (str): The previous status
        new_status (str): The new status
        
    Returns:
        dict: A notification object
    """
    notification_type = NOTIFICATION_TYPE_INFO
    if new_status in ['approved', 'completed', 'resolved']:
        notification_type = NOTIFICATION_TYPE_SUCCESS
    elif new_status in ['rejected', 'canceled']:
        notification_type = NOTIFICATION_TYPE_ERROR
    elif new_status in ['on_hold', 'pending_info']:
        notification_type = NOTIFICATION_TYPE_WARNING
    
    return {
        'title': f'Case Status Update: {case_title}',
        'message': f'Your case has been updated from "{old_status}" to "{new_status}".',
        'type': notification_type,
        'actionUrl': f'/cases/{case_id}',
        'relatedEntityId': case_id,
        'relatedEntityType': EVENT_CATEGORY_CASE
    }

def create_document_notification(user_id, document_id, document_title, event_type):
    """
    Create a notification for document processing events
    
    Args:
        user_id (str): The ID of the user to notify
        document_id (str): The ID of the document
        document_title (str): The title of the document
        event_type (str): The type of event ('completed', 'failed', etc.)
        
    Returns:
        dict: A notification object
    """
    notification_type = NOTIFICATION_TYPE_INFO
    message = f'Your document "{document_title}" is being processed.'
    action_url = f'/document-generator/{document_id}'
    
    if event_type == 'completed':
        notification_type = NOTIFICATION_TYPE_SUCCESS
        message = f'Your document "{document_title}" has been successfully processed.'
    elif event_type == 'failed':
        notification_type = NOTIFICATION_TYPE_ERROR
        message = f'Processing of document "{document_title}" failed. Please try again.'
    elif event_type == 'review_needed':
        notification_type = NOTIFICATION_TYPE_WARNING
        message = f'Your document "{document_title}" needs review.'
        
    return {
        'title': f'Document Update: {document_title}',
        'message': message,
        'type': notification_type,
        'actionUrl': action_url,
        'relatedEntityId': document_id,
        'relatedEntityType': EVENT_CATEGORY_DOCUMENT
    }

def create_appointment_notification(user_id, appointment_id, attorney_name, appointment_time, event_type):
    """
    Create a notification for appointment-related events
    
    Args:
        user_id (str): The ID of the user to notify
        appointment_id (str): The ID of the appointment
        attorney_name (str): The name of the attorney
        appointment_time (datetime): The time of the appointment
        event_type (str): The type of event ('reminder', 'scheduled', 'canceled', etc.)
        
    Returns:
        dict: A notification object
    """
    notification_type = NOTIFICATION_TYPE_INFO
    formatted_time = appointment_time.strftime('%B %d, %Y at %I:%M %p')
    
    if event_type == 'reminder':
        notification_type = NOTIFICATION_TYPE_INFO
        title = 'Appointment Reminder'
        message = f'Your appointment with {attorney_name} is scheduled for {formatted_time}.'
    elif event_type == 'scheduled':
        notification_type = NOTIFICATION_TYPE_SUCCESS
        title = 'Appointment Scheduled'
        message = f'Your appointment with {attorney_name} has been scheduled for {formatted_time}.'
    elif event_type == 'canceled':
        notification_type = NOTIFICATION_TYPE_WARNING
        title = 'Appointment Canceled'
        message = f'Your appointment with {attorney_name} for {formatted_time} has been canceled.'
    elif event_type == 'rescheduled':
        notification_type = NOTIFICATION_TYPE_INFO
        title = 'Appointment Rescheduled'
        message = f'Your appointment with {attorney_name} has been rescheduled to {formatted_time}.'
    else:
        title = 'Appointment Update'
        message = f'There has been an update to your appointment with {attorney_name} for {formatted_time}.'
    
    return {
        'title': title,
        'message': message,
        'type': notification_type,
        'actionUrl': f'/appointments/{appointment_id}',
        'relatedEntityId': appointment_id,
        'relatedEntityType': EVENT_CATEGORY_APPOINTMENT
    }

def create_message_notification(user_id, sender_name, room_id, room_name, preview_text):
    """
    Create a notification for new message events
    
    Args:
        user_id (str): The ID of the user to notify
        sender_name (str): The name of the message sender
        room_id (str): The ID of the chat room
        room_name (str): The name of the chat room
        preview_text (str): A preview of the message content (truncated)
        
    Returns:
        dict: A notification object
    """
    # Truncate message preview if too long
    if len(preview_text) > 50:
        preview_text = preview_text[:47] + '...'
    
    return {
        'title': f'New message in {room_name}',
        'message': f'{sender_name}: {preview_text}',
        'type': NOTIFICATION_TYPE_INFO,
        'actionUrl': f'/chat-room/{room_id}',
        'relatedEntityId': room_id,
        'relatedEntityType': EVENT_CATEGORY_MESSAGE
    }

def create_legal_response_notification(user_id, query_id, preview_text):
    """
    Create a notification for legal AI response
    
    Args:
        user_id (str): The ID of the user to notify
        query_id (str): The ID of the legal query
        preview_text (str): A preview of the response (truncated)
        
    Returns:
        dict: A notification object
    """
    # Truncate message preview if too long
    if len(preview_text) > 50:
        preview_text = preview_text[:47] + '...'
    
    return {
        'title': 'Legal Assistant Response',
        'message': f'Your legal query has been answered: {preview_text}',
        'type': NOTIFICATION_TYPE_INFO,
        'actionUrl': f'/legal-chat?query={query_id}',
        'relatedEntityId': query_id,
        'relatedEntityType': 'legal_query'
    }

def create_system_notification(user_id, title, message, action_url=None, notification_type=NOTIFICATION_TYPE_INFO):
    """
    Create a generic system notification
    
    Args:
        user_id (str): The ID of the user to notify
        title (str): The notification title
        message (str): The notification message
        action_url (str, optional): URL to navigate to when clicked
        notification_type (str, optional): The notification type
        
    Returns:
        dict: A notification object
    """
    notification = {
        'title': title,
        'message': message,
        'type': notification_type,
        'relatedEntityType': EVENT_CATEGORY_SYSTEM
    }
    
    if action_url:
        notification['actionUrl'] = action_url
        
    return notification

def should_send_notification(user_id, notification_type, entity_type, channel="app"):
    """
    Check if a user should receive notifications of a particular type.
    
    Args:
        user_id (str): The user ID
        notification_type (str): Type of notification (info, success, warning, error)
        entity_type (str): Type of entity (case, document, appointment, message, legal_ai, system)
        channel (str): The channel to check (app, email, browser)
        
    Returns:
        bool: True if the user should receive the notification, False otherwise
    """
    try:
        from models.user_notification_preferences import UserNotificationPreferences

        # Get user preferences
        prefs = UserNotificationPreferences.get_by_user_id(user_id)
        
        # Map entity type to preference field
        entity_map = {
            ENTITY_TYPE_CASE: "case_updates",
            ENTITY_TYPE_DOCUMENT: "document_updates",
            ENTITY_TYPE_APPOINTMENT: "appointment_reminders",
            ENTITY_TYPE_MESSAGE: "messages",
            ENTITY_TYPE_LEGAL_AI: "legal_ai_responses",
            ENTITY_TYPE_SYSTEM: "system_announcements"
        }
        
        # Default to true if entity_type is not recognized
        if entity_type not in entity_map:
            return True
            
        # Get the preference field name
        pref_field = entity_map[entity_type]
        
        # Check the appropriate channel preference
        if channel == "app":
            attribute = f"app_{pref_field}"
        elif channel == "email":
            attribute = f"email_{pref_field}"
        elif channel == "browser":
            attribute = f"browser_{pref_field}"
        else:
            # Unknown channel, default to true
            return True
            
        # Get the preference value
        return getattr(prefs, attribute, True)
        
    except Exception as e:
        # Log the error and default to True
        import logging
        logging.error(f"Error checking notification preferences: {str(e)}")
        return True 