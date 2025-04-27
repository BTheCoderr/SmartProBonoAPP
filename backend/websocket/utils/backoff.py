"""
Backoff strategy utilities for retrying operations
"""
import random
import math
from typing import Optional

def exponential_backoff(attempt: int, base_delay: float = 0.5, jitter: float = 0.1, cap: float = 30.0) -> float:
    """
    Calculate exponential backoff with jitter
    
    Args:
        attempt: The attempt number (starting from 1)
        base_delay: The base delay in seconds
        jitter: The jitter factor (0-1) to add randomness
        cap: The maximum delay in seconds
        
    Returns:
        The delay in seconds to wait before the next attempt
    """
    # Calculate exponential delay: base_delay * 2^(attempt-1)
    delay = base_delay * (2 ** (attempt - 1))
    
    # Add jitter
    jitter_amount = random.uniform(-jitter * delay, jitter * delay)
    delay += jitter_amount
    
    # Cap the delay
    delay = min(delay, cap)
    
    return delay

def linear_backoff(attempt: int, base_delay: float = 1.0, 
                 increment: float = 1.0, max_delay: float = 30.0) -> float:
    """
    Calculate delay using linear backoff strategy
    
    Args:
        attempt: The attempt number (starting from 1)
        base_delay: Base delay in seconds
        increment: Increment per attempt in seconds
        max_delay: Maximum delay in seconds
        
    Returns:
        Delay in seconds
    """
    # Ensure attempt is at least 1
    attempt = max(1, attempt)
    
    # Calculate linear backoff
    delay = min(max_delay, base_delay + (increment * (attempt - 1)))
    
    # Ensure delay is positive
    return max(0.01, delay)

def fibonacci_backoff(attempt: int, base_delay: float = 1.0, 
                    max_delay: float = 30.0) -> float:
    """
    Calculate delay using Fibonacci backoff strategy
    
    Args:
        attempt: The attempt number (starting from 1)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        
    Returns:
        Delay in seconds
    """
    # Ensure attempt is at least 1
    attempt = max(1, min(attempt, 20))  # Cap at 20 to avoid huge Fibonacci numbers
    
    # Calculate Fibonacci number for this attempt
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    
    # Calculate Fibonacci backoff
    delay = min(max_delay, base_delay * fib(attempt))
    
    # Ensure delay is positive
    return max(0.01, delay) 