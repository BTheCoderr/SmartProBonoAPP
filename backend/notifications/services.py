from flask import current_app
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bson import ObjectId
from ..models.notification import Notification
from ..models.user import User
from ..config.api_keys import SMTP_CONFIG
from ..utils.logger import get_logger

logger = get_logger(__name__)

class NotificationService:
    def __init__(self):
        self.smtp_config = SMTP_CONFIG
        
    def send_notification(self, user_id, notification_type, data):
        """Send both in-app and email notifications"""
        try:
            # Create in-app notification
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                data=data,
                created_at=datetime.utcnow(),
                read=False
            ).save()
            
            # Send email notification if email template exists
            if hasattr(self, f'_get_{notification_type}_template'):
                template_func = getattr(self, f'_get_{notification_type}_template')
                subject, body = template_func(data)
                self._send_email(user_id, subject, body)
                
            return notification
            
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            raise
            
    def _send_email(self, user_id, subject, body):
        """Send email using SMTP"""
        try:
            # Get user email from database
            user = User.find_one({'_id': ObjectId(user_id)})
            if not user or not user.get('email'):
                logger.warning(f"No email found for user {user_id}")
                return
                
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['sender']
            msg['To'] = user['email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_config['host'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
                
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
            
    def _get_document_shared_template(self, data):
        """Template for document shared notification"""
        subject = f"Document Shared: {data['document_name']}"
        body = f"""
        <h2>Document Shared With You</h2>
        <p>A document has been shared with you on SmartProBono:</p>
        <ul>
            <li>Document: {data['document_name']}</li>
            <li>Shared by: {data['shared_by']}</li>
            <li>Access Level: {data['access_level']}</li>
        </ul>
        <p>Click <a href="/documents/{data['document_id']}">here</a> to view the document.</p>
        """
        return subject, body
        
    def mark_as_read(self, notification_id, user_id):
        """Mark a notification as read"""
        try:
            result = Notification.update_one(
                {
                    '_id': ObjectId(notification_id),
                    'user_id': user_id
                },
                {'$set': {'read': True}}
            )
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {str(e)}")
            raise
            
    def get_unread_notifications(self, user_id):
        """Get unread notifications for a user"""
        try:
            notifications = Notification.find({
                'user_id': user_id,
                'read': False
            }).sort('created_at', -1)
            
            return [{
                'id': str(notif['_id']),
                'type': notif['type'],
                'data': notif['data'],
                'created_at': notif['created_at']
            } for notif in notifications]
            
        except Exception as e:
            logger.error(f"Failed to get unread notifications: {str(e)}")
            raise

def send_user_notification(user_id, message, notification_type="info"):
    """
    Send a notification to a user
    
    Args:
        user_id: The ID of the user to notify
        message: The notification message
        notification_type: Type of notification (info, warning, error)
        
    Returns:
        bool: True if notification was sent successfully
    """
    try:
        # TODO: Implement actual notification sending logic
        # For now, just log the notification
        logger.info(f"Notification for user {user_id}: {message} (type: {notification_type})")
        return True
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        return False 