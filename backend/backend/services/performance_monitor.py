import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from config.ai_config import MONITORING_CONFIG
import psutil
from services.redis_service import get_redis
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.config = MONITORING_CONFIG
        self.ensure_log_directory()
        self._redis = get_redis()
        self._process = psutil.Process()

    def ensure_log_directory(self):
        """Ensure log directory exists"""
        if not os.path.exists(self.config['log_directory']):
            os.makedirs(self.config['log_directory'])

    def start_request(self) -> float:
        """Start timing a request"""
        return time.time()

    def log_request(self,
                   model: str,
                   task_type: str,
                   start_time: float,
                   response: Optional[str] = None,
                   error: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log request performance metrics
        """
        if not self.config['enabled']:
            return

        end_time = time.time()
        duration = end_time - start_time

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'task_type': task_type,
            'response_time': duration,
            'success': error is None,
            'error': error if error else None,
            'token_count': len(response.split()) if response else 0,
            'metadata': metadata or {}
        }

        # Write to daily log file
        log_file = os.path.join(
            self.config['log_directory'],
            f"performance_{datetime.now().strftime('%Y%m%d')}.json"
        )

        try:
            existing_logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    existing_logs = json.load(f)
            
            existing_logs.append(metrics)
            
            with open(log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)

        except Exception as e:
            print(f"Error logging performance metrics: {str(e)}")

    def get_model_performance(self, model: str, timeframe: str = 'today') -> Dict[str, Any]:
        """
        Get performance metrics for a specific model
        """
        try:
            # Determine which log file to read based on timeframe
            if timeframe == 'today':
                log_file = os.path.join(
                    self.config['log_directory'],
                    f"performance_{datetime.now().strftime('%Y%m%d')}.json"
                )
            else:
                raise ValueError(f"Unsupported timeframe: {timeframe}")

            if not os.path.exists(log_file):
                return {
                    'average_response_time': 0,
                    'success_rate': 0,
                    'total_requests': 0,
                    'error_rate': 0
                }

            with open(log_file, 'r') as f:
                logs = json.load(f)

            # Filter logs for specific model
            model_logs = [log for log in logs if log['model'] == model]
            
            if not model_logs:
                return {
                    'average_response_time': 0,
                    'success_rate': 0,
                    'total_requests': 0,
                    'error_rate': 0
                }

            total_requests = len(model_logs)
            successful_requests = len([log for log in model_logs if log['success']])
            total_response_time = sum(log['response_time'] for log in model_logs)

            return {
                'average_response_time': total_response_time / total_requests,
                'success_rate': (successful_requests / total_requests) * 100,
                'total_requests': total_requests,
                'error_rate': ((total_requests - successful_requests) / total_requests) * 100
            }

        except Exception as e:
            print(f"Error getting model performance: {str(e)}")
            return {
                'average_response_time': 0,
                'success_rate': 0,
                'total_requests': 0,
                'error_rate': 0
            }

    def track_request_time(self, endpoint: str, execution_time: float) -> None:
        """Track the execution time of a request for a specific endpoint.
        
        Args:
            endpoint: The API endpoint being monitored
            execution_time: Request execution time in milliseconds
        """
        try:
            # Increment request count for the endpoint
            self._redis.hincrby('request_counts', endpoint, 1)
            
            # Store execution time in a list for the endpoint
            self._redis.rpush(f'request_times:{endpoint}', execution_time)
            
            # Trim the list to keep only recent data (last 1000 requests)
            self._redis.ltrim(f'request_times:{endpoint}', -1000, -1)
        except Exception as e:
            logger.error(f"Error tracking request time: {str(e)}")
    
    def get_average_response_time(self, endpoint: str) -> float:
        """Calculate average response time for an endpoint.
        
        Args:
            endpoint: The API endpoint to analyze
            
        Returns:
            float: Average response time in milliseconds
        """
        try:
            times = self._redis.lrange(f'request_times:{endpoint}', 0, -1)
            if not times:
                return 0.0
            
            # Convert bytes to float and calculate average
            times_float = [float(t.decode()) for t in times]
            return sum(times_float) / len(times_float)
        except Exception as e:
            logger.error(f"Error calculating average response time: {str(e)}")
            return 0.0
    
    def get_request_count(self, endpoint: str) -> int:
        """Get total request count for an endpoint.
        
        Args:
            endpoint: The API endpoint to check
            
        Returns:
            int: Total number of requests
        """
        try:
            count = self._redis.hget('request_counts', endpoint)
            return int(count.decode()) if count else 0
        except Exception as e:
            logger.error(f"Error getting request count: {str(e)}")
            return 0
    
    def track_error(self, error_type: str, endpoint: str) -> None:
        """Track occurrence of an error.
        
        Args:
            error_type: Type of error (e.g., ValidationError)
            endpoint: The endpoint where error occurred
        """
        try:
            self._redis.hincrby('error_counts', f'{endpoint}:{error_type}', 1)
        except Exception as e:
            logger.error(f"Error tracking error occurrence: {str(e)}")
    
    def get_error_count(self, error_type: str, endpoint: str) -> int:
        """Get error count for a specific type and endpoint.
        
        Args:
            error_type: Type of error to check
            endpoint: The endpoint to check
            
        Returns:
            int: Number of errors
        """
        try:
            count = self._redis.hget('error_counts', f'{endpoint}:{error_type}')
            return int(count.decode()) if count else 0
        except Exception as e:
            logger.error(f"Error getting error count: {str(e)}")
            return 0
    
    def track_memory_usage(self) -> None:
        """Track current memory usage of the application."""
        try:
            # Get memory usage in MB
            memory_mb = self._process.memory_info().rss / (1024 * 1024)
            self._redis.rpush('memory_usage', memory_mb)
            
            # Keep only last 24 hours of data (assuming 1-minute intervals)
            self._redis.ltrim('memory_usage', -1440, -1)
        except Exception as e:
            logger.error(f"Error tracking memory usage: {str(e)}")
    
    def get_average_memory_usage(self) -> float:
        """Calculate average memory usage.
        
        Returns:
            float: Average memory usage in MB
        """
        try:
            usages = self._redis.lrange('memory_usage', 0, -1)
            if not usages:
                return 0.0
            
            usages_float = [float(u.decode()) for u in usages]
            return sum(usages_float) / len(usages_float)
        except Exception as e:
            logger.error(f"Error calculating average memory usage: {str(e)}")
            return 0.0
    
    def track_cpu_usage(self) -> None:
        """Track current CPU usage percentage."""
        try:
            cpu_percent = psutil.cpu_percent()
            self._redis.rpush('cpu_usage', cpu_percent)
            
            # Keep only last 24 hours of data (assuming 1-minute intervals)
            self._redis.ltrim('cpu_usage', -1440, -1)
        except Exception as e:
            logger.error(f"Error tracking CPU usage: {str(e)}")
    
    def get_average_cpu_usage(self) -> float:
        """Calculate average CPU usage.
        
        Returns:
            float: Average CPU usage percentage
        """
        try:
            usages = self._redis.lrange('cpu_usage', 0, -1)
            if not usages:
                return 0.0
            
            usages_float = [float(u.decode()) for u in usages]
            return sum(usages_float) / len(usages_float)
        except Exception as e:
            logger.error(f"Error calculating average CPU usage: {str(e)}")
            return 0.0
    
    def track_database_query(self, query_type: str, execution_time: float) -> None:
        """Track database query execution time.
        
        Args:
            query_type: Type of query (select, insert, update, delete)
            execution_time: Query execution time in milliseconds
        """
        try:
            self._redis.hincrby('query_counts', query_type, 1)
            self._redis.rpush(f'query_times:{query_type}', execution_time)
            
            # Keep only recent queries
            self._redis.ltrim(f'query_times:{query_type}', -1000, -1)
        except Exception as e:
            logger.error(f"Error tracking database query: {str(e)}")
    
    def get_slow_queries(self, threshold: float = 100.0) -> List[Dict[str, Union[str, float]]]:
        """Get statistics about slow queries.
        
        Args:
            threshold: Time threshold in milliseconds to consider a query slow
            
        Returns:
            List of slow query information
        """
        try:
            query_types = ['select', 'insert', 'update', 'delete']
            slow_queries = []
            
            for query_type in query_types:
                times = self._redis.lrange(f'query_times:{query_type}', 0, -1)
                if not times:
                    continue
                
                times_float = [float(t.decode()) for t in times]
                slow_times = [t for t in times_float if t > threshold]
                
                if slow_times:
                    slow_queries.append({
                        'type': query_type,
                        'count': len(slow_times),
                        'average_time': sum(slow_times) / len(slow_times)
                    })
            
            return slow_queries
        except Exception as e:
            logger.error(f"Error getting slow queries: {str(e)}")
            return []
    
    def generate_report(self) -> Dict[str, Union[float, int, Dict]]:
        """Generate a comprehensive performance report.
        
        Returns:
            Dictionary containing various performance metrics
        """
        try:
            endpoints = self._redis.hkeys('request_counts')
            endpoints = [e.decode() for e in endpoints] if endpoints else []
            
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'average_response_time': {},
                'total_requests': 0,
                'error_rate': 0.0,
                'memory_usage': self.get_average_memory_usage(),
                'cpu_usage': self.get_average_cpu_usage(),
                'slow_queries': self.get_slow_queries()
            }
            
            total_errors = 0
            for endpoint in endpoints:
                avg_time = self.get_average_response_time(endpoint)
                req_count = self.get_request_count(endpoint)
                error_count = sum(
                    self.get_error_count(error_type, endpoint)
                    for error_type in ['ValidationError', 'AuthError', 'ServerError']
                )
                
                report['average_response_time'][endpoint] = avg_time
                report['total_requests'] += req_count
                total_errors += error_count
            
            if report['total_requests'] > 0:
                report['error_rate'] = (total_errors / report['total_requests']) * 100
            
            return report
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }
    
    def cleanup_old_metrics(self, retention_days: int = 7) -> None:
        """Clean up metrics older than specified days.
        
        Args:
            retention_days: Number of days to retain metrics
        """
        try:
            cutoff = datetime.utcnow() - timedelta(days=retention_days)
            pattern = f'*:{cutoff.strftime("%Y%m%d")}:*'
            
            # Get all keys matching the pattern
            keys = self._redis.keys(pattern)
            if keys:
                self._redis.delete(*keys)
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {str(e)}")
    
    def track_concurrent_users(self, count: int) -> None:
        """Track number of concurrent users.
        
        Args:
            count: Number of current active users
        """
        try:
            self._redis.set('concurrent_users', count, ex=60)  # 1-minute expiry
            
            # Update peak if current count is higher
            peak = self.get_peak_concurrent_users()
            if count > peak:
                self._redis.set('peak_concurrent_users', count)
        except Exception as e:
            logger.error(f"Error tracking concurrent users: {str(e)}")
    
    def get_peak_concurrent_users(self) -> int:
        """Get peak number of concurrent users.
        
        Returns:
            int: Peak number of concurrent users
        """
        try:
            peak = self._redis.get('peak_concurrent_users')
            return int(peak.decode()) if peak else 0
        except Exception as e:
            logger.error(f"Error getting peak concurrent users: {str(e)}")
            return 0

# Create singleton instance
performance_monitor = PerformanceMonitor() 