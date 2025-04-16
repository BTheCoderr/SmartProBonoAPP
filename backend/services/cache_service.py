import redis
import json
from datetime import timedelta
import logging
from flask import current_app

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self, redis_url=None):
        """Initialize Redis connection"""
        try:
            # If redis_url is provided, use it directly
            if redis_url:
                self.redis = redis.from_url(redis_url, decode_responses=True)
            else:
                # Try to get from app config, but handle the case when outside app context
                try:
                    self.redis = redis.from_url(
                        current_app.config['REDIS_URL'],
                        decode_responses=True
                    )
                except RuntimeError as e:
                    # Handle the "Working outside of application context" error
                    logger.warning(f"Redis initialization outside app context. Will use upon first request: {e}")
                    self.redis = None
                    return
            
            logger.info("Redis cache service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            self.redis = None

    def get(self, key):
        """Get value from cache"""
        try:
            if not self.redis:
                return None
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None

    def set(self, key, value, expire_seconds=3600):
        """Set value in cache with expiration"""
        try:
            if not self.redis:
                return False
            json_value = json.dumps(value)
            return self.redis.setex(key, expire_seconds, json_value)
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False

    def delete(self, key):
        """Delete value from cache"""
        try:
            if not self.redis:
                return False
            return self.redis.delete(key) > 0
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False

    def clear_pattern(self, pattern):
        """Clear all keys matching pattern"""
        try:
            if not self.redis:
                return False
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys) > 0
            return True
        except Exception as e:
            logger.error(f"Error clearing cache pattern: {e}")
            return False

# Create singleton instance
_cache_service = None

def get_cache_service():
    """Get or create cache service instance"""
    global _cache_service
    if not _cache_service:
        try:
            _cache_service = CacheService()
            # Test if Redis is actually available
            if _cache_service.redis is None:
                # Fall back to SimpleCacheService
                from .simple_cache_service import SimpleCacheService
                logger.info("Falling back to SimpleCacheService")
                _cache_service = SimpleCacheService()
        except Exception as e:
            logger.error(f"Error initializing CacheService: {e}")
            # Fall back to SimpleCacheService
            from .simple_cache_service import SimpleCacheService
            logger.info("Falling back to SimpleCacheService due to error")
            _cache_service = SimpleCacheService()
    return _cache_service 