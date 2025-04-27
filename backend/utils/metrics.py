"""
Utility functions for collecting system metrics
"""
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from backend.database.mongo import mongo

logger = logging.getLogger(__name__)

def get_time_range_start(time_range: str) -> datetime:
    """Get the start time based on the time range"""
    now = datetime.utcnow()
    if time_range == '1h':
        return now - timedelta(hours=1)
    elif time_range == '24h':
        return now - timedelta(days=1)
    elif time_range == '7d':
        return now - timedelta(days=7)
    elif time_range == '30d':
        return now - timedelta(days=30)
    else:
        raise ValueError(f"Invalid time range: {time_range}")

def get_system_metrics(time_range: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get system metrics (CPU, memory usage)
    
    Args:
        time_range: Time range to fetch metrics for ('1h', '24h', '7d', '30d')
        
    Returns:
        Dictionary containing system metrics
    """
    try:
        # Get current metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # In a real application, these would be fetched from a time series database
        # For demo purposes, we'll generate some sample data
        start_time = get_time_range_start(time_range)
        current_time = datetime.utcnow()
        
        # Generate data points
        if time_range == '1h':
            interval = timedelta(minutes=1)
        elif time_range == '24h':
            interval = timedelta(minutes=15)
        elif time_range == '7d':
            interval = timedelta(hours=1)
        else:  # 30d
            interval = timedelta(hours=4)
            
        data_points = []
        current = start_time
        
        while current <= current_time:
            # Simulate some variation in the metrics
            cpu_var = (hash(str(current)) % 20) - 10  # +/- 10%
            mem_var = (hash(str(current)) % 10) - 5   # +/- 5%
            
            data_points.append({
                'timestamp': current.isoformat(),
                'cpu': max(0, min(100, cpu_percent + cpu_var)),
                'memory': max(0, min(100, memory_percent + mem_var))
            })
            current += interval
            
        # Format the response
        return {
            'cpu_usage': [{'timestamp': dp['timestamp'], 'value': dp['cpu']} for dp in data_points],
            'memory_usage': [{'timestamp': dp['timestamp'], 'value': dp['memory']} for dp in data_points]
        }
    except Exception as e:
        logger.error(f"Error collecting system metrics: {str(e)}")
        return {
            'cpu_usage': [],
            'memory_usage': []
        }

def get_api_metrics(time_range: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get API metrics (response times, error rates, active users)
    
    Args:
        time_range: Time range to fetch metrics for ('1h', '24h', '7d', '30d')
        
    Returns:
        Dictionary containing API metrics
    """
    try:
        # In a real application, these would be fetched from a monitoring system
        # For demo purposes, we'll generate sample data
        start_time = get_time_range_start(time_range)
        current_time = datetime.utcnow()
        
        # Generate data points with appropriate intervals
        if time_range == '1h':
            interval = timedelta(minutes=1)
        elif time_range == '24h':
            interval = timedelta(minutes=15)
        elif time_range == '7d':
            interval = timedelta(hours=1)
        else:  # 30d
            interval = timedelta(hours=4)
            
        data_points = []
        current = start_time
        
        while current <= current_time:
            # Simulate metrics with some variation
            response_time = 100 + (hash(str(current)) % 100)  # 100-200ms
            error_rate = max(0, min(5, (hash(str(current)) % 10) / 2))  # 0-5%
            active_users = 50 + (hash(str(current)) % 100)  # 50-150 users
            
            data_points.append({
                'timestamp': current.isoformat(),
                'response_time': response_time,
                'error_rate': error_rate,
                'active_users': active_users
            })
            current += interval
            
        # Format the response
        return {
            'response_times': [{'timestamp': dp['timestamp'], 'value': dp['response_time']} for dp in data_points],
            'error_rates': [{'timestamp': dp['timestamp'], 'value': dp['error_rate']} for dp in data_points],
            'active_users': [{'timestamp': dp['timestamp'], 'value': dp['active_users']} for dp in data_points]
        }
    except Exception as e:
        logger.error(f"Error collecting API metrics: {str(e)}")
        return {
            'response_times': [],
            'error_rates': [],
            'active_users': []
        }

def get_database_metrics(time_range: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get database performance metrics
    
    Args:
        time_range: Time range to fetch metrics for ('1h', '24h', '7d', '30d')
        
    Returns:
        Dictionary containing database metrics
    """
    try:
        # In a real application, these would be fetched from MongoDB's built-in monitoring
        # For demo purposes, we'll generate sample data
        start_time = get_time_range_start(time_range)
        current_time = datetime.utcnow()
        
        # Generate data points with appropriate intervals
        if time_range == '1h':
            interval = timedelta(minutes=1)
        elif time_range == '24h':
            interval = timedelta(minutes=15)
        elif time_range == '7d':
            interval = timedelta(hours=1)
        else:  # 30d
            interval = timedelta(hours=4)
            
        data_points = []
        current = start_time
        
        while current <= current_time:
            # Simulate query times with some variation
            query_time = 20 + (hash(str(current)) % 30)  # 20-50ms
            
            data_points.append({
                'timestamp': current.isoformat(),
                'query_time': query_time
            })
            current += interval
            
        # Format the response
        return {
            'query_times': [{'timestamp': dp['timestamp'], 'value': dp['query_time']} for dp in data_points]
        }
    except Exception as e:
        logger.error(f"Error collecting database metrics: {str(e)}")
        return {
            'query_times': []
        } 