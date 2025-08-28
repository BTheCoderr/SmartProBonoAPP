from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.error_handlers import handle_exceptions
from ..database.models import User, NotificationSettings
from ..database.db import db
from ..utils.logging_setup import get_logger

logger = get_logger('users')

# Create blueprint
users = Blueprint('users', __name__)

@users.route('/notification-settings', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_notification_settings():
    """
    Get the notification settings for the current user
    
    Returns:
        Notification settings object
    """
    user_id = get_jwt_identity()
    
    # Get user notification settings from the database
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    # If no settings found, create default settings
    if not settings:
        settings = NotificationSettings(
            user_id=user_id,
            email_notifications=True,
            push_notifications=True,
            case_updates=True,
            form_submissions=True,
            document_requests=True,
            appointments=True,
            messages=True
        )
        db.session.add(settings)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'settings': {
            'emailNotifications': settings.email_notifications,
            'pushNotifications': settings.push_notifications,
            'caseUpdates': settings.case_updates,
            'formSubmissions': settings.form_submissions,
            'documentRequests': settings.document_requests,
            'appointments': settings.appointments,
            'messages': settings.messages
        }
    })

@users.route('/notification-settings', methods=['PUT'])
@jwt_required()
@handle_exceptions
def update_notification_settings():
    """
    Update notification settings for the current user
    
    Request body:
        emailNotifications: Enable/disable email notifications (optional)
        pushNotifications: Enable/disable push notifications (optional)
        caseUpdates: Enable/disable case update notifications (optional)
        formSubmissions: Enable/disable form submission notifications (optional)
        documentRequests: Enable/disable document request notifications (optional)
        appointments: Enable/disable appointment notifications (optional)
        messages: Enable/disable message notifications (optional)
        
    Returns:
        Updated notification settings
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Map frontend keys to database columns
    field_mapping = {
        'emailNotifications': 'email_notifications',
        'pushNotifications': 'push_notifications',
        'caseUpdates': 'case_updates',
        'formSubmissions': 'form_submissions',
        'documentRequests': 'document_requests',
        'appointments': 'appointments',
        'messages': 'messages'
    }
    
    # Get user notification settings from the database
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    # If no settings found, create default settings
    if not settings:
        settings = NotificationSettings(user_id=user_id)
        db.session.add(settings)
    
    # Update settings based on request data
    for frontend_key, db_column in field_mapping.items():
        if frontend_key in data:
            setattr(settings, db_column, bool(data[frontend_key]))
    
    # Save changes
    db.session.commit()
    
    # Return updated settings
    return jsonify({
        'success': True,
        'message': 'Notification settings updated',
        'settings': {
            'emailNotifications': settings.email_notifications,
            'pushNotifications': settings.push_notifications,
            'caseUpdates': settings.case_updates,
            'formSubmissions': settings.form_submissions,
            'documentRequests': settings.document_requests,
            'appointments': settings.appointments,
            'messages': settings.messages
        }
    })

@users.route('/notification-settings/reset', methods=['POST'])
@jwt_required()
@handle_exceptions
def reset_notification_settings():
    """
    Reset notification settings to default values for the current user
    
    Returns:
        Default notification settings
    """
    user_id = get_jwt_identity()
    
    # Get user notification settings from the database
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    # If no settings found, create default settings
    if not settings:
        settings = NotificationSettings(user_id=user_id)
        db.session.add(settings)
    
    # Reset to default values
    settings.email_notifications = True
    settings.push_notifications = True
    settings.case_updates = True
    settings.form_submissions = True
    settings.document_requests = True
    settings.appointments = True
    settings.messages = True
    
    # Save changes
    db.session.commit()
    
    # Return updated settings
    return jsonify({
        'success': True,
        'message': 'Notification settings reset to defaults',
        'settings': {
            'emailNotifications': settings.email_notifications,
            'pushNotifications': settings.push_notifications,
            'caseUpdates': settings.case_updates,
            'formSubmissions': settings.form_submissions,
            'documentRequests': settings.document_requests,
            'appointments': settings.appointments,
            'messages': settings.messages
        }
    }) 