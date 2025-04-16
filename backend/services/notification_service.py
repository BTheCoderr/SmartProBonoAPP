import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import logging
import uuid
from flask_socketio import emit
from flask import current_app

from models.database import db
from models.notification import Notification
from utils.notification_utils import should_send_notification, ENTITY_TYPE_SYSTEM
from services.cache_service import get_cache_service

logger = logging.getLogger(__name__)

class NotificationPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationType:
    CASE_UPDATE = "case_update"
    EMERGENCY = "emergency"
    AVAILABILITY = "availability"
    SYSTEM = "system"

class NotificationService:
    def __init__(self, socketio=None):
        """
        Initialize the notification service
        
        Args:
            socketio: The Socket.IO instance to use for real-time notifications
        """
        self.socketio = socketio
        self.logger = logging.getLogger(__name__)
        self.cache = get_cache_service()
        
    def _get_notification_cache_key(self, user_id: str) -> str:
        """Get cache key for user's notifications"""
        return f"notifications:{user_id}"
        
    def _cache_notification(self, notification: Dict) -> bool:
        """Cache a notification"""
        try:
            user_id = notification['user_id']
            cache_key = self._get_notification_cache_key(user_id)
            
            # Get existing cached notifications
            cached = self.cache.get(cache_key) or []
            
            # Add new notification to front of list
            cached.insert(0, notification)
            
            # Keep only last 50 notifications in cache
            cached = cached[:50]
            
            # Update cache with 1 hour expiration
            return self.cache.set(cache_key, cached, expire_seconds=3600)
        except Exception as e:
            self.logger.error(f"Error caching notification: {e}")
            return False
            
    def _invalidate_notification_cache(self, user_id: str) -> bool:
        """Invalidate cached notifications for a user"""
        try:
            cache_key = self._get_notification_cache_key(user_id)
            return self.cache.delete(cache_key)
        except Exception as e:
            self.logger.error(f"Error invalidating notification cache: {e}")
            return False
        
    def create_notification(self, user_id, notification_data):
        """
        Create a new notification for a user
        
        Args:
            user_id (str): The ID of the user to notify
            notification_data (dict): The notification data (title, message, type, etc.)
            
        Returns:
            dict: The created notification object with ID and timestamp
        """
        # Check if we should send this notification based on user preferences
        if not should_send_notification(
            user_id, 
            notification_data.get('type'), 
            notification_data.get('relatedEntityType')
        ):
            return None
            
        # Generate notification ID and timestamp
        notification_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Create notification object
        notification = Notification(
            id=notification_id,
            user_id=user_id,
            title=notification_data.get('title', ''),
            message=notification_data.get('message', ''),
            type=notification_data.get('type', 'info'),
            action_url=notification_data.get('actionUrl'),
            related_entity_id=notification_data.get('relatedEntityId'),
            related_entity_type=notification_data.get('relatedEntityType'),
            sender=notification_data.get('sender'),
            data=json.dumps(notification_data.get('data', {}))
        )
        
        try:
            # Save to database
            db.session.add(notification)
            db.session.commit()
            
            # Convert to dict for caching and response
            notification_dict = notification.to_dict()
            
            # Cache the notification
            self._cache_notification(notification_dict)
            
            return notification_dict
        except Exception as e:
            self.logger.error(f"Error creating notification: {e}")
            db.session.rollback()
            return None
    
    def send_notification(self, user_id, notification_data, online_users=None):
        """
        Create and send a notification to a user
        
        Args:
            user_id (str): The ID of the user to notify
            notification_data (dict): The notification data
            online_users (dict, optional): Map of session_id to user data for finding online users
            
        Returns:
            dict: The created notification or None if not sent
        """
        # First check if user wants in-app notifications for this type
        if not should_send_notification(
            user_id, 
            notification_data.get('type'), 
            notification_data.get('relatedEntityType'),
            channel="app"
        ):
            return None
        
        # Create the notification in database and cache
        notification = self.create_notification(user_id, notification_data)
        
        if not notification:
            return None
        
        # Try to send via WebSocket if user is online
        if self.socketio and online_users:
            # Find the user's session ID
            target_sid = None
            for sid, user_data in online_users.items():
                if user_data.get('user_id') == user_id:
                    target_sid = sid
                    break
            
            # Send notification if user is online
            if target_sid:
                self.logger.info(f"Sending real-time notification to user {user_id}")
                try:
                    self.socketio.emit('new_notification', notification, to=target_sid)
                except Exception as e:
                    self.logger.error(f"Error sending WebSocket notification: {e}")
        
        # If browser notifications are enabled for this type, send event to trigger browser notification
        if should_send_notification(
            user_id, 
            notification_data.get('type'), 
            notification_data.get('relatedEntityType'),
            channel="browser"
        ):
            # If user is online and socketio is available, send an event to trigger a browser notification
            if target_sid and self.socketio:
                try:
                    self.socketio.emit('browser_notification', notification, to=target_sid)
                except Exception as e:
                    self.logger.error(f"Error sending browser notification event: {e}")
        
        return notification
    
    def send_bulk_notification(self, user_ids, notification_template, online_users=None):
        """
        Send the same notification to multiple users
        
        Args:
            user_ids (list): List of user IDs to notify
            notification_template (dict): The notification template
            online_users (dict, optional): Map of session_id to user data for finding online users
            
        Returns:
            int: Number of notifications sent
        """
        sent_count = 0
        
        for user_id in user_ids:
            notification = self.send_notification(user_id, notification_template, online_users)
            if notification:
                sent_count += 1
                
        return sent_count
    
    def get_user_notifications(self, user_id: str, limit: int = 50, include_read: bool = True) -> List[Dict]:
        """
        Get notifications for a user
        
        Args:
            user_id (str): The user ID
            limit (int): Maximum number of notifications to return
            include_read (bool): Whether to include read notifications
            
        Returns:
            list: List of notification dictionaries
        """
        # Try to get from cache first
        if include_read:
            cache_key = self._get_notification_cache_key(user_id)
            cached = self.cache.get(cache_key)
            if cached:
                return cached[:limit]
        
        # Query from database
        query = Notification.query.filter_by(user_id=user_id)
        if not include_read:
            query = query.filter_by(is_read=False)
            
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        
        # Convert to list of dicts
        notification_list = [n.to_dict() for n in notifications]
        
        # Cache if we're getting all notifications
        if include_read:
            self.cache.set(
                self._get_notification_cache_key(user_id),
                notification_list,
                expire_seconds=3600
            )
        
        return notification_list
    
    def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user_id
            ).first()
            
            if notification:
                notification.is_read = True
                db.session.commit()
                
                # Invalidate cache
                self._invalidate_notification_cache(user_id)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error marking notification as read: {e}")
            db.session.rollback()
            return False
    
    def mark_all_notifications_read(self, user_id: str) -> bool:
        """Mark all notifications as read for a user"""
        try:
            Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).update({'is_read': True})
            
            db.session.commit()
            
            # Invalidate cache
            self._invalidate_notification_cache(user_id)
            return True
        except Exception as e:
            self.logger.error(f"Error marking all notifications as read: {e}")
            db.session.rollback()
            return False
    
    def delete_notification(self, user_id: str, notification_id: str) -> bool:
        """Delete a notification"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user_id
            ).first()
            
            if notification:
                db.session.delete(notification)
                db.session.commit()
                
                # Invalidate cache
                self._invalidate_notification_cache(user_id)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting notification: {e}")
            db.session.rollback()
            return False
    
    def delete_all_notifications(self, user_id):
        """
        Delete all notifications for a user
        
        Args:
            user_id (str): The user ID
            
        Returns:
            int: Number of notifications deleted
        """
        try:
            return Notification.delete_all_notifications(user_id)
        except Exception as e:
            self.logger.error(f"Error deleting all notifications: {str(e)}")
            return 0

# Singleton instance
_notification_service = None

def init_notification_service(socketio=None):
    """Initialize or get the notification service instance"""
    global _notification_service
    if not _notification_service:
        _notification_service = NotificationService(socketio)
    return _notification_service

def get_notification_service():
    """Get the notification service instance"""
    return _notification_service 