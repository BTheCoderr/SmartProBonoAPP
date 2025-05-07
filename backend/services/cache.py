"""Cache service for managing Redis caching"""
import json
from datetime import datetime, timedelta
import redis.asyncio as redis
from flask import current_app

class Cache:
    """Cache service class"""
    _redis_client = None

    @classmethod
    async def get_redis(cls):
        """Get Redis client instance"""
        if cls._redis_client is None:
            redis_url = current_app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            cls._redis_client = redis.from_url(redis_url, decode_responses=True)
        return cls._redis_client

    @classmethod
    async def set(cls, key, value, expire=None):
        """Set a key-value pair in Redis"""
        try:
            redis_client = await cls.get_redis()
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await redis_client.set(key, value, ex=expire)
            return True
        except Exception as e:
            current_app.logger.error(f"Redis set error: {str(e)}")
            return False

    @classmethod
    async def get(cls, key):
        """Get a value from Redis by key"""
        try:
            redis_client = await cls.get_redis()
            value = await redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            current_app.logger.error(f"Redis get error: {str(e)}")
            return None

    @classmethod
    async def delete(cls, key):
        """Delete a key from Redis"""
        try:
            redis_client = await cls.get_redis()
            await redis_client.delete(key)
            return True
        except Exception as e:
            current_app.logger.error(f"Redis delete error: {str(e)}")
            return False

    @classmethod
    async def exists(cls, key):
        """Check if a key exists in Redis"""
        try:
            redis_client = await cls.get_redis()
            return await redis_client.exists(key)
        except Exception as e:
            current_app.logger.error(f"Redis exists error: {str(e)}")
            return False

    @classmethod
    async def expire(cls, key, seconds):
        """Set expiration time for a key"""
        try:
            redis_client = await cls.get_redis()
            await redis_client.expire(key, seconds)
            return True
        except Exception as e:
            current_app.logger.error(f"Redis expire error: {str(e)}")
            return False

    @classmethod
    async def ttl(cls, key):
        """Get time to live for a key"""
        try:
            redis_client = await cls.get_redis()
            return await redis_client.ttl(key)
        except Exception as e:
            current_app.logger.error(f"Redis TTL error: {str(e)}")
            return -2

    @classmethod
    async def clear(cls):
        """Clear all keys in Redis"""
        try:
            redis_client = await cls.get_redis()
            await redis_client.flushdb()
            return True
        except Exception as e:
            current_app.logger.error(f"Redis clear error: {str(e)}")
            return False

# Create singleton instance
cache = Cache() 