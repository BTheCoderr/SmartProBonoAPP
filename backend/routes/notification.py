"""
Notification Routes.

This module provides API routes for sending notifications through the WebSocket.
"""

import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from database.mongo import mongo

from backend.websocket.services.notification_service import (
    send_notification,
    get_user_notifications,
    mark_notification_read,
    delete_notification
)

# Configure logging
logger = logging.getLogger('routes.notification')

# Create blueprint
notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')

@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        current_user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page
        
        # Get unread count
        unread_count = mongo.get_collection('notifications').count_documents({
            'user_id': ObjectId(current_user_id),
            'read': False
        })
        
        # Get notifications with pagination
        notifications = list(mongo.get_collection('notifications')
                           .find({'user_id': ObjectId(current_user_id)})
                           .sort('created_at', -1)
                           .skip(skip)
                           .limit(per_page))
        
        # Convert ObjectId to string for JSON serialization
        for notif in notifications:
            notif['_id'] = str(notif['_id'])
            notif['user_id'] = str(notif['user_id'])
            if 'case_id' in notif:
                notif['case_id'] = str(notif['case_id'])
        
        # Get total count for pagination
        total_notifications = mongo.get_collection('notifications').count_documents({
            'user_id': ObjectId(current_user_id)
        })
        
        return jsonify({
            'notifications': notifications,
            'unread_count': unread_count,
            'total': total_notifications,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_notifications + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        logger.error(f"Get notifications error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@notification_bp.route('/<notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Update notification
        result = mongo.get_collection('notifications').update_one(
            {
                '_id': ObjectId(notification_id),
                'user_id': ObjectId(current_user_id)
            },
            {
                '$set': {
                    'read': True,
                    'read_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'Notification not found'}), 404
        
        return jsonify({'message': 'Notification marked as read'}), 200
        
    except Exception as e:
        logger.error(f"Mark notification as read error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@notification_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    try:
        current_user_id = get_jwt_identity()
        
        # Update all unread notifications
        result = mongo.get_collection('notifications').update_many(
            {
                'user_id': ObjectId(current_user_id),
                'read': False
            },
            {
                '$set': {
                    'read': True,
                    'read_at': datetime.utcnow()
                }
            }
        )
        
        return jsonify({
            'message': 'All notifications marked as read',
            'updated_count': result.modified_count
        }), 200
        
    except Exception as e:
        logger.error(f"Mark all notifications as read error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def create_notification(user_id, title, message, notification_type, case_id=None, data=None):
    """
    Helper function to create a notification
    
    Args:
        user_id (str): ID of the user to notify
        title (str): Notification title
        message (str): Notification message
        notification_type (str): Type of notification (e.g., 'case_update', 'document_upload')
        case_id (str, optional): Related case ID
        data (dict, optional): Additional data to store with the notification
    
    Returns:
        str: ID of the created notification
    """
    try:
        notification = {
            'user_id': ObjectId(user_id),
            'title': title,
            'message': message,
            'type': notification_type,
            'read': False,
            'created_at': datetime.utcnow(),
            'data': data or {}
        }
        
        if case_id:
            notification['case_id'] = ObjectId(case_id)
        
        result = mongo.get_collection('notifications').insert_one(notification)
        return str(result.inserted_id)
        
    except Exception as e:
        logger.error(f"Create notification error: {str(e)}")
        return None

@notification_bp.route('/send', methods=['POST'])
@jwt_required()
def send_notification_route():
    """
    Send a notification to a user.
    
    JSON body:
    {
        "user_id": "ID of user to receive notification",
        "title": "Notification title",
        "message": "Notification message",
        "type": "info|success|warning|error", (optional, default: info)
        "category": "Category for grouping", (optional)
        "data": {} (optional additional data)
    }
    
    Returns:
        JSON with status and notification details
    """
    sender_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    # Required fields
    user_id = data.get('user_id')
    title = data.get('title')
    message = data.get('message')
    
    if not user_id or not title or not message:
        return jsonify({
            'status': 'error',
            'message': 'user_id, title, and message are required'
        }), 400
    
    # Optional fields
    notification_type = data.get('type', 'info')
    category = data.get('category')
    additional_data = data.get('data', {})
    
    # Add sender info to data
    if isinstance(additional_data, dict):
        additional_data['sender_id'] = sender_id
    
    # Send notification
    notification = send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        category=category,
        data=additional_data
    )
    
    if notification.get('error'):
        return jsonify({
            'status': 'error',
            'message': notification['error']
        }), 400
    
    return jsonify({
        'status': 'success',
        'message': 'Notification sent',
        'notification': notification
    })

@notification_bp.route('/test', methods=['POST'])
@jwt_required()
def send_test_notification():
    """
    Send a test notification to the authenticated user.
    
    Returns:
        JSON with status and notification details
    """
    user_id = get_jwt_identity()
    
    notification = send_notification(
        user_id=user_id,
        title='Test Notification',
        message='This is a test notification from the API.',
        notification_type='info',
        category='test',
        data={
            'test': True,
            'timestamp': current_app.config.get('SERVER_START_TIME', 'unknown')
        }
    )
    
    if notification.get('error'):
        return jsonify({
            'status': 'error',
            'message': notification['error']
        }), 400
    
    return jsonify({
        'status': 'success',
        'message': 'Test notification sent',
        'notification': notification
    }) 