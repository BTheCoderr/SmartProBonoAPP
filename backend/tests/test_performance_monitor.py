import pytest
from unittest.mock import Mock, patch, MagicMock
import time
from datetime import datetime, timedelta
from services.performance_monitor import PerformanceMonitor
import redis

@pytest.fixture
def performance_monitor():
    """Create a performance monitor instance with mocked dependencies."""
    with patch('services.performance_monitor.get_redis') as mock_redis:
        monitor = PerformanceMonitor()
        monitor._redis = mock_redis.return_value
        yield monitor

def test_track_request_time(performance_monitor):
    """Test tracking request execution time."""
    endpoint = '/api/test'
    execution_time = 150  # milliseconds
    
    performance_monitor.track_request_time(endpoint, execution_time)
    
    performance_monitor._redis.hincrby.assert_called_with(
        'request_counts', endpoint, 1
    )
    performance_monitor._redis.rpush.assert_called_with(
        f'request_times:{endpoint}', execution_time
    )

def test_get_average_response_time(performance_monitor):
    """Test getting average response time for an endpoint."""
    endpoint = '/api/test'
    times = [100, 150, 200]  # milliseconds
    
    performance_monitor._redis.lrange.return_value = [
        str(t).encode() for t in times
    ]
    
    avg_time = performance_monitor.get_average_response_time(endpoint)
    
    assert avg_time == sum(times) / len(times)
    performance_monitor._redis.lrange.assert_called_with(
        f'request_times:{endpoint}', 0, -1
    )

def test_get_request_count(performance_monitor):
    """Test getting request count for an endpoint."""
    endpoint = '/api/test'
    count = 42
    
    performance_monitor._redis.hget.return_value = str(count).encode()
    
    result = performance_monitor.get_request_count(endpoint)
    
    assert result == count
    performance_monitor._redis.hget.assert_called_with(
        'request_counts', endpoint
    )

def test_track_error(performance_monitor):
    """Test tracking an error occurrence."""
    error_type = 'ValidationError'
    endpoint = '/api/test'
    
    performance_monitor.track_error(error_type, endpoint)
    
    performance_monitor._redis.hincrby.assert_called_with(
        'error_counts', f'{endpoint}:{error_type}', 1
    )

def test_get_error_count(performance_monitor):
    """Test getting error count for an endpoint and error type."""
    error_type = 'ValidationError'
    endpoint = '/api/test'
    count = 5
    
    performance_monitor._redis.hget.return_value = str(count).encode()
    
    result = performance_monitor.get_error_count(error_type, endpoint)
    
    assert result == count
    performance_monitor._redis.hget.assert_called_with(
        'error_counts', f'{endpoint}:{error_type}'
    )

def test_track_memory_usage(performance_monitor):
    """Test tracking memory usage."""
    memory_usage = 1024  # MB
    
    with patch('psutil.Process') as mock_process:
        mock_process.return_value.memory_info.return_value.rss = memory_usage * 1024 * 1024
        
        performance_monitor.track_memory_usage()
        
        performance_monitor._redis.rpush.assert_called_with(
            'memory_usage', memory_usage
        )

def test_get_average_memory_usage(performance_monitor):
    """Test getting average memory usage."""
    usages = [1024, 1536, 2048]  # MB
    
    performance_monitor._redis.lrange.return_value = [
        str(u).encode() for u in usages
    ]
    
    avg_usage = performance_monitor.get_average_memory_usage()
    
    assert avg_usage == sum(usages) / len(usages)
    performance_monitor._redis.lrange.assert_called_with(
        'memory_usage', 0, -1
    )

def test_track_cpu_usage(performance_monitor):
    """Test tracking CPU usage."""
    cpu_percent = 45.5
    
    with patch('psutil.cpu_percent') as mock_cpu:
        mock_cpu.return_value = cpu_percent
        
        performance_monitor.track_cpu_usage()
        
        performance_monitor._redis.rpush.assert_called_with(
            'cpu_usage', cpu_percent
        )

def test_get_average_cpu_usage(performance_monitor):
    """Test getting average CPU usage."""
    usages = [30.5, 45.5, 60.0]
    
    performance_monitor._redis.lrange.return_value = [
        str(u).encode() for u in usages
    ]
    
    avg_usage = performance_monitor.get_average_cpu_usage()
    
    assert avg_usage == sum(usages) / len(usages)
    performance_monitor._redis.lrange.assert_called_with(
        'cpu_usage', 0, -1
    )

def test_track_database_query(performance_monitor):
    """Test tracking database query execution time."""
    query_type = 'select'
    execution_time = 50  # milliseconds
    
    performance_monitor.track_database_query(query_type, execution_time)
    
    performance_monitor._redis.hincrby.assert_called_with(
        'query_counts', query_type, 1
    )
    performance_monitor._redis.rpush.assert_called_with(
        f'query_times:{query_type}', execution_time
    )

def test_get_slow_queries(performance_monitor):
    """Test getting slow query statistics."""
    threshold = 100  # milliseconds
    query_times = [50, 150, 200]  # milliseconds
    
    performance_monitor._redis.lrange.return_value = [
        str(t).encode() for t in query_times
    ]
    
    slow_queries = performance_monitor.get_slow_queries(threshold)
    
    assert len(slow_queries) == 2  # Two queries above threshold
    performance_monitor._redis.lrange.assert_called_with(
        'query_times:select', 0, -1
    )

def test_generate_performance_report(performance_monitor):
    """Test generating a performance report."""
    with patch.object(performance_monitor, 'get_average_response_time') as mock_avg_time, \
         patch.object(performance_monitor, 'get_request_count') as mock_req_count, \
         patch.object(performance_monitor, 'get_error_count') as mock_error_count, \
         patch.object(performance_monitor, 'get_average_memory_usage') as mock_mem_usage, \
         patch.object(performance_monitor, 'get_average_cpu_usage') as mock_cpu_usage:
        
        mock_avg_time.return_value = 100
        mock_req_count.return_value = 1000
        mock_error_count.return_value = 5
        mock_mem_usage.return_value = 1024
        mock_cpu_usage.return_value = 45.5
        
        report = performance_monitor.generate_report()
        
        assert isinstance(report, dict)
        assert 'average_response_time' in report
        assert 'total_requests' in report
        assert 'error_rate' in report
        assert 'memory_usage' in report
        assert 'cpu_usage' in report

def test_cleanup_old_metrics(performance_monitor):
    """Test cleaning up old metrics."""
    retention_days = 7
    
    performance_monitor.cleanup_old_metrics(retention_days)
    
    assert performance_monitor._redis.delete.call_count > 0

def test_track_concurrent_users(performance_monitor):
    """Test tracking concurrent users."""
    performance_monitor.track_concurrent_users(5)
    
    performance_monitor._redis.set.assert_called_with(
        'concurrent_users',
        5,
        ex=60  # 1-minute expiry
    )

def test_get_peak_concurrent_users(performance_monitor):
    """Test getting peak concurrent users."""
    peak_users = 10
    
    performance_monitor._redis.get.return_value = str(peak_users).encode()
    
    result = performance_monitor.get_peak_concurrent_users()
    
    assert result == peak_users
    performance_monitor._redis.get.assert_called_with('peak_concurrent_users')

def test_track_request_time_with_invalid_endpoint(performance_monitor):
    """Test tracking request time with invalid endpoint."""
    performance_monitor._redis.hincrby.side_effect = redis.RedisError("Connection error")
    
    # Should not raise exception but log error
    performance_monitor.track_request_time("", 100)
    
    assert performance_monitor._redis.hincrby.called
    assert performance_monitor._redis.rpush.not_called

def test_get_average_response_time_empty_data(performance_monitor):
    """Test getting average response time when no data exists."""
    performance_monitor._redis.lrange.return_value = []
    
    avg_time = performance_monitor.get_average_response_time('/api/test')
    
    assert avg_time == 0.0
    performance_monitor._redis.lrange.assert_called_once()

def test_get_average_response_time_invalid_data(performance_monitor):
    """Test getting average response time with invalid data."""
    performance_monitor._redis.lrange.return_value = [b'invalid', b'123.45']
    
    avg_time = performance_monitor.get_average_response_time('/api/test')
    
    assert avg_time == 0.0  # Should return 0 on error

def test_track_memory_usage_process_error(performance_monitor):
    """Test tracking memory usage when process info fails."""
    with patch('psutil.Process') as mock_process:
        mock_process.side_effect = psutil.NoSuchProcess(0)
        performance_monitor._process = mock_process()
        
        # Should not raise exception but log error
        performance_monitor.track_memory_usage()
        
        assert performance_monitor._redis.rpush.not_called

def test_track_cpu_usage_error(performance_monitor):
    """Test tracking CPU usage when psutil fails."""
    with patch('psutil.cpu_percent') as mock_cpu:
        mock_cpu.side_effect = Exception("CPU info not available")
        
        # Should not raise exception but log error
        performance_monitor.track_cpu_usage()
        
        assert performance_monitor._redis.rpush.not_called

def test_get_slow_queries_with_invalid_data(performance_monitor):
    """Test getting slow queries with invalid data in Redis."""
    performance_monitor._redis.lrange.return_value = [b'invalid', b'not_a_number']
    
    slow_queries = performance_monitor.get_slow_queries(threshold=100)
    
    assert len(slow_queries) == 0  # Should return empty list on error

def test_generate_report_with_redis_error(performance_monitor):
    """Test generating report when Redis operations fail."""
    performance_monitor._redis.hkeys.side_effect = redis.RedisError("Connection lost")
    
    report = performance_monitor.generate_report()
    
    assert 'error' in report
    assert 'timestamp' in report
    assert isinstance(report['error'], str)

def test_cleanup_old_metrics_with_no_keys(performance_monitor):
    """Test cleanup when no keys match the pattern."""
    performance_monitor._redis.keys.return_value = []
    
    performance_monitor.cleanup_old_metrics(retention_days=7)
    
    assert performance_monitor._redis.delete.not_called

def test_track_concurrent_users_negative_count(performance_monitor):
    """Test tracking concurrent users with negative count."""
    performance_monitor.track_concurrent_users(-5)
    
    # Should still set the value but not update peak
    performance_monitor._redis.set.assert_called_once_with('concurrent_users', -5, ex=60)
    assert not performance_monitor._redis.get.called

def test_get_peak_concurrent_users_invalid_data(performance_monitor):
    """Test getting peak concurrent users with invalid data."""
    performance_monitor._redis.get.return_value = b'not_a_number'
    
    result = performance_monitor.get_peak_concurrent_users()
    
    assert result == 0  # Should return 0 on error

def test_track_database_query_invalid_type(performance_monitor):
    """Test tracking database query with invalid query type."""
    performance_monitor.track_database_query('invalid_type', 100)
    
    # Should still attempt to track but might fail silently
    performance_monitor._redis.hincrby.assert_called_once()

def test_generate_report_with_division_by_zero(performance_monitor):
    """Test report generation with zero total requests."""
    performance_monitor._redis.hkeys.return_value = [b'/api/test']
    performance_monitor.get_request_count = Mock(return_value=0)
    
    report = performance_monitor.generate_report()
    
    assert report['error_rate'] == 0.0
    assert report['total_requests'] == 0

def test_track_request_time_very_large_number(performance_monitor):
    """Test tracking request time with very large number."""
    large_time = float('inf')
    
    performance_monitor.track_request_time('/api/test', large_time)
    
    performance_monitor._redis.rpush.assert_called_once_with(
        'request_times:/api/test', large_time
    )

def test_cleanup_old_metrics_redis_error(performance_monitor):
    """Test cleanup with Redis error."""
    performance_monitor._redis.keys.side_effect = redis.RedisError("Connection error")
    
    # Should not raise exception but log error
    performance_monitor.cleanup_old_metrics()
    
    assert not performance_monitor._redis.delete.called

@pytest.mark.integration
def test_integration_with_real_redis():
    """Integration test with real Redis instance.
    
    Note: Requires a running Redis instance on localhost:6379
    """
    try:
        # Create real Redis connection
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        redis_client.ping()  # Ensure connection is alive
        
        # Create monitor with real Redis
        monitor = PerformanceMonitor()
        monitor._redis = redis_client
        
        # Test full workflow
        endpoint = '/api/test_integration'
        
        # Track some requests
        monitor.track_request_time(endpoint, 100)
        monitor.track_request_time(endpoint, 200)
        monitor.track_error('TestError', endpoint)
        
        # Verify data
        avg_time = monitor.get_average_response_time(endpoint)
        assert 100 <= avg_time <= 200
        
        count = monitor.get_request_count(endpoint)
        assert count == 2
        
        error_count = monitor.get_error_count('TestError', endpoint)
        assert error_count == 1
        
        # Cleanup
        monitor.cleanup_old_metrics(retention_days=0)
        
    except (redis.ConnectionError, redis.RedisError) as e:
        pytest.skip(f"Redis integration tests skipped: {str(e)}")
    finally:
        if 'redis_client' in locals():
            redis_client.close()