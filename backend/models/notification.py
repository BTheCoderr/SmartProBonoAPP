from datetime import datetime
from models.database import db

class Notification(db.Model):
    """Model for storing user notifications in the database"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID string
    user_id = db.Column(db.String(36), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, success, warning, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    action_url = db.Column(db.String(500), nullable=True)
    related_entity_id = db.Column(db.String(36), nullable=True)
    related_entity_type = db.Column(db.String(50), nullable=True)
    sender = db.Column(db.String(36), nullable=True)  # User ID of sender, if applicable
    data = db.Column(db.Text, nullable=True)  # JSON string of additional data
    
    def __init__(self, id, user_id, title, message, **kwargs):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message
        
        # Set optional fields from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        """Convert notification to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'isRead': self.is_read,
            'timestamp': self.created_at.isoformat(),
            'actionUrl': self.action_url,
            'relatedEntityId': self.related_entity_id,
            'relatedEntityType': self.related_entity_type,
            'sender': self.sender,
            'data': self.data
        }
    
    @classmethod
    def get_user_notifications(cls, user_id, limit=50, include_read=True):
        """Get notifications for a user"""
        query = cls.query.filter_by(user_id=user_id)
        
        if not include_read:
            query = query.filter_by(is_read=False)
            
        return query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def mark_as_read(cls, notification_id, user_id):
        """Mark a notification as read"""
        notification = cls.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False
    
    @classmethod
    def mark_all_as_read(cls, user_id):
        """Mark all notifications as read for a user"""
        result = cls.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return result
    
    @classmethod
    def delete_notification(cls, notification_id, user_id):
        """Delete a notification"""
        notification = cls.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def delete_all_notifications(cls, user_id):
        """Delete all notifications for a user"""
        count = cls.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return count 