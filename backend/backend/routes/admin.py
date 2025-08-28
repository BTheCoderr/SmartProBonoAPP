"""
Admin routes for user management in SmartProBono
"""
from flask import Blueprint, request, jsonify
from models.user import User
from extensions import mongo, db
from utils.decorators import token_required
from bson import ObjectId
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import or_, desc, Column, DateTime, cast, func
from sqlalchemy.sql.expression import cast
import json
import psutil
import os
from flask_jwt_extended import jwt_required, get_jwt_identity

# Mock websocket imports to allow the app to start
# These functions will be placeholder functions that don't actually use websockets
# This fixes the import error while allowing the app to start

# Notification types
NOTIFICATION_TYPE_INFO = 'info'
NOTIFICATION_TYPE_SUCCESS = 'success'
NOTIFICATION_TYPE_WARNING = 'warning'
NOTIFICATION_TYPE_ERROR = 'error'

# Categories
CATEGORY_IMMIGRATION = 'immigration'
CATEGORY_DOCUMENTS = 'documents'
CATEGORY_MESSAGES = 'messages'
CATEGORY_SYSTEM = 'system'
CATEGORY_CASE = 'case'
CATEGORY_APPOINTMENT = 'appointment'

# Mock functions
def send_broadcast_notification(title, message, notification_type, category='system', data=None, persist=True, exclude_users=None):
    """Mock function for sending broadcast notifications"""
    print(f"MOCK: Broadcasting notification: {title} - {message}")
    return True

def send_notification(user_id, title, message, notification_type, category='system', data=None):
    """Mock function for sending a notification to a specific user"""
    print(f"MOCK: Sending notification to {user_id}: {title} - {message}")
    return True

def get_connected_users():
    """Mock function for getting connected users"""
    return []

from utils.responses import success_response, error_response
from utils.logging_setup import get_logger
from utils.admin_required import admin_required
from utils.metrics import get_system_metrics, get_api_metrics, get_database_metrics
from typing import cast as type_cast

# Set up logging
logger = get_logger('routes.admin')

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    # Build query
    query = User.query
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        filters = []
        for attr in ['username', 'email', 'first_name', 'last_name']:
            column = getattr(User, attr)
            if hasattr(column, 'ilike'):
                filters.append(column.ilike(search_term))
        
        if filters:
            query = query.filter(or_(*filters))
    
    # Get paginated results using SQLAlchemy's desc() function
    pagination = query.order_by(desc(cast(User.created_at, DateTime))).paginate(page=page, per_page=per_page)
    users = pagination.items
    
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    }), 200

@bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
@admin_required
def get_user(current_user, user_id):
    """Get a specific user by ID (admin only)"""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'user': user.to_dict()
    }), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user, user_id):
    """Update a user (admin only)"""
    data = request.json
    user = User.query.get_or_404(user_id)
    
    if data is None:
        return jsonify({'message': 'No data provided'}), 400
        
    if 'active' in data and data['active'] is not None:
        user.active = bool(data['active'])
        
    if 'role' in data and data['role'] is not None:
        allowed_roles = ['client', 'lawyer', 'admin']
        if data['role'] not in allowed_roles:
            return jsonify({'message': f'Role must be one of {", ".join(allowed_roles)}'}), 400
        user.role = data['role']
    
    if 'email_verified' in data and data['email_verified'] is not None:
        user.email_verified = bool(data['email_verified'])
    
    # Update fields
    if 'first_name' in data and data['first_name'] is not None:
        user.first_name = data['first_name']
    
    if 'last_name' in data and data['last_name'] is not None:
        user.last_name = data['last_name']
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    """Delete a user (admin only)"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting own account
    if user.id == current_user.id:
        return jsonify({'message': 'Cannot delete your own account'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User deleted successfully'
    }), 200

@bp.route('/stats', methods=['GET'])
@token_required
@admin_required
def get_user_stats(current_user):
    """Get user statistics (admin only)"""
    total_users = User.query.count()
    active_users = User.query.filter_by(active=True).count()
    verified_users = User.query.filter_by(email_verified=True).count()
    
    # Users by role
    client_count = User.query.filter_by(role='client').count()
    lawyer_count = User.query.filter_by(role='lawyer').count()
    admin_count = User.query.filter_by(role='admin').count()
    
    # New users in the last 30 days using func.now()
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users = User.query.filter(
        User.created_at >= func.date(thirty_days_ago)
    ).count()
    
    # Recent logins in the last 7 days using func.now()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_logins = User.query.filter(
        User.last_login >= func.date(seven_days_ago)
    ).count()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'verified_users': verified_users,
        'new_users_last_30_days': new_users,
        'active_users_last_7_days': recent_logins,
        'users_by_role': {
            'client': client_count,
            'lawyer': lawyer_count,
            'admin': admin_count
        }
    }), 200

@bp.route('/notifications', methods=['GET'])
@jwt_required()
@admin_required
def get_all_notifications():
    """
    Get all notifications (admin only)
    
    Returns:
        List of all notifications
    """
    try:
        # In a real application, you would fetch notifications from a database
        # For now, we'll return demo data
        notifications = [
            {
                "_id": "1",
                "title": "System Maintenance",
                "message": "The system will be down for maintenance tonight from 2-4 AM EST.",
                "type": "info",
                "category": "system",
                "createdAt": datetime.utcnow().isoformat(),
                "sentTo": "all",
                "readCount": 12,
                "deliveryCount": 25,
                "errorCount": 0
            },
            {
                "_id": "2",
                "title": "Form Processing Delay",
                "message": "There is currently a delay in processing immigration forms due to high volume.",
                "type": "warning",
                "category": "immigration",
                "createdAt": (datetime.utcnow().timestamp() - 24*60*60) * 1000,
                "sentTo": "immigration-users",
                "readCount": 43,
                "deliveryCount": 120,
                "errorCount": 2
            },
            {
                "_id": "3",
                "title": "New Feature Available",
                "message": "Document scanning is now available in the mobile app.",
                "type": "success",
                "category": "system",
                "createdAt": (datetime.utcnow().timestamp() - 3*24*60*60) * 1000,
                "sentTo": "all",
                "readCount": 156,
                "deliveryCount": 450,
                "errorCount": 0
            }
        ]
        
        return success_response(
            message="Retrieved all notifications",
            data=notifications
        )
    except Exception as e:
        logger.error(f"Error retrieving notifications: {str(e)}")
        return error_response(message=f"Failed to retrieve notifications: {str(e)}")

@bp.route('/notifications/broadcast', methods=['POST'])
@jwt_required()
@admin_required
def broadcast_notification():
    """
    Broadcast a notification to all users (admin only)
    
    Returns:
        Success message
    """
    try:
        data = request.get_json()
        if not data:
            return error_response(message="No data provided")
        
        # Get message details
        message = data.get('message')
        title = data.get('title', 'System Notification')
        notification_type = data.get('type', NOTIFICATION_TYPE_INFO)
        
        if not message:
            return error_response(message="Message is required")
        
        # Validate notification type
        valid_types = [
            NOTIFICATION_TYPE_INFO, 
            NOTIFICATION_TYPE_SUCCESS, 
            NOTIFICATION_TYPE_WARNING, 
            NOTIFICATION_TYPE_ERROR
        ]
        
        if notification_type not in valid_types:
            return error_response(
                message=f"Invalid notification type. Must be one of: {', '.join(valid_types)}"
            )
        
        # Send broadcast
        result = send_broadcast_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            category='system',
            data=data.get('data', {}),
            persist=True,
            exclude_users=data.get('exclude_users', [])
        )
        
        if result:
            logger.info(f"Broadcast notification sent by admin {get_jwt_identity()}")
            return success_response(
                message="Broadcast notification sent successfully",
                data={"notification": data}
            )
        else:
            logger.error(f"Failed to send broadcast notification")
            return error_response(message="Failed to send broadcast notification")
            
    except Exception as e:
        logger.error(f"Error sending broadcast notification: {str(e)}")
        return error_response(message=f"Failed to send broadcast: {str(e)}")

@bp.route('/notifications/<notification_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_notification(notification_id):
    """
    Delete a notification (admin only)
    
    Args:
        notification_id: The ID of the notification to delete
        
    Returns:
        Success message
    """
    try:
        # In a real application, you would delete the notification from a database
        # For now, we'll just return success
        logger.info(f"Notification {notification_id} deleted by admin {get_jwt_identity()}")
        
        return success_response(
            message=f"Notification {notification_id} deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        return error_response(message=f"Failed to delete notification: {str(e)}")

@bp.route('/users/connected', methods=['GET'])
@jwt_required()
@admin_required
def get_connected_users_admin():
    """
    Get all connected users (admin only)
    
    Returns:
        List of connected users and their session IDs
    """
    try:
        connected_users = get_connected_users()
        
        # Calculate summary metrics
        total_users = len(connected_users)
        total_sessions = sum(user_data.get('session_count', 0) for user_data in connected_users)
        
        return success_response(
            message="Retrieved connected users",
            data={
                "connected_users": connected_users,
                "total_users": total_users,
                "total_sessions": total_sessions
            }
        )
    except Exception as e:
        logger.error(f"Error retrieving connected users: {str(e)}")
        return error_response(message=f"Failed to retrieve connected users: {str(e)}")

@bp.route('/notifications/user/<user_id>', methods=['POST'])
@jwt_required()
@admin_required
def send_user_notification_admin(user_id):
    """
    Send a notification to a specific user (admin only)
    
    Args:
        user_id: The user ID to send the notification to
        
    Returns:
        Success message
    """
    try:
        data = request.get_json()
        if not data:
            return error_response(message="No data provided")
        
        # Get message details
        message = data.get('message')
        title = data.get('title', 'Admin Notification')
        notification_type = data.get('type', NOTIFICATION_TYPE_INFO)
        
        if not message:
            return error_response(message="Message is required")
        
        # Create notification data
        notification_data = {
            'title': title,
            'message': message,
            'type': notification_type,
            'category': data.get('category', 'system'),
            'timestamp': datetime.utcnow().isoformat(),
            'data': data.get('data', {}),
            'admin_user': get_jwt_identity()
        }
        
        # Send notification
        result = send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            category=data.get('category', 'system'),
            data=data.get('data', {})
        )
        
        if result:
            logger.info(f"Admin notification sent to user {user_id} by admin {get_jwt_identity()}")
            return success_response(
                message=f"Notification sent to user {user_id} successfully",
                data={"notification": notification_data}
            )
        else:
            logger.error(f"Failed to send notification to user {user_id}")
            return error_response(message=f"Failed to send notification to user {user_id}")
            
    except Exception as e:
        logger.error(f"Error sending admin notification: {str(e)}")
        return error_response(message=f"Failed to send notification: {str(e)}")

@bp.route('/stats/notifications', methods=['GET'])
@jwt_required()
@admin_required
def get_notification_stats():
    """
    Get notification statistics (admin only)
    
    Returns:
        Notification statistics
    """
    try:
        # In a real application, you would fetch stats from a database
        # For now, we'll return demo data
        stats = {
            "total_sent": 1250,
            "total_read": 975,
            "total_errors": 15,
            "by_type": {
                "info": 725,
                "success": 320,
                "warning": 180,
                "error": 25
            },
            "by_category": {
                "system": 350,
                "immigration": 450,
                "documents": 275,
                "messages": 125,
                "appointments": 50
            },
            "recent_activity": {
                "last_24h": 120,
                "last_7d": 450,
                "last_30d": 950
            }
        }
        
        return success_response(
            message="Retrieved notification statistics",
            data=stats
        )
    except Exception as e:
        logger.error(f"Error retrieving notification stats: {str(e)}")
        return error_response(message=f"Failed to retrieve notification statistics: {str(e)}")

@bp.route('/settings', methods=['GET'])
@jwt_required()
@admin_required
def get_system_settings():
    """Get system settings (admin only)"""
    try:
        settings = {
            'maintenance_mode': False,  # Replace with actual setting from database
            'max_file_size_mb': 50,
            'allowed_file_types': ['pdf', 'doc', 'docx', 'jpg', 'png'],
            'notification_settings': {
                'email_notifications': True,
                'system_notifications': True
            },
            'security_settings': {
                'two_factor_required': False,
                'password_expiry_days': 90,
                'session_timeout_minutes': 30
            },
            'api_settings': {
                'rate_limit_per_minute': 100,
                'max_concurrent_requests': 50
            }
        }
        return jsonify(settings), 200
    except Exception as e:
        logger.error(f"Error fetching system settings: {str(e)}")
        return jsonify({'error': 'Failed to fetch system settings'}), 500

@bp.route('/settings', methods=['PUT'])
@jwt_required()
@admin_required
def update_system_settings():
    """Update system settings (admin only)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate settings
        if 'maintenance_mode' in data and not isinstance(data['maintenance_mode'], bool):
            return jsonify({'error': 'maintenance_mode must be a boolean'}), 400

        if 'max_file_size_mb' in data:
            try:
                max_size = int(data['max_file_size_mb'])
                if max_size <= 0 or max_size > 100:
                    return jsonify({'error': 'max_file_size_mb must be between 1 and 100'}), 400
            except ValueError:
                return jsonify({'error': 'max_file_size_mb must be a number'}), 400

        # TODO: Store settings in database
        return jsonify({'message': 'Settings updated successfully'}), 200
    except Exception as e:
        logger.error(f"Error updating system settings: {str(e)}")
        return jsonify({'error': 'Failed to update system settings'}), 500

@bp.route('/metrics', methods=['GET'])
@jwt_required()
@admin_required
def get_performance_metrics():
    """Get system performance metrics (admin only)"""
    try:
        time_range = request.args.get('range', '24h')
        valid_ranges = ['1h', '24h', '7d', '30d']
        
        if time_range not in valid_ranges:
            return jsonify({'error': f'Invalid time range. Must be one of: {", ".join(valid_ranges)}'}), 400

        # Get metrics from different sources
        system_metrics = get_system_metrics(time_range)
        api_metrics = get_api_metrics(time_range)
        db_metrics = get_database_metrics(time_range)

        metrics = {
            'api_response_times': api_metrics['response_times'],
            'error_rates': api_metrics['error_rates'],
            'active_users': api_metrics['active_users'],
            'memory_usage': system_metrics['memory_usage'],
            'cpu_usage': system_metrics['cpu_usage'],
            'database_queries': db_metrics['query_times']
        }

        return jsonify(metrics), 200
    except Exception as e:
        logger.error(f"Error fetching performance metrics: {str(e)}")
        return jsonify({'error': 'Failed to fetch performance metrics'}), 500 