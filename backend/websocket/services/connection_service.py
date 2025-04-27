"""
Connection Service for WebSocket.

This module provides functionality for tracking and managing
active WebSocket connections and sessions.
"""

import logging
import threading
from datetime import datetime
from collections import defaultdict
from flask import current_app

# Configure logging
logger = logging.getLogger('websocket.services.connection')

# Thread-safe connection tracking
_connection_lock = threading.RLock()
_user_to_sid_map = defaultdict(set)  # Maps user_id to a set of session IDs
_sid_to_user_map = {}  # Maps session ID to user_id
_connection_metadata = {}  # Stores metadata for each connection

def register_connection(sid, user_id, metadata=None):
    """
    Register a new WebSocket connection for a user.
    
    Args:
        sid (str): The Socket.IO session ID
        user_id (str): The user ID
        metadata (dict, optional): Additional connection metadata
        
    Returns:
        bool: True if registration successful, False otherwise
    """
    if not sid or not user_id:
        logger.error("Cannot register connection: missing sid or user_id")
        return False
    
    with _connection_lock:
        # Add the mapping from user to session
        _user_to_sid_map[user_id].add(sid)
        
        # Add the reverse mapping
        _sid_to_user_map[sid] = user_id
        
        # Store metadata with timestamp
        _connection_metadata[sid] = {
            'connected_at': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'client_info': metadata or {}
        }
    
    total_connections = len(_sid_to_user_map)
    unique_users = len(_user_to_sid_map)
    logger.info(f"User {user_id} connected with sid {sid}. Total: {total_connections} connections, {unique_users} unique users")
    return True

def unregister_connection(sid):
    """
    Unregister a WebSocket connection.
    
    Args:
        sid (str): The Socket.IO session ID
        
    Returns:
        bool: True if unregistration successful, False otherwise
    """
    if not sid:
        logger.error("Cannot unregister connection: missing sid")
        return False
    
    with _connection_lock:
        # Get the user ID for this session
        user_id = _sid_to_user_map.pop(sid, None)
        
        if user_id:
            # Remove the session from user's set of sessions
            if sid in _user_to_sid_map[user_id]:
                _user_to_sid_map[user_id].remove(sid)
                
            # Clean up if this was the user's last session
            if not _user_to_sid_map[user_id]:
                del _user_to_sid_map[user_id]
            
            # Clean up metadata
            if sid in _connection_metadata:
                del _connection_metadata[sid]
                
            total_connections = len(_sid_to_user_map)
            unique_users = len(_user_to_sid_map)
            logger.info(f"User {user_id} disconnected (sid: {sid}). Remaining: {total_connections} connections, {unique_users} unique users")
            return True
        else:
            logger.warning(f"Attempted to unregister unknown session: {sid}")
            return False

def get_user_sessions(user_id):
    """
    Get all active session IDs for a user.
    
    Args:
        user_id (str): The user ID
        
    Returns:
        set: Set of active session IDs for the user
    """
    with _connection_lock:
        return set(_user_to_sid_map.get(user_id, set()))

def get_connection_user(sid):
    """
    Get the user ID associated with a session ID.
    
    Args:
        sid (str): The Socket.IO session ID
        
    Returns:
        str or None: The user ID or None if not found
    """
    with _connection_lock:
        return _sid_to_user_map.get(sid)

def get_connection_metadata(sid):
    """
    Get metadata for a connection.
    
    Args:
        sid (str): The Socket.IO session ID
        
    Returns:
        dict or None: Connection metadata or None if not found
    """
    with _connection_lock:
        return _connection_metadata.get(sid)

def update_connection_metadata(sid, metadata_updates):
    """
    Update metadata for a connection.
    
    Args:
        sid (str): The Socket.IO session ID
        metadata_updates (dict): Metadata fields to update
        
    Returns:
        bool: True if update successful, False otherwise
    """
    if not sid or not isinstance(metadata_updates, dict):
        return False
    
    with _connection_lock:
        if sid in _connection_metadata:
            # Update only the provided fields
            _connection_metadata[sid]['client_info'].update(metadata_updates)
            # Add updated_at timestamp
            _connection_metadata[sid]['updated_at'] = datetime.utcnow().isoformat()
            return True
        return False

def is_user_connected(user_id):
    """
    Check if a user has any active connections.
    
    Args:
        user_id (str): The user ID
        
    Returns:
        bool: True if user has active connections, False otherwise
    """
    with _connection_lock:
        return user_id in _user_to_sid_map and bool(_user_to_sid_map[user_id])

def get_connected_users():
    """
    Get a list of all connected users and their session counts.
    
    Returns:
        list: List of dicts with user_id and session_count
    """
    with _connection_lock:
        return [
            {'user_id': user_id, 'session_count': len(sessions)}
            for user_id, sessions in _user_to_sid_map.items()
        ]

def get_connection_stats():
    """
    Get statistics about active connections.
    
    Returns:
        dict: Connection statistics
    """
    with _connection_lock:
        total_connections = len(_sid_to_user_map)
        unique_users = len(_user_to_sid_map)
        
        # Calculate users with multiple connections
        multi_session_users = sum(
            1 for sessions in _user_to_sid_map.values() if len(sessions) > 1
        )
        
        # Get the user with most connections
        most_connections = 0
        if _user_to_sid_map:
            most_connections = max(
                len(sessions) for sessions in _user_to_sid_map.values()
            )
        
        return {
            'total_connections': total_connections,
            'unique_users': unique_users,
            'multi_session_users': multi_session_users,
            'most_connections_per_user': most_connections,
            'timestamp': datetime.utcnow().isoformat()
        }

def clear_all_connections():
    """
    Clear all tracked connections (primarily for testing/reset).
    
    Returns:
        int: Number of connections cleared
    """
    with _connection_lock:
        connection_count = len(_sid_to_user_map)
        _user_to_sid_map.clear()
        _sid_to_user_map.clear()
        _connection_metadata.clear()
        
        logger.warning(f"Cleared all {connection_count} tracked connections")
        return connection_count 