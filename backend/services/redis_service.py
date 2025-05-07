from typing import Dict, List, Optional
import json
from datetime import datetime
from flask import current_app
import redis
import logging

logger = logging.getLogger(__name__)

def get_redis() -> redis.Redis:
    """Get Redis client instance."""
    try:
        if hasattr(current_app, 'redis'):
            return current_app.redis
        
        redis_url = current_app.config.get('REDIS_URL', 'redis://localhost:6379/0')
        client = redis.from_url(redis_url)
        current_app.redis = client
        return client
    except Exception as e:
        logger.error(f"Failed to get Redis client: {str(e)}")
        return None

class RedisService:
    def __init__(self):
        self._redis_client = None

    @property
    def redis(self) -> redis.Redis:
        if not self._redis_client:
            self._redis_client = get_redis()
        return self._redis_client

    async def store_notification(self, user_id: str, notification: Dict) -> str:
        """Store a notification in Redis."""
        notification_id = f"notification:{datetime.utcnow().timestamp()}"
        notification["id"] = notification_id
        notification["timestamp"] = datetime.utcnow().isoformat()
        notification["read"] = False

        try:
            # Store notification in user's notification list
            user_notifications_key = f"user:{user_id}:notifications"
            await self.redis.lpush(user_notifications_key, json.dumps(notification))
            
            # Keep only last 100 notifications
            await self.redis.ltrim(user_notifications_key, 0, 99)
            
            return notification_id
        except Exception as e:
            logger.error(f"Failed to store notification: {str(e)}")
            return None

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's notifications."""
        try:
            notifications = []
            user_notifications_key = f"user:{user_id}:notifications"
            
            # Get notifications from list
            notification_data = await self.redis.lrange(user_notifications_key, 0, limit - 1)
            
            for data in notification_data:
                notification = json.loads(data)
                notifications.append(notification)
                
            return notifications
        except Exception as e:
            logger.error(f"Failed to get user notifications: {str(e)}")
            return []

    async def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read."""
        try:
            user_notifications_key = f"user:{user_id}:notifications"
            
            # Get all notifications
            notifications = await self.redis.lrange(user_notifications_key, 0, -1)
            
            for idx, notification_data in enumerate(notifications):
                notification = json.loads(notification_data)
                if notification["id"] == notification_id:
                    notification["read"] = True
                    # Update the notification in the list
                    await self.redis.lset(
                        user_notifications_key,
                        idx,
                        json.dumps(notification)
                    )
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Failed to mark notification as read: {str(e)}")
            return False

    async def delete_notification(self, user_id: str, notification_id: str) -> bool:
        """Delete a notification."""
        try:
            user_notifications_key = f"user:{user_id}:notifications"
            
            # Get all notifications
            notifications = await self.redis.lrange(user_notifications_key, 0, -1)
            
            for notification_data in notifications:
                notification = json.loads(notification_data)
                if notification["id"] == notification_id:
                    # Remove the notification
                    await self.redis.lrem(
                        user_notifications_key,
                        1,
                        notification_data
                    )
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Failed to delete notification: {str(e)}")
            return False

    async def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications."""
        try:
            user_notifications_key = f"user:{user_id}:notifications"
            notifications = await self.redis.lrange(user_notifications_key, 0, -1)
            
            unread_count = 0
            for notification_data in notifications:
                notification = json.loads(notification_data)
                if not notification.get("read", False):
                    unread_count += 1
                    
            return unread_count
        except Exception as e:
            logger.error(f"Failed to get unread count: {str(e)}")
            return 0

# Create a singleton instance
redis_service = RedisService() 