import pytest
from unittest.mock import Mock, patch, MagicMock
from services.redis_service import RedisService
import redis

@pytest.fixture
def redis_service():
    """Create a Redis service instance with mocked Redis client."""
    with patch('redis.Redis') as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        service = RedisService()
        service._client = mock_client
        yield service

def test_connect(redis_service):
    """Test Redis connection initialization."""
    with patch('redis.Redis') as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        
        redis_service.connect()
        
        mock_redis.assert_called_once()
        assert redis_service._client is not None

def test_connect_with_custom_config(redis_service):
    """Test Redis connection with custom configuration."""
    config = {
        'host': 'custom-host',
        'port': 6380,
        'db': 1,
        'password': 'secret'
    }
    
    with patch('redis.Redis') as mock_redis:
        mock_client = MagicMock()
        mock_redis.return_value = mock_client
        
        redis_service.connect(config)
        
        mock_redis.assert_called_once_with(**config)
        assert redis_service._client is not None

def test_set_key(redis_service):
    """Test setting a key in Redis."""
    key = 'test_key'
    value = 'test_value'
    expiry = 3600
    
    redis_service.set(key, value, expiry)
    
    redis_service._client.setex.assert_called_once_with(
        key, expiry, value
    )

def test_get_key(redis_service):
    """Test getting a key from Redis."""
    key = 'test_key'
    expected_value = 'test_value'
    redis_service._client.get.return_value = expected_value.encode()
    
    value = redis_service.get(key)
    
    assert value == expected_value
    redis_service._client.get.assert_called_once_with(key)

def test_delete_key(redis_service):
    """Test deleting a key from Redis."""
    key = 'test_key'
    redis_service._client.delete.return_value = 1
    
    result = redis_service.delete(key)
    
    assert result == True
    redis_service._client.delete.assert_called_once_with(key)

def test_exists(redis_service):
    """Test checking if a key exists in Redis."""
    key = 'test_key'
    redis_service._client.exists.return_value = 1
    
    result = redis_service.exists(key)
    
    assert result == True
    redis_service._client.exists.assert_called_once_with(key)

def test_increment(redis_service):
    """Test incrementing a counter in Redis."""
    key = 'counter'
    redis_service._client.incr.return_value = 1
    
    value = redis_service.increment(key)
    
    assert value == 1
    redis_service._client.incr.assert_called_once_with(key)

def test_decrement(redis_service):
    """Test decrementing a counter in Redis."""
    key = 'counter'
    redis_service._client.decr.return_value = 0
    
    value = redis_service.decrement(key)
    
    assert value == 0
    redis_service._client.decr.assert_called_once_with(key)

def test_set_hash(redis_service):
    """Test setting a hash in Redis."""
    key = 'hash_key'
    field = 'field'
    value = 'value'
    
    redis_service.hset(key, field, value)
    
    redis_service._client.hset.assert_called_once_with(
        key, field, value
    )

def test_get_hash(redis_service):
    """Test getting a hash field from Redis."""
    key = 'hash_key'
    field = 'field'
    expected_value = 'value'
    redis_service._client.hget.return_value = expected_value.encode()
    
    value = redis_service.hget(key, field)
    
    assert value == expected_value
    redis_service._client.hget.assert_called_once_with(key, field)

def test_get_all_hash(redis_service):
    """Test getting all hash fields from Redis."""
    key = 'hash_key'
    expected_values = {
        'field1': 'value1',
        'field2': 'value2'
    }
    redis_service._client.hgetall.return_value = {
        k.encode(): v.encode() for k, v in expected_values.items()
    }
    
    values = redis_service.hgetall(key)
    
    assert values == expected_values
    redis_service._client.hgetall.assert_called_once_with(key)

def test_delete_hash_field(redis_service):
    """Test deleting a hash field from Redis."""
    key = 'hash_key'
    field = 'field'
    redis_service._client.hdel.return_value = 1
    
    result = redis_service.hdel(key, field)
    
    assert result == True
    redis_service._client.hdel.assert_called_once_with(key, field)

def test_set_list(redis_service):
    """Test setting a list in Redis."""
    key = 'list_key'
    values = ['value1', 'value2', 'value3']
    
    redis_service.lpush(key, *values)
    
    redis_service._client.lpush.assert_called_once_with(key, *values)

def test_get_list(redis_service):
    """Test getting a list from Redis."""
    key = 'list_key'
    expected_values = ['value1', 'value2', 'value3']
    redis_service._client.lrange.return_value = [
        v.encode() for v in expected_values
    ]
    
    values = redis_service.lrange(key, 0, -1)
    
    assert values == expected_values
    redis_service._client.lrange.assert_called_once_with(key, 0, -1)

def test_connection_error():
    """Test handling Redis connection error."""
    with patch('redis.Redis') as mock_redis:
        mock_redis.side_effect = redis.ConnectionError('Connection refused')
        
        with pytest.raises(redis.ConnectionError):
            RedisService().connect()

def test_operation_error(redis_service):
    """Test handling Redis operation error."""
    redis_service._client.get.side_effect = redis.RedisError('Operation failed')
    
    with pytest.raises(redis.RedisError):
        redis_service.get('test_key') 