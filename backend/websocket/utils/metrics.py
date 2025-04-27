"""
Utility functions for tracking WebSocket metrics
"""
import time
from typing import Dict, Any
from threading import Lock

# Metrics store
_connection_metrics = {
    'current_connections': 0,
    'peak_connections': 0,
    'total_connections': 0,
    'total_disconnections': 0,
    'started_at': time.time()
}

# Notification metrics
_notification_metrics = {
    'sent': 0,
    'delivered': 0,
    'failed': 0,
    'queued': 0,
    'error': 0
}

# Thread safety
_metrics_lock = Lock()

def track_connection() -> None:
    """Track a new connection"""
    with _metrics_lock:
        _connection_metrics['current_connections'] += 1
        _connection_metrics['total_connections'] += 1
        
        # Update peak if needed
        if _connection_metrics['current_connections'] > _connection_metrics['peak_connections']:
            _connection_metrics['peak_connections'] = _connection_metrics['current_connections']

def track_disconnection() -> None:
    """Track a disconnection"""
    with _metrics_lock:
        _connection_metrics['current_connections'] -= 1
        _connection_metrics['total_disconnections'] += 1

def get_connection_metrics() -> Dict[str, Any]:
    """
    Get current connection metrics
    
    Returns:
        Dictionary of connection metrics
    """
    with _metrics_lock:
        # Make a copy to avoid modification during access
        metrics = dict(_connection_metrics)
        
        # Add derived metrics
        metrics['uptime_seconds'] = time.time() - metrics['started_at']
        if metrics['uptime_seconds'] > 0:
            metrics['connections_per_second'] = round(
                metrics['total_connections'] / metrics['uptime_seconds'], 2
            )
        else:
            metrics['connections_per_second'] = 0
            
    return metrics

def increment_notification_metric(metric_name: str) -> None:
    """
    Increment a notification metric counter
    
    Args:
        metric_name: The name of the metric to increment
    """
    if metric_name not in _notification_metrics:
        return
        
    with _metrics_lock:
        _notification_metrics[metric_name] += 1

def get_notification_metrics() -> Dict[str, int]:
    """
    Get current notification metrics
    
    Returns:
        Dictionary of notification metrics
    """
    with _metrics_lock:
        # Make a copy to avoid modification during access
        return dict(_notification_metrics)

def get_user_sid(user_id: str) -> str:
    """
    Get the socket ID for a user (placeholder implementation)
    
    Args:
        user_id: The user ID
        
    Returns:
        The socket ID (session ID) if found, empty string otherwise
    """
    # In a real implementation, this would look up the user's session ID
    # For now, we'll return an empty string
    return ""

def get_active_connections() -> int:
    """
    Get the number of active connections
    
    Returns:
        Number of active connections
    """
    with _metrics_lock:
        return _connection_metrics['current_connections'] 