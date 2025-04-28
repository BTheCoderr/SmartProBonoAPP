from flask import Blueprint, request, jsonify, current_app
from flask_socketio import emit
from datetime import datetime
from bson import ObjectId
from ..models.notification import Notification
from ..utils.auth import login_required, admin_required
from ..services.notification_service import NotificationService
from ..utils.validation import validate_notification

notifications = Blueprint('notifications', __name__)
notification_service = NotificationService()

@notifications.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Get notifications for the current user"""
    try:
        user_id = request.user_id
        notifications = notification_service.get_user_notifications(user_id)
        return jsonify(notifications), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching notifications: {str(e)}")
        return jsonify({"error": "Failed to fetch notifications"}), 500

@notifications.route('/notifications/mark-read', methods=['POST'])
@login_required
def mark_notification_read():
    """Mark a notification as read"""
    try:
        notification_id = request.json.get('notification_id')
        if not notification_id:
            return jsonify({"error": "Notification ID is required"}), 400
            
        notification_service.mark_notification_read(notification_id, request.user_id)
        return jsonify({"message": "Notification marked as read"}), 200
    except Exception as e:
        current_app.logger.error(f"Error marking notification as read: {str(e)}")
        return jsonify({"error": "Failed to mark notification as read"}), 500

@notifications.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all notifications as read for the current user"""
    try:
        notification_service.mark_all_read(request.user_id)
        return jsonify({"message": "All notifications marked as read"}), 200
    except Exception as e:
        current_app.logger.error(f"Error marking all notifications as read: {str(e)}")
        return jsonify({"error": "Failed to mark all notifications as read"}), 500

@notifications.route('/notifications', methods=['POST'])
@admin_required
def create_notification():
    """Create a new notification (admin only)"""
    try:
        data = request.json
        if not validate_notification(data):
            return jsonify({"error": "Invalid notification data"}), 400
            
        notification = notification_service.create_notification(data)
        return jsonify(notification), 201
    except Exception as e:
        current_app.logger.error(f"Error creating notification: {str(e)}")
        return jsonify({"error": "Failed to create notification"}), 500

@notifications.route('/notifications/broadcast', methods=['POST'])
@admin_required
def broadcast_notification():
    """Broadcast a notification to all users (admin only)"""
    try:
        data = request.json
        if not validate_notification(data):
            return jsonify({"error": "Invalid notification data"}), 400
            
        notification_service.broadcast_notification(data)
        return jsonify({"message": "Notification broadcasted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error broadcasting notification: {str(e)}")
        return jsonify({"error": "Failed to broadcast notification"}), 500

@notifications.route('/notifications/<notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        notification_service.delete_notification(notification_id, request.user_id)
        return jsonify({"message": "Notification deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting notification: {str(e)}")
        return jsonify({"error": "Failed to delete notification"}), 500

@notifications.route('/notifications/settings', methods=['GET'])
@login_required
def get_notification_settings():
    """Get notification settings for the current user"""
    try:
        settings = notification_service.get_notification_settings(request.user_id)
        return jsonify(settings), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching notification settings: {str(e)}")
        return jsonify({"error": "Failed to fetch notification settings"}), 500

@notifications.route('/notifications/settings', methods=['PUT'])
@login_required
def update_notification_settings():
    """Update notification settings for the current user"""
    try:
        settings = request.json
        updated_settings = notification_service.update_notification_settings(
            request.user_id, 
            settings
        )
        return jsonify(updated_settings), 200
    except Exception as e:
        current_app.logger.error(f"Error updating notification settings: {str(e)}")
        return jsonify({"error": "Failed to update notification settings"}), 500 