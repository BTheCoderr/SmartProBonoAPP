"""
Application-specific Notification Services.

This module provides application-specific notification functions
for sending various types of notifications in different contexts.
"""

import logging
from datetime import datetime
from flask import current_app

from websocket.services.notification_service import send_notification

# Configure logging
logger = logging.getLogger('websocket.services.application_notifications')

# Define categories
CATEGORY_IMMIGRATION = 'immigration'
CATEGORY_DOCUMENTS = 'documents'
CATEGORY_MESSAGES = 'messages'
CATEGORY_SYSTEM = 'system'
CATEGORY_CASE = 'case'
CATEGORY_APPOINTMENT = 'appointment'

def send_user_notification(user_id, title, message, notification_type='info', data=None):
    """
    Send a general notification to a user.
    
    Args:
        user_id (str): The user ID to send the notification to
        title (str): Notification title
        message (str): Notification message
        notification_type (str, optional): Type of notification ('info', 'success', 'warning', 'error')
        data (dict, optional): Additional data to include with the notification
        
    Returns:
        dict: The notification object
    """
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        category=CATEGORY_SYSTEM,
        data=data
    )

def send_case_status_update(user_id, case_id, status, details=None):
    """
    Send a case status update notification.
    
    Args:
        user_id (str): The user ID to send the notification to
        case_id (str): The case ID
        status (str): The new status of the case
        details (str, optional): Additional details about the status change
        
    Returns:
        dict: The notification object
    """
    title = "Case Status Update"
    message = f"Your case status has been updated to: {status}"
    if details:
        message += f". {details}"
    
    data = {
        'case_id': case_id,
        'status': status,
        'updated_at': datetime.utcnow().isoformat()
    }
    
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type='info',
        category=CATEGORY_CASE,
        data=data
    )

def send_document_request(user_id, document_type, due_date=None, case_id=None):
    """
    Send a document request notification.
    
    Args:
        user_id (str): The user ID to send the notification to
        document_type (str): The type of document requested
        due_date (str, optional): Due date for the document
        case_id (str, optional): The associated case ID
        
    Returns:
        dict: The notification object
    """
    title = f"Document Request: {document_type}"
    message = f"Please upload your {document_type} document"
    if due_date:
        message += f" by {due_date}"
    
    data = {
        'document_type': document_type,
        'due_date': due_date,
        'case_id': case_id,
        'requested_at': datetime.utcnow().isoformat()
    }
    
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type='warning',  # Warning to emphasize importance
        category=CATEGORY_DOCUMENTS,
        data=data
    )

def send_document_uploaded_notification(attorney_id, client_id, document_type, case_id=None):
    """
    Send a notification when a client uploads a document.
    
    Args:
        attorney_id (str): The attorney's user ID
        client_id (str): The client's user ID
        document_type (str): The type of document uploaded
        case_id (str, optional): The associated case ID
        
    Returns:
        dict: The notification object
    """
    title = f"Document Uploaded: {document_type}"
    message = f"A client has uploaded a {document_type} document"
    
    data = {
        'document_type': document_type,
        'client_id': client_id,
        'case_id': case_id,
        'uploaded_at': datetime.utcnow().isoformat()
    }
    
    return send_notification(
        user_id=attorney_id,
        title=title,
        message=message,
        notification_type='info',
        category=CATEGORY_DOCUMENTS,
        data=data
    )

def send_appointment_reminder(user_id, appointment_type, date_time, location=None, zoom_link=None):
    """
    Send an appointment reminder notification.
    
    Args:
        user_id (str): The user ID to send the notification to
        appointment_type (str): The type of appointment
        date_time (str): The date and time of the appointment
        location (str, optional): Physical location of the appointment
        zoom_link (str, optional): Zoom link for virtual appointments
        
    Returns:
        dict: The notification object
    """
    title = f"Appointment Reminder: {appointment_type}"
    message = f"Your {appointment_type} appointment is scheduled for {date_time}"
    
    if location:
        message += f" at {location}"
    elif zoom_link:
        message += " (virtual appointment)"
    
    data = {
        'appointment_type': appointment_type,
        'date_time': date_time,
        'location': location,
        'zoom_link': zoom_link
    }
    
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type='info',
        category=CATEGORY_APPOINTMENT,
        data=data
    )

def send_message_notification(user_id, sender_name, message_preview, conversation_id):
    """
    Send a notification about a new message.
    
    Args:
        user_id (str): The user ID to send the notification to
        sender_name (str): The name of the message sender
        message_preview (str): A preview of the message content
        conversation_id (str): The conversation ID
        
    Returns:
        dict: The notification object
    """
    title = f"New Message from {sender_name}"
    
    # Truncate message preview if too long
    if len(message_preview) > 100:
        message_preview = message_preview[:97] + "..."
    
    message = message_preview
    
    data = {
        'sender_name': sender_name,
        'conversation_id': conversation_id,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type='info',
        category=CATEGORY_MESSAGES,
        data=data
    )

def send_immigration_form_notification(user_id, form_type, status, case_id=None):
    """
    Send a notification about an immigration form.
    
    Args:
        user_id (str): The user ID to send the notification to
        form_type (str): The type of immigration form
        status (str): The status of the form (e.g., 'submitted', 'approved', 'rejected')
        case_id (str, optional): The associated case ID
        
    Returns:
        dict: The notification object
    """
    title_map = {
        'submitted': f"Immigration Form {form_type} Submitted",
        'approved': f"Immigration Form {form_type} Approved",
        'rejected': f"Immigration Form {form_type} Rejected",
        'review': f"Immigration Form {form_type} Ready for Review",
        'incomplete': f"Immigration Form {form_type} Incomplete"
    }
    
    message_map = {
        'submitted': f"Your {form_type} form has been successfully submitted.",
        'approved': f"Your {form_type} form has been approved!",
        'rejected': f"Your {form_type} form has been rejected. Please check for details.",
        'review': f"Your {form_type} form is ready for review.",
        'incomplete': f"Your {form_type} form is incomplete. Additional information required."
    }
    
    notification_type_map = {
        'submitted': 'success',
        'approved': 'success',
        'rejected': 'error',
        'review': 'info',
        'incomplete': 'warning'
    }
    
    title = title_map.get(status, f"Immigration Form {form_type} Update")
    message = message_map.get(status, f"There is an update to your {form_type} form.")
    notification_type = notification_type_map.get(status, 'info')
    
    data = {
        'form_type': form_type,
        'status': status,
        'case_id': case_id,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        category=CATEGORY_IMMIGRATION,
        data=data
    ) 