from flask import Blueprint, jsonify, request, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.notification_service import get_notification_service, NotificationType, NotificationPriority
from utils.auth import require_auth
from flask_socketio import emit
from models.database import db
from models.user_notification_preferences import UserNotificationPreferences
from utils.rate_limit import check_rate_limit
from models.notification import Notification
import logging

logger = logging.getLogger(__name__)
notification_routes = Blueprint('notifications', __name__)

@notification_routes.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get notifications for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        limit = request.args.get('limit', default=50, type=int)
        include_read = request.args.get('include_read', default='true').lower() == 'true'
        
        # Get notifications from service (will use cache if available)
        service = get_notification_service()
        if not service:
            return jsonify({
                'success': False,
                'error': 'Notification service not initialized'
            }), 500
            
        notifications = service.get_user_notifications(
            user_id=user_id,
            limit=limit,
            include_read=include_read
        )
        
        return jsonify({
            'success': True,
            'notifications': notifications
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve notifications'
        }), 500

@notification_routes.route('/notifications/<notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        user_id = get_jwt_identity()
        
        # Check rate limit
        if not check_rate_limit(user_id, 'mark_notification_read', 100, 3600):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded'
            }), 429
        
        # Mark as read (will invalidate cache)
        service = get_notification_service()
        if not service:
            return jsonify({
                'success': False,
                'error': 'Notification service not initialized'
            }), 500
            
        success = service.mark_notification_read(user_id, notification_id)
        
        if success:
            return jsonify({'success': True}), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Notification not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to mark notification as read'
        }), 500

@notification_routes.route('/notifications/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read for the current user"""
    try:
        user_id = get_jwt_identity()
        
        # Check rate limit
        if not check_rate_limit(user_id, 'mark_all_notifications_read', 10, 3600):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded'
            }), 429
        
        # Mark all as read (will invalidate cache)
        service = get_notification_service()
        if not service:
            return jsonify({
                'success': False,
                'error': 'Notification service not initialized'
            }), 500
            
        success = service.mark_all_notifications_read(user_id)
        
        if success:
            return jsonify({'success': True}), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to mark notifications as read'
            }), 500
            
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to mark all notifications as read'
        }), 500

@notification_routes.route('/notifications/<notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        user_id = get_jwt_identity()
        
        # Check rate limit
        if not check_rate_limit(user_id, 'delete_notification', 100, 3600):
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded'
            }), 429
        
        # Delete notification (will invalidate cache)
        service = get_notification_service()
        if not service:
            return jsonify({
                'success': False,
                'error': 'Notification service not initialized'
            }), 500
            
        success = service.delete_notification(user_id, notification_id)
        
        if success:
            return jsonify({'success': True}), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Notification not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error deleting notification: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete notification'
        }), 500

@notification_routes.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    """Create a new notification"""
    try:
        data = request.get_json()
        
        # Get required fields
        user_id = data.get('user_id')
        title = data.get('title')
        message = data.get('message')
        notification_type = data.get('type')
        
        # Optional fields
        priority = data.get('priority', 'normal')
        metadata = data.get('metadata', {})
        
        if not all([user_id, title, message, notification_type]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
            
        service = get_notification_service()
        if not service:
            return jsonify({
                'success': False,
                'error': 'Notification service not initialized'
            }), 500
            
        notification = service.create_notification(
            user_id=user_id,
            notification_data={
                'title': title,
                'message': message,
                'type': notification_type,
                'priority': priority,
                'data': metadata
            }
        )
        
        if notification:
            return jsonify({
                'success': True,
                'notification': notification
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create notification'
            }), 500
            
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to create notification'
        }), 500

@notification_routes.route('/notifications/preferences', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    """Get notification preferences for the current user"""
    try:
        user_id = get_jwt_identity()
        
        preferences = UserNotificationPreferences.query.filter_by(user_id=user_id).first()
        if not preferences:
            # Create default preferences
            preferences = UserNotificationPreferences(
                user_id=user_id,
                email_enabled=True,
                app_enabled=True,
                browser_enabled=False,
                email_case_updates=True,
                email_document_updates=True,
                email_appointment_reminders=True,
                email_messages=True,
                email_legal_ai_responses=True,
                email_system_announcements=True,
                app_case_updates=True,
                app_document_updates=True,
                app_appointment_reminders=True,
                app_messages=True,
                app_legal_ai_responses=True,
                app_system_announcements=True,
                browser_case_updates=False,
                browser_document_updates=False,
                browser_appointment_reminders=False,
                browser_messages=False,
                browser_legal_ai_responses=False,
                browser_system_announcements=False
            )
            db.session.add(preferences)
            db.session.commit()
            
        return jsonify({
            'success': True,
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting notification preferences: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get notification preferences'
        }), 500

@notification_routes.route('/notifications/preferences', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    """Update notification preferences for the current user"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        preferences = UserNotificationPreferences.query.filter_by(user_id=user_id).first()
        if not preferences:
            preferences = UserNotificationPreferences(user_id=user_id)
            db.session.add(preferences)
        
        # Update email settings
        if 'email_enabled' in data:
            preferences.email_enabled = bool(data['email_enabled'])
        if 'email_case_updates' in data:
            preferences.email_case_updates = bool(data['email_case_updates'])
        if 'email_document_updates' in data:
            preferences.email_document_updates = bool(data['email_document_updates'])
        if 'email_appointment_reminders' in data:
            preferences.email_appointment_reminders = bool(data['email_appointment_reminders'])
        if 'email_messages' in data:
            preferences.email_messages = bool(data['email_messages'])
        if 'email_legal_ai_responses' in data:
            preferences.email_legal_ai_responses = bool(data['email_legal_ai_responses'])
        if 'email_system_announcements' in data:
            preferences.email_system_announcements = bool(data['email_system_announcements'])
            
        # Update in-app settings
        if 'app_enabled' in data:
            preferences.app_enabled = bool(data['app_enabled'])
        if 'app_case_updates' in data:
            preferences.app_case_updates = bool(data['app_case_updates'])
        if 'app_document_updates' in data:
            preferences.app_document_updates = bool(data['app_document_updates'])
        if 'app_appointment_reminders' in data:
            preferences.app_appointment_reminders = bool(data['app_appointment_reminders'])
        if 'app_messages' in data:
            preferences.app_messages = bool(data['app_messages'])
        if 'app_legal_ai_responses' in data:
            preferences.app_legal_ai_responses = bool(data['app_legal_ai_responses'])
        if 'app_system_announcements' in data:
            preferences.app_system_announcements = bool(data['app_system_announcements'])
            
        # Update browser settings
        if 'browser_enabled' in data:
            preferences.browser_enabled = bool(data['browser_enabled'])
            # If browser notifications are disabled, disable all browser notification types
            if not preferences.browser_enabled:
                preferences.browser_case_updates = False
                preferences.browser_document_updates = False
                preferences.browser_appointment_reminders = False
                preferences.browser_messages = False
                preferences.browser_legal_ai_responses = False
                preferences.browser_system_announcements = False
        
        if preferences.browser_enabled:
            if 'browser_case_updates' in data:
                preferences.browser_case_updates = bool(data['browser_case_updates'])
            if 'browser_document_updates' in data:
                preferences.browser_document_updates = bool(data['browser_document_updates'])
            if 'browser_appointment_reminders' in data:
                preferences.browser_appointment_reminders = bool(data['browser_appointment_reminders'])
            if 'browser_messages' in data:
                preferences.browser_messages = bool(data['browser_messages'])
            if 'browser_legal_ai_responses' in data:
                preferences.browser_legal_ai_responses = bool(data['browser_legal_ai_responses'])
            if 'browser_system_announcements' in data:
                preferences.browser_system_announcements = bool(data['browser_system_announcements'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating notification preferences: {e}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to update notification preferences'
        }), 500

@notification_routes.route('/api/notifications/browser-permission', methods=['POST'])
@require_auth
def update_browser_permission():
    """Update browser notification permission status"""
    try:
        user_id = g.user.get('user_id')
        data = request.json
        if not data or 'granted' not in data:
            return jsonify({"error": "Missing permission status"}), 400
            
        # If permission is denied, disable all browser notifications
        if not data['granted']:
            preferences = UserNotificationPreferences.get_by_user_id(user_id)
            preferences.browser_case_updates = False
            preferences.browser_document_updates = False
            preferences.browser_appointment_reminders = False
            preferences.browser_messages = False
            preferences.browser_legal_ai_responses = False
            preferences.browser_system_announcements = False
            db.session.commit()
            
        return jsonify({
            "message": "Browser permission status updated",
            "granted": data['granted']
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error updating browser permission: {str(e)}"}), 500

@notification_routes.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    """Get user notifications."""
    try:
        notifications = Notification.query.all()
        return jsonify([n.to_dict() for n in notifications])
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        return jsonify({'error': str(e)}), 500

@notification_routes.route('/api/notifications/<notification_id>/read', methods=['POST'])
@require_auth
def mark_as_read(notification_id):
    """Mark a notification as read."""
    try:
        notification = Notification.query.get(notification_id)
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
            
        notification.is_read = True
        db.session.commit()
        return jsonify(notification.to_dict())
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Alias for compatibility with routes/__init__.py
notification_bp = notification_routes 