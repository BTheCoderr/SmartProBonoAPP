from services.cache_service import get_cache_service
import time
import logging

logger = logging.getLogger(__name__)

def check_rate_limit(user_id: str, action: str, max_requests: int, window_seconds: int) -> bool:
    """
    Check if a user has exceeded their rate limit for an action
    
    Args:
        user_id (str): The user ID
        action (str): The action being rate limited
        max_requests (int): Maximum number of requests allowed in the window
        window_seconds (int): The time window in seconds
        
    Returns:
        bool: True if under limit, False if exceeded
    """
    try:
        cache = get_cache_service()
        if not cache:
            logger.error("Cache service not initialized")
            return True  # Allow request if cache is down
            
        # Get the rate limit key
        key = f"rate_limit:{user_id}:{action}"
        
        # Get current timestamp
        now = int(time.time())
        
        # Get the current window's requests
        window = cache.get(key) or []
        
        # Remove timestamps outside the window
        window = [ts for ts in window if ts > now - window_seconds]
        
        # Check if we're over the limit
        if len(window) >= max_requests:
            logger.warning(f"Rate limit exceeded for user {user_id} on action {action}")
            return False
            
        # Add current timestamp and update cache
        window.append(now)
        cache.set(key, window, expire_seconds=window_seconds)
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking rate limit: {e}")
        return True  # Allow request if there's an error 