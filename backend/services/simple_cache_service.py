import logging
import json
import time
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class SimpleCacheService:
    """
    A simple cache service that can use Redis if available or fallback to in-memory caching.
    This is perfect for development environments where Redis might not be installed.
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize the cache service with optional Redis connection
        
        Args:
            redis_url: Redis connection URL or None for in-memory cache
        """
        self.redis_client = None
        self.in_memory_cache = {}  # key -> (value, expiry_timestamp)
        self.is_redis_available = False
        
        if redis_url:
            try:
                import redis
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()  # Test connection
                self.is_redis_available = True
                logger.info(f"Connected to Redis at {redis_url}")
            except (ImportError, Exception) as e:
                logger.warning(f"Failed to connect to Redis: {e}. Using in-memory cache instead.")
        else:
            logger.info("No Redis URL provided. Using in-memory cache.")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache
        
        Args:
            key: The cache key
            
        Returns:
            The cached value or None if not found
        """
        if self.is_redis_available:
            try:
                return self.redis_client.get(key)
            except Exception as e:
                logger.error(f"Error retrieving from Redis: {e}")
                return None
        else:
            # Use in-memory cache with expiry check
            if key in self.in_memory_cache:
                value, expiry = self.in_memory_cache[key]
                if expiry is None or time.time() < expiry:
                    return value
                else:
                    # Expired, remove from cache
                    del self.in_memory_cache[key]
            return None
    
    def set(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> bool:
        """
        Set a value in the cache
        
        Args:
            key: The cache key
            value: The value to store
            expire_seconds: Optional expiration time in seconds
            
        Returns:
            True if successful, False on error
        """
        if self.is_redis_available:
            try:
                if expire_seconds:
                    return bool(self.redis_client.setex(key, expire_seconds, value))
                else:
                    return bool(self.redis_client.set(key, value))
            except Exception as e:
                logger.error(f"Error storing in Redis: {e}")
                return False
        else:
            # Use in-memory cache
            try:
                expiry = time.time() + expire_seconds if expire_seconds else None
                self.in_memory_cache[key] = (value, expiry)
                return True
            except Exception as e:
                logger.error(f"Error storing in memory cache: {e}")
                return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache
        
        Args:
            key: The cache key
            
        Returns:
            True if successful, False on error
        """
        if self.is_redis_available:
            try:
                return bool(self.redis_client.delete(key))
            except Exception as e:
                logger.error(f"Error deleting from Redis: {e}")
                return False
        else:
            # Use in-memory cache
            try:
                if key in self.in_memory_cache:
                    del self.in_memory_cache[key]
                return True
            except Exception as e:
                logger.error(f"Error deleting from memory cache: {e}")
                return False
    
    def clear_pattern(self, pattern: str) -> bool:
        """
        Delete all keys matching a pattern
        
        Args:
            pattern: The pattern to match (e.g., "user:*:notifications")
            
        Returns:
            True if successful, False on error
        """
        if self.is_redis_available:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return bool(self.redis_client.delete(*keys))
                return True
            except Exception as e:
                logger.error(f"Error clearing pattern from Redis: {e}")
                return False
        else:
            # Use in-memory cache with simple pattern matching
            try:
                import fnmatch
                keys_to_delete = [k for k in self.in_memory_cache.keys() if fnmatch.fnmatch(k, pattern)]
                for k in keys_to_delete:
                    del self.in_memory_cache[k]
                return True
            except Exception as e:
                logger.error(f"Error clearing pattern from memory cache: {e}")
                return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        if self.is_redis_available:
            try:
                info = self.redis_client.info()
                return {
                    'type': 'redis',
                    'keys': self.redis_client.dbsize(),
                    'used_memory': info.get('used_memory_human', 'unknown'),
                    'uptime': info.get('uptime_in_seconds', 0)
                }
            except Exception as e:
                logger.error(f"Error getting Redis stats: {e}")
                return {'type': 'redis', 'error': str(e)}
        else:
            # In-memory cache stats
            return {
                'type': 'in-memory',
                'keys': len(self.in_memory_cache),
                'active_keys': sum(1 for _, expiry in self.in_memory_cache.values() 
                                  if expiry is None or time.time() < expiry)
            }

# Singleton instance
_cache_service = None

def get_cache_service(redis_url: Optional[str] = None) -> SimpleCacheService:
    """
    Get or create the cache service singleton
    
    Args:
        redis_url: Optional Redis URL for initialization
        
    Returns:
        The cache service instance
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = SimpleCacheService(redis_url)
    return _cache_service 