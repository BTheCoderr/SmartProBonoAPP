"""
Persistence utilities for WebSocket functionality
This is a simple in-memory implementation for the MVP.
In a production environment, this would be replaced with database storage.
"""
import logging
import uuid
import copy
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Set up logging
logger = logging.getLogger('websocket.persistence')

# In-memory storage for notifications
# Structure: {user_id: [notification1, notification2, ...]}
notifications_store: Dict[str, List[Dict[str, Any]]] = {}

def save_notification(user_id: str, notification_data: Dict[str, Any]) -> str:
    """
    Save a notification for a user
    
    Args:
        user_id: The ID of the user to save the notification for
        notification_data: The notification data to save
        
    Returns:
        str: The ID of the saved notification
    """
    if user_id not in notifications_store:
        notifications_store[user_id] = []
    
    # Make a copy of the notification data to avoid modifying the original
    notification = copy.deepcopy(notification_data)
    
    # Ensure the notification has an ID
    notification_id = notification.get('_id') or notification.get('id')
    if not notification_id:
        notification_id = str(uuid.uuid4())
        notification['_id'] = notification_id
    
    # Ensure the notification has a timestamp
    if 'timestamp' not in notification and 'createdAt' not in notification:
        notification['timestamp'] = datetime.now().isoformat()
    
    # Ensure read status is set
    if 'read' not in notification and 'isRead' not in notification:
        notification['read'] = False
    
    # Add the notification to the store
    notifications_store[user_id].append(notification)
    
    logger.info(f"Notification saved for user {user_id}: {notification_id}")
    return notification_id

def save_broadcast_notification(notification_data: Dict[str, Any]) -> str:
    """
    Save a broadcast notification for all users
    
    Args:
        notification_data: The notification data to save
        
    Returns:
        str: The ID of the saved notification
    """
    # Make a copy of the notification data to avoid modifying the original
    notification = copy.deepcopy(notification_data)
    
    # Ensure the notification has an ID
    notification_id = notification.get('_id') or notification.get('id')
    if not notification_id:
        notification_id = str(uuid.uuid4())
        notification['_id'] = notification_id
    
    # Ensure the notification has a timestamp
    if 'timestamp' not in notification and 'createdAt' not in notification:
        notification['timestamp'] = datetime.now().isoformat()
    
    # Ensure read status is set
    if 'read' not in notification and 'isRead' not in notification:
        notification['read'] = False
    
    # Add the notification to the broadcast store (store as special user 'broadcast')
    if 'broadcast' not in notifications_store:
        notifications_store['broadcast'] = []
    
    notifications_store['broadcast'].append(notification)
    
    logger.info(f"Broadcast notification saved: {notification_id}")
    return notification_id

def get_notifications_for_user(user_id: str, limit: int = 20, unread_only: bool = False) -> List[Dict[str, Any]]:
    """
    Get notifications for a user
    
    Args:
        user_id: The ID of the user to get notifications for
        limit: The maximum number of notifications to return
        unread_only: Whether to return only unread notifications
        
    Returns:
        List[Dict[str, Any]]: List of notification objects
    """
    # Get user-specific notifications
    user_notifications = notifications_store.get(user_id, [])
    
    # Get broadcast notifications
    broadcast_notifications = notifications_store.get('broadcast', [])
    
    # Combine user-specific and broadcast notifications
    all_notifications = user_notifications + broadcast_notifications
    
    # Filter by read status if needed
    if unread_only:
        all_notifications = [
            n for n in all_notifications if 
            (not n.get('read', False) and not n.get('isRead', False))
        ]
    
    # Sort by timestamp (newest first)
    sorted_notifications = sorted(
        all_notifications,
        key=lambda n: n.get('timestamp', n.get('createdAt', '')),
        reverse=True
    )
    
    # Apply limit
    limited_notifications = sorted_notifications[:limit]
    
    return limited_notifications

def mark_as_read(user_id: str, notification_ids: Union[str, List[str]]) -> bool:
    """
    Mark notifications as read for a user
    
    Args:
        user_id: The ID of the user to mark notifications for
        notification_ids: The ID(s) of the notification(s) to mark as read
        
    Returns:
        bool: Whether the operation was successful
    """
    if isinstance(notification_ids, str):
        notification_ids = [notification_ids]
    
    if not notification_ids:
        return False
    
    # Get user-specific notifications
    user_notifications = notifications_store.get(user_id, [])
    
    # Get broadcast notifications (we need to make a copy since these are shared)
    broadcast_notifications = copy.deepcopy(notifications_store.get('broadcast', []))
    
    success = False
    
    # Mark user-specific notifications as read
    for notification in user_notifications:
        notification_id = notification.get('_id') or notification.get('id')
        if notification_id in notification_ids:
            notification['read'] = True
            if 'isRead' in notification:
                notification['isRead'] = True
            success = True
    
    # Mark broadcast notifications as read (for this user only)
    for notification in broadcast_notifications:
        notification_id = notification.get('_id') or notification.get('id')
        if notification_id in notification_ids:
            # Create a copy of the broadcast notification for this user with read=True
            notification_copy = copy.deepcopy(notification)
            notification_copy['read'] = True
            if 'isRead' in notification_copy:
                notification_copy['isRead'] = True
            
            # Add to user's notifications
            if user_id not in notifications_store:
                notifications_store[user_id] = []
            
            notifications_store[user_id].append(notification_copy)
            success = True
    
    return success

def delete_notification(user_id: str, notification_id: str) -> bool:
    """
    Delete a notification for a user
    
    Args:
        user_id: The ID of the user to delete the notification for
        notification_id: The ID of the notification to delete
        
    Returns:
        bool: Whether the operation was successful
    """
    if user_id not in notifications_store:
        return False
    
    original_length = len(notifications_store[user_id])
    
    # Filter out the notification to delete
    notifications_store[user_id] = [
        n for n in notifications_store[user_id]
        if (n.get('_id') != notification_id and n.get('id') != notification_id)
    ]
    
    # Check if a notification was deleted
    return len(notifications_store[user_id]) < original_length

def clear_notifications(user_id: str) -> bool:
    """
    Clear all notifications for a user
    
    Args:
        user_id: The ID of the user to clear notifications for
        
    Returns:
        bool: Whether the operation was successful
    """
    if user_id in notifications_store:
        notifications_store[user_id] = []
        return True
    
    return False 