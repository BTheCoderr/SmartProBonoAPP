"""
Notification Service for WebSockets.

This module provides functionality for sending, tracking, and managing
user notifications through WebSockets.
"""

import json
import uuid
import logging
import threading
from datetime import datetime
from flask import current_app
from flask_socketio import emit

# Import connection service
from backend.websocket.services.connection_service import (
    get_user_sessions,
    is_user_connected
)

# Configure logging
logger = logging.getLogger('websocket.services.notification')

# Thread-safe notification tracking
_notification_lock = threading.RLock()
_notifications = {}  # Store in-memory notifications (in production, use database)
_notification_stats = {
    'total_sent': 0,
    'total_delivered': 0,
    'total_read': 0,
    'total_errors': 0,
    'by_type': {},
    'by_category': {}
}

# Notification types
NOTIFICATION_TYPES = ['info', 'success', 'warning', 'error']

# Default notification expiry (in seconds)
DEFAULT_EXPIRY = 7 * 24 * 60 * 60  # 7 days

def send_notification(user_id, title, message, notification_type='info', 
                     category=None, data=None, persist=True):
    """
    Send a notification to a specific user.
    
    Args:
        user_id (str): The user ID to send the notification to
        title (str): Notification title
        message (str): Notification message
        notification_type (str, optional): Type of notification ('info', 'success', 'warning', 'error')
        category (str, optional): Category for grouping notifications
        data (dict, optional): Additional data to include with the notification
        persist (bool, optional): Whether to persist the notification

    Returns:
        dict: The notification object with delivery status
    """
    if not user_id:
        logger.error("Cannot send notification: missing user_id")
        return {'error': 'Missing user_id'}
    
    if notification_type not in NOTIFICATION_TYPES:
        logger.warning(f"Invalid notification type: {notification_type}, using 'info' instead")
        notification_type = 'info'
    
    # Create notification object
    notification = {
        'id': str(uuid.uuid4()),
        'title': title,
        'message': message,
        'type': notification_type,
        'category': category,
        'data': data or {},
        'createdAt': datetime.utcnow().isoformat(),
        'sentTo': user_id,
        'read': False,
        'delivered': False,
        'error': None
    }
    
    # Track notification stats
    with _notification_lock:
        _notification_stats['total_sent'] += 1
        _notification_stats['by_type'][notification_type] = _notification_stats['by_type'].get(notification_type, 0) + 1
        if category:
            _notification_stats['by_category'][category] = _notification_stats['by_category'].get(category, 0) + 1
    
    # Check if user is connected
    sessions = get_user_sessions(user_id)
    
    if sessions:
        try:
            # Send to all user's sessions using socketio from current_app if available
            socketio = None
            if hasattr(current_app, 'extensions') and 'socketio' in current_app.extensions:
                socketio = current_app.extensions['socketio']
            
            if socketio:
                # Get the socketio instance to use emit with namespace and room
                for sid in sessions:
                    socketio.emit('notification', notification, to=sid, namespace='/ws')
                    logger.debug(f"Notification sent via socketio to {sid}")
            else:
                # If we can't use socketio directly, use Flask-SocketIO's emit
                # This will only work if called from within a socket event handler
                from backend.websocket.core import socketio as core_socketio
                for sid in sessions:
                    core_socketio.emit('notification', notification, to=sid, namespace='/ws')
                    logger.debug(f"Notification sent via core_socketio to {sid}")
            
            notification['delivered'] = True
            with _notification_lock:
                _notification_stats['total_delivered'] += 1
            
            logger.info(f"Notification {notification['id']} sent to user {user_id}")
        except Exception as e:
            notification['error'] = str(e)
            notification['delivered'] = False
            with _notification_lock:
                _notification_stats['total_errors'] += 1
            
            logger.error(f"Error sending notification to user {user_id}: {str(e)}")
    else:
        notification['delivered'] = False
        logger.info(f"User {user_id} not connected, notification queued for delivery")
    
    # Persist notification if requested
    if persist:
        with _notification_lock:
            _notifications[notification['id']] = notification
    
    return notification

def send_broadcast_notification(title, message, notification_type='info', 
                               category=None, data=None, persist=True, 
                               exclude_users=None):
    """
    Send a notification to all connected users.
    
    Args:
        title (str): Notification title
        message (str): Notification message
        notification_type (str, optional): Type of notification
        category (str, optional): Category for grouping notifications
        data (dict, optional): Additional data to include
        persist (bool, optional): Whether to persist the notification
        exclude_users (list, optional): List of user IDs to exclude

    Returns:
        dict: Broadcast results with success count and errors
    """
    exclude_users = exclude_users or []
    
    # Get all connected sessions from connection service
    from backend.websocket.services.connection_service import get_connected_users
    
    connected_users = get_connected_users()
    broadcast_id = str(uuid.uuid4())
    
    results = {
        'broadcast_id': broadcast_id,
        'timestamp': datetime.utcnow().isoformat(),
        'total_users': len(connected_users),
        'excluded_users': len(exclude_users),
        'sent_count': 0,
        'error_count': 0,
        'errors': []
    }
    
    for user_data in connected_users:
        user_id = user_data['user_id']
        
        if user_id in exclude_users:
            continue
        
        try:
            # Reuse send_notification but with the same broadcast ID
            notification = send_notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                category=category,
                data={**(data or {}), 'broadcast_id': broadcast_id},
                persist=persist
            )
            
            if notification.get('error'):
                results['error_count'] += 1
                results['errors'].append({
                    'user_id': user_id,
                    'error': notification['error']
                })
            else:
                results['sent_count'] += 1
        except Exception as e:
            results['error_count'] += 1
            results['errors'].append({
                'user_id': user_id,
                'error': str(e)
            })
            logger.error(f"Error in broadcast to user {user_id}: {str(e)}")
    
    logger.info(f"Broadcast {broadcast_id} sent to {results['sent_count']} users with {results['error_count']} errors")
    return results

def mark_notification_read(notification_id, user_id=None):
    """
    Mark a notification as read.
    
    Args:
        notification_id (str): The notification ID to mark as read
        user_id (str, optional): The user ID to verify ownership

    Returns:
        bool: True if marked as read, False otherwise
    """
    with _notification_lock:
        if notification_id in _notifications:
            notification = _notifications[notification_id]
            
            # If user_id provided, check ownership
            if user_id and notification['sentTo'] != user_id:
                logger.warning(f"User {user_id} attempted to mark notification {notification_id} as read, but it belongs to {notification['sentTo']}")
                return False
            
            if not notification['read']:
                notification['read'] = True
                notification['readAt'] = datetime.utcnow().isoformat()
                _notification_stats['total_read'] += 1
                logger.debug(f"Notification {notification_id} marked as read")
            
            return True
        
        return False

def get_user_notifications(user_id, include_read=False, limit=50):
    """
    Get notifications for a user.
    
    Args:
        user_id (str): The user ID to get notifications for
        include_read (bool, optional): Whether to include read notifications
        limit (int, optional): Maximum number of notifications to return

    Returns:
        list: List of notification objects
    """
    if not user_id:
        return []
    
    with _notification_lock:
        user_notifications = [
            notification for notification in _notifications.values()
            if notification['sentTo'] == user_id and (include_read or not notification['read'])
        ]
    
    # Sort by creation date, newest first
    user_notifications.sort(
        key=lambda n: n.get('createdAt', ''), 
        reverse=True
    )
    
    return user_notifications[:limit]

def delete_notification(notification_id, user_id=None, admin=False):
    """
    Delete a notification.
    
    Args:
        notification_id (str): The notification ID to delete
        user_id (str, optional): The user ID to verify ownership
        admin (bool, optional): Whether this is an admin operation

    Returns:
        bool: True if deleted, False otherwise
    """
    with _notification_lock:
        if notification_id in _notifications:
            notification = _notifications[notification_id]
            
            # If not admin and user_id provided, check ownership
            if not admin and user_id and notification['sentTo'] != user_id:
                logger.warning(f"User {user_id} attempted to delete notification {notification_id}, but it belongs to {notification['sentTo']}")
                return False
            
            del _notifications[notification_id]
            logger.info(f"Notification {notification_id} deleted{' by admin' if admin else ''}")
            return True
        
        return False

def get_notification_stats():
    """
    Get notification statistics.
    
    Returns:
        dict: Notification statistics
    """
    with _notification_lock:
        # Create a copy to avoid thread issues
        return {
            **_notification_stats,
            'total_notifications': len(_notifications),
            'timestamp': datetime.utcnow().isoformat()
        }

def clear_all_notifications():
    """
    Clear all stored notifications (for testing).
    
    Returns:
        int: Number of notifications cleared
    """
    with _notification_lock:
        count = len(_notifications)
        _notifications.clear()
        
        # Reset stats
        for key in _notification_stats:
            if isinstance(_notification_stats[key], dict):
                _notification_stats[key] = {}
            else:
                _notification_stats[key] = 0
        
        logger.warning(f"Cleared all {count} notifications")
        return count 