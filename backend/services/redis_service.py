from typing import Dict, List, Optional
import json
from datetime import datetime
from flask import current_app
import redis

class RedisService:
    def __init__(self):
        self._redis_client = None

    @property
    def redis(self) -> redis.Redis:
        if not self._redis_client:
            self._redis_client = current_app.redis
        return self._redis_client

    async def store_notification(self, user_id: str, notification: Dict) -> str:
        """Store a notification in Redis."""
        notification_id = f"notification:{datetime.utcnow().timestamp()}"
        notification["id"] = notification_id
        notification["timestamp"] = datetime.utcnow().isoformat()
        notification["read"] = False

        # Store notification in user's notification list
        user_notifications_key = f"user:{user_id}:notifications"
        await self.redis.lpush(user_notifications_key, json.dumps(notification))
        
        # Keep only last 100 notifications
        await self.redis.ltrim(user_notifications_key, 0, 99)
        
        return notification_id

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's notifications."""
        notifications = []
        user_notifications_key = f"user:{user_id}:notifications"
        
        # Get notifications from list
        notification_data = await self.redis.lrange(user_notifications_key, 0, limit - 1)
        
        for data in notification_data:
            notification = json.loads(data)
            notifications.append(notification)
            
        return notifications

    async def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read."""
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

    async def delete_notification(self, user_id: str, notification_id: str) -> bool:
        """Delete a notification."""
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

    async def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications."""
        user_notifications_key = f"user:{user_id}:notifications"
        notifications = await self.redis.lrange(user_notifications_key, 0, -1)
        
        unread_count = 0
        for notification_data in notifications:
            notification = json.loads(notification_data)
            if not notification.get("read", False):
                unread_count += 1
                
        return unread_count

# Create a singleton instance
redis_service = RedisService() 