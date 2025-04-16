from datetime import datetime
import uuid
import json
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base

# Will be replaced with the actual db instance
Base = declarative_base()

class CachedNotification(Base):
    """Model for user notifications with Redis caching capabilities"""
    __tablename__ = 'notifications'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(20), default='info')  # info, success, warning, error
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    action_url = Column(String(500), nullable=True)
    related_entity_id = Column(String(36), nullable=True)
    related_entity_type = Column(String(50), nullable=True)
    priority = Column(String(20), default='normal')  # low, normal, high, urgent
    
    def __init__(self, user_id, title, message, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.user_id = user_id
        self.title = title
        self.message = message
        self.type = kwargs.get('type', 'info')
        self.is_read = kwargs.get('is_read', False)
        self.action_url = kwargs.get('action_url')
        self.related_entity_id = kwargs.get('related_entity_id')
        self.related_entity_type = kwargs.get('related_entity_type')
        self.priority = kwargs.get('priority', 'normal')
        
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'action_url': self.action_url,
            'related_entity_id': self.related_entity_id,
            'related_entity_type': self.related_entity_type,
            'priority': self.priority
        }
    
    @property
    def cache_key(self):
        """Get the cache key for this notification"""
        return f"notification:{self.id}"
    
    @property
    def user_cache_key(self):
        """Get the cache key for user's notifications list"""
        return f"user:{self.user_id}:notifications"
    
    def save_to_cache(self, cache_service):
        """Save notification to cache"""
        if not cache_service:
            return False
            
        try:
            # Store the individual notification
            cache_service.set(
                self.cache_key,
                json.dumps(self.to_dict()),
                expire_seconds=3600  # 1 hour cache
            )
            
            # Add to user's notification list
            user_notifications = cache_service.get(self.user_cache_key)
            if user_notifications:
                user_notifications = json.loads(user_notifications)
                # Update if exists, otherwise append
                updated = False
                for i, notif in enumerate(user_notifications):
                    if notif.get('id') == self.id:
                        user_notifications[i] = self.to_dict()
                        updated = True
                        break
                        
                if not updated:
                    user_notifications.append(self.to_dict())
            else:
                user_notifications = [self.to_dict()]
                
            # Save the updated list
            cache_service.set(
                self.user_cache_key,
                json.dumps(user_notifications),
                expire_seconds=3600  # 1 hour cache
            )
            
            return True
        except Exception as e:
            print(f"Error saving notification to cache: {e}")
            return False
    
    def invalidate_cache(self, cache_service):
        """Remove notification from cache"""
        if not cache_service:
            return False
            
        try:
            # Delete individual notification
            cache_service.delete(self.cache_key)
            
            # Remove from user's notification list
            user_notifications = cache_service.get(self.user_cache_key)
            if user_notifications:
                user_notifications = json.loads(user_notifications)
                user_notifications = [n for n in user_notifications if n.get('id') != self.id]
                
                # Save the updated list
                cache_service.set(
                    self.user_cache_key,
                    json.dumps(user_notifications),
                    expire_seconds=3600  # 1 hour cache
                )
                
            return True
        except Exception as e:
            print(f"Error invalidating notification cache: {e}")
            return False
    
    @staticmethod
    def get_from_cache(cache_service, notification_id):
        """Get a notification from cache by ID"""
        if not cache_service:
            return None
            
        cache_key = f"notification:{notification_id}"
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            try:
                return json.loads(cached_data)
            except Exception as e:
                print(f"Error deserializing cached notification: {e}")
                
        return None
    
    @staticmethod
    def get_user_notifications_from_cache(cache_service, user_id):
        """Get all user's notifications from cache"""
        if not cache_service:
            return None
            
        cache_key = f"user:{user_id}:notifications"
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            try:
                return json.loads(cached_data)
            except Exception as e:
                print(f"Error deserializing cached user notifications: {e}")
                
        return None
    
    @staticmethod
    def invalidate_user_notifications_cache(cache_service, user_id):
        """Remove all user's notifications from cache"""
        if not cache_service:
            return False
            
        try:
            cache_key = f"user:{user_id}:notifications"
            cache_service.delete(cache_key)
            return True
        except Exception as e:
            print(f"Error invalidating user notifications cache: {e}")
            return False 