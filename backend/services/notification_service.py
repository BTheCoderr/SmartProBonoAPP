"""
Notification service for sending notifications to users
"""
from websocket_service import send_notification, send_broadcast_notification
from datetime import datetime
import uuid
import logging
from typing import List, Optional, Dict, Any
from bson import ObjectId
from flask import current_app
from backend.database.mongo import mongo
from backend.websocket.services.connection_service import get_connected_users
from backend.utils.logging_setup import get_logger
from flask_socketio import emit
from backend.models.notification import Notification
from backend.notifications.templates import get_notification_template
from backend.services.email_service import send_email

# Configure logger
logger = get_logger(__name__)

class NotificationService:
    """Unified service for handling all types of notifications."""
    
    def __init__(self):
        self.db = mongo.db
    
    def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = 'info',
        metadata: Optional[Dict[str, Any]] = None,
        category: Optional[str] = None
    ) -> ObjectId:
        """Create a new notification."""
        try:
            notification = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'type': notification_type,
                'metadata': metadata or {},
                'category': category,
                'is_read': False,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = self.db.notifications.insert_one(notification)
            
            # Emit real-time notification if user is connected
            self._emit_notification(user_id, notification)
            
            return result.inserted_id
        except Exception as e:
            logger.error(f"Failed to create notification: {str(e)}")
            raise
    
    def get_user_notifications(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        unread_only: bool = False,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get notifications for a user with filtering options."""
        try:
            query = {'user_id': user_id}
            
            if unread_only:
                query['is_read'] = False
            
            if category:
                query['category'] = category
            
            notifications = list(self.db.notifications.find(query)
                               .sort('created_at', -1)
                               .skip(offset)
                               .limit(limit))
            
            return notifications
        except Exception as e:
            logger.error(f"Failed to get notifications: {str(e)}")
            raise
    
    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read."""
        try:
            result = self.db.notifications.update_one(
                {'_id': ObjectId(notification_id), 'user_id': user_id},
                {'$set': {'is_read': True, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {str(e)}")
            raise
    
    def mark_all_as_read(self, user_id: str, category: Optional[str] = None) -> int:
        """Mark all notifications as read for a user."""
        try:
            query = {'user_id': user_id, 'is_read': False}
            if category:
                query['category'] = category
            
            result = self.db.notifications.update_many(
                query,
                {'$set': {'is_read': True, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Failed to mark all notifications as read: {str(e)}")
            raise
    
    def delete_notification(self, notification_id: str, user_id: str) -> bool:
        """Delete a notification."""
        try:
            result = self.db.notifications.delete_one({
                '_id': ObjectId(notification_id),
                'user_id': user_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete notification: {str(e)}")
            raise
    
    def clear_notifications(self, user_id: str, category: Optional[str] = None) -> int:
        """Clear all notifications for a user."""
        try:
            query = {'user_id': user_id}
            if category:
                query['category'] = category
            
            result = self.db.notifications.delete_many(query)
            return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to clear notifications: {str(e)}")
            raise
    
    def get_unread_count(self, user_id: str, category: Optional[str] = None) -> int:
        """Get count of unread notifications."""
        try:
            query = {'user_id': user_id, 'is_read': False}
            if category:
                query['category'] = category
            
            return self.db.notifications.count_documents(query)
        except Exception as e:
            logger.error(f"Failed to get unread count: {str(e)}")
            raise
    
    def _emit_notification(self, user_id: str, notification: Dict[str, Any]) -> None:
        """Emit notification to connected user sessions."""
        try:
            connected_users = get_connected_users()
            user_info = next((user for user in connected_users if user['user_id'] == user_id), None)
            
            if not user_info:
                return
                
            # Convert ObjectId to string for JSON serialization
            notification['_id'] = str(notification['_id'])
            
            # Send notification through WebSocket service
            send_notification(user_id, notification)
        except Exception as e:
            logger.error(f"Failed to emit notification: {str(e)}")

def send_user_notification(
    user_id: str,
    template_type: str,
    template_params: Dict[str, Any],
    send_email: bool = True,
    send_socket: bool = True
) -> Optional[str]:
    """
    Send a notification to a user using specified template and delivery methods.
    
    Args:
        user_id: ID of the user to send notification to
        template_type: Type of notification template to use
        template_params: Parameters to format the template with
        send_email: Whether to send an email notification
        send_socket: Whether to send a real-time socket notification
        
    Returns:
        ID of the created notification if successful, None otherwise
    """
    try:
        # Get user details
        user = mongo.db.users.find_one({'_id': user_id})
        if not user:
            current_app.logger.error(f"User not found for notification: {user_id}")
            return None
            
        # Get formatted notification content
        template_params['user_name'] = user.get('name', 'User')
        notification_content = get_notification_template(template_type, template_params)
        
        # Create notification record
        notification = {
            'user_id': user_id,
            'title': notification_content['title'],
            'message': notification_content['message'],
            'type': template_type,
            'read': False,
            'created_at': datetime.utcnow(),
            'metadata': template_params
        }
        
        result = mongo.db.notifications.insert_one(notification)
        notification_id = str(result.inserted_id)
        
        # Send email if enabled
        if send_email and user.get('email'):
            try:
                send_email(
                    recipient=user['email'],
                    subject=notification_content['email_subject'],
                    body=notification_content['email_body']
                )
            except Exception as e:
                current_app.logger.error(f"Failed to send email notification: {str(e)}")
        
        # Send socket notification if enabled
        if send_socket:
            try:
                emit('notification', {
                    'id': notification_id,
                    'title': notification_content['title'],
                    'message': notification_content['message'],
                    'type': template_type,
                    'created_at': notification['created_at'].isoformat()
                }, room=f"user_{user_id}")
            except Exception as e:
                current_app.logger.error(f"Failed to send socket notification: {str(e)}")
        
        return notification_id
        
    except Exception as e:
        current_app.logger.error(f"Error sending notification: {str(e)}")
        return None

# Create a singleton instance
notification_service = NotificationService()

# Export the service
def get_notification_service():
    """
    Get the notification service instance
    
    Returns:
        NotificationService: The notification service instance
    """
    return notification_service 