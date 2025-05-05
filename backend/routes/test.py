from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from websocket import send_notification, get_connected_users, send_broadcast_notification
import random
import time
from datetime import datetime

test_bp = Blueprint('test', __name__, url_prefix='/api/test')

notification_types = ['info', 'success', 'warning', 'error']
notification_messages = [
    'Your document has been processed successfully',
    'New message received from your lawyer',
    'Reminder: Your appointment is scheduled for tomorrow',
    'Your case status has been updated',
    'Document upload failed. Please try again',
    'Payment received. Thank you!',
    'Your account has been verified',
    'Action required: Please complete your profile',
    'New resource is available for your case type',
    'Your immigration form has been submitted'
]

@test_bp.route('/notification/<user_id>', methods=['POST', 'GET'])
def send_notification_to_user(user_id):
    """
    Test endpoint to send a notification to a specific user
    
    Args:
        user_id (str): The user ID to send the notification to
    
    Returns:
        Response: JSON response indicating success or failure
    """
    try:
        # Use custom message if provided, otherwise use a random one
        data = request.json or {}
        message = data.get('message')
        if not message:
            message = random.choice(notification_messages)
        
        title = data.get('title', 'Test Notification')
        notification_type = data.get('type') or random.choice(notification_types)
        
        # Send notification using the new API
        notification = send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            category='test',
            data={'test': True}
        )
        
        return jsonify({
            'success': True,
            'message': f'Notification sent to user {user_id}',
            'notification': notification
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to send notification: {str(e)}'
        }), 500

@test_bp.route('/direct-message/<session_id>', methods=['POST'])
def test_direct_message(session_id):
    """
    Test endpoint to send a direct message to a specific client session
    
    Args:
        session_id (str): The session ID to send the message to
    
    Returns:
        Response: JSON response indicating success or failure
    """
    try:
        # Get message from request data
        data = request.json or {}
        message = data.get('message', 'Test direct message')
        title = data.get('title', 'Direct Message')
        notification_type = data.get('type', 'info')
        
        # Send direct message using new API
        notification = send_notification(
            user_id=session_id,  # Using session_id as user_id
            title=title,
            message=message,
            notification_type=notification_type,
            category='direct_message',
            data={'test': True, 'direct': True}
        )
        
        return jsonify({
            'success': True,
            'message': f'Direct message sent to session {session_id}',
            'notification': notification
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to send direct message: {str(e)}'
        }), 500

@test_bp.route('/connected-users', methods=['GET'])
def get_connected_users_route():
    """
    Test endpoint to get all connected users
    
    Returns:
        Response: JSON response with connected users
    """
    # Get connected users from the websocket module
    connected_users = get_connected_users()
    
    # Calculate total connections
    total_connections = 0
    for user_data in connected_users:
        if 'sessions' in user_data and isinstance(user_data['sessions'], list):
            total_connections += len(user_data['sessions'])
    
    return jsonify({
        'connected_users': connected_users,
        'total_users': len(connected_users),
        'total_connections': total_connections
    }), 200

@test_bp.route('/websocket-stats', methods=['GET'])
def websocket_stats():
    """Get statistics about WebSocket connections"""
    try:
        users = get_connected_users()
        connected_users_count = len(users)
        
        # Calculate total connections
        total_connections = 0
        for user_data in users:
            if 'sessions' in user_data and isinstance(user_data['sessions'], list):
                total_connections += len(user_data['sessions'])
        
        return jsonify({
            'status': 'success',
            'connected_users': connected_users_count,
            'total_connections': total_connections
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@test_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping test endpoint."""
    return jsonify({'status': 'success', 'message': 'pong'})

@test_bp.route('/notification', methods=['POST'])
def test_notification():
    """
    Test endpoint to send a notification to a user.
    
    JSON body:
    {
        "user_id": "The user ID to notify",
        "title": "Notification title",
        "message": "Notification message",
        "type": "info|success|warning|error" (optional)
    }
    """
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    user_id = data.get('user_id')
    title = data.get('title', 'Test Notification')
    message = data.get('message', 'This is a test notification')
    notification_type = data.get('type', 'info')
    
    if not user_id:
        return jsonify({
            'status': 'error',
            'message': 'user_id is required'
        }), 400
    
    notification = send_notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        category='test',
        data={'test': True}
    )
    
    return jsonify({
        'status': 'success',
        'message': f'Notification sent to user {user_id}',
        'notification': notification
    })

@test_bp.route('/broadcast', methods=['POST'])
def test_broadcast():
    """
    Test endpoint to broadcast a notification to all connected users.
    
    JSON body:
    {
        "title": "Notification title",
        "message": "Notification message",
        "type": "info|success|warning|error" (optional),
        "exclude_users": ["user_id1", "user_id2"] (optional)
    }
    """
    data = request.json
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        }), 400
    
    title = data.get('title', 'Broadcast Notification')
    message = data.get('message', 'This is a broadcast notification')
    notification_type = data.get('type', 'info')
    exclude_users = data.get('exclude_users', [])
    
    result = send_broadcast_notification(
        title=title,
        message=message,
        notification_type=notification_type,
        category='test',
        data={'test': True},
        exclude_users=exclude_users
    )
    
    return jsonify({
        'status': 'success',
        'message': f'Broadcast sent to {result["sent_count"]} users',
        'result': result
    })

@test_bp.route('/connections', methods=['GET'])
def test_connections():
    """Get all active WebSocket connections."""
    users = get_connected_users()
    
    return jsonify({
        'status': 'success',
        'connections': {
            'count': len(users),
            'users': users
        }
    })

@test_bp.route('/send-notification', methods=['POST'])
@jwt_required(optional=True)
def send_test_notification():
    """
    Test endpoint to send WebSocket notifications
    
    Required payload:
    {
        "message": "Your notification message",
        "type": "info|success|warning|error",  # Optional, defaults to info
        "userId": "optional-user-id"  # Optional, if not provided uses current user or broadcasts
    }
    """
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid request data'}), 400
            
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
            
        message = data.get('message')
        notification_type = data.get('type', 'info')
        
        # Get target user ID (optional)
        user_id = data.get('userId')
        
        # If no userId was specified, use the current authenticated user
        if not user_id:
            user_id = get_jwt_identity()
        
        # Send notification
        notification = send_notification(
            user_id=user_id,
            title='Notification',
            message=message,
            notification_type=notification_type,
            category='test',
            data=data.get('data', {})
        )
        
        if notification and not notification.get('error'):
            return jsonify({
                'status': 'success', 
                'message': 'Notification sent successfully',
                'to': user_id or 'broadcast'
            }), 200
        else:
            return jsonify({
                'status': 'warning',
                'message': 'Notification queued (user may not be connected)'
            }), 202
            
    except Exception as e:
        current_app.logger.error(f"Error sending test notification: {str(e)}")
        return jsonify({'error': f'Failed to send notification: {str(e)}'}), 500 