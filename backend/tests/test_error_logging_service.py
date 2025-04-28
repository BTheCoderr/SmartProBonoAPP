import pytest
from unittest.mock import Mock, patch, MagicMock, call
import logging
from datetime import datetime
from services.error_logging_service import ErrorLoggingService

@pytest.fixture
def error_logging_service():
    """Create an error logging service instance with mocked dependencies."""
    with patch('logging.getLogger') as mock_logger:
        service = ErrorLoggingService()
        service._logger = mock_logger
        yield service

@pytest.fixture
def sample_error():
    """Create a sample error object."""
    return {
        'message': 'Test error message',
        'type': 'TestError',
        'stack': 'Error: Test error message\n    at test_function (/test/file.js:10:5)',
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': '12345',
        'request_id': 'req-123',
        'metadata': {
            'browser': 'Chrome',
            'os': 'Windows',
            'url': '/test/path'
        }
    }

def test_log_error(error_logging_service, sample_error):
    """Test logging an error."""
    error_logging_service.log_error(
        message=sample_error['message'],
        error_type=sample_error['type'],
        stack_trace=sample_error['stack'],
        user_id=sample_error['user_id'],
        request_id=sample_error['request_id'],
        metadata=sample_error['metadata']
    )
    
    error_logging_service._logger.error.assert_called_once()
    args = error_logging_service._logger.error.call_args[0]
    assert sample_error['message'] in args[0]
    assert sample_error['type'] in args[0]

def test_log_error_with_exception(error_logging_service):
    """Test logging an error with an exception object."""
    try:
        raise ValueError('Test exception')
    except ValueError as e:
        error_logging_service.log_exception(
            e,
            user_id='12345',
            request_id='req-123'
        )
    
    error_logging_service._logger.exception.assert_called_once()
    args = error_logging_service._logger.exception.call_args[0]
    assert 'Test exception' in args[0]

def test_log_warning(error_logging_service):
    """Test logging a warning."""
    warning_message = 'Test warning message'
    metadata = {'key': 'value'}
    
    error_logging_service.log_warning(
        message=warning_message,
        metadata=metadata
    )
    
    error_logging_service._logger.warning.assert_called_once()
    args = error_logging_service._logger.warning.call_args[0]
    assert warning_message in args[0]

def test_log_info(error_logging_service):
    """Test logging an info message."""
    info_message = 'Test info message'
    metadata = {'key': 'value'}
    
    error_logging_service.log_info(
        message=info_message,
        metadata=metadata
    )
    
    error_logging_service._logger.info.assert_called_once()
    args = error_logging_service._logger.info.call_args[0]
    assert info_message in args[0]

def test_log_debug(error_logging_service):
    """Test logging a debug message."""
    debug_message = 'Test debug message'
    metadata = {'key': 'value'}
    
    error_logging_service.log_debug(
        message=debug_message,
        metadata=metadata
    )
    
    error_logging_service._logger.debug.assert_called_once()
    args = error_logging_service._logger.debug.call_args[0]
    assert debug_message in args[0]

def test_get_recent_errors(error_logging_service):
    """Test retrieving recent errors."""
    with patch.object(error_logging_service, '_db') as mock_db:
        mock_db.errors.find.return_value = [
            {'message': 'Error 1', 'timestamp': datetime.utcnow()},
            {'message': 'Error 2', 'timestamp': datetime.utcnow()}
        ]
        
        errors = error_logging_service.get_recent_errors(limit=2)
        
        assert len(errors) == 2
        mock_db.errors.find.assert_called_once()

def test_get_error_stats(error_logging_service):
    """Test retrieving error statistics."""
    with patch.object(error_logging_service, '_db') as mock_db:
        mock_db.errors.aggregate.return_value = [
            {'_id': 'TestError', 'count': 5},
            {'_id': 'ValueError', 'count': 3}
        ]
        
        stats = error_logging_service.get_error_stats()
        
        assert len(stats) == 2
        assert sum(item['count'] for item in stats) == 8
        mock_db.errors.aggregate.assert_called_once()

def test_cleanup_old_errors(error_logging_service):
    """Test cleaning up old errors."""
    with patch.object(error_logging_service, '_db') as mock_db:
        mock_db.errors.delete_many.return_value = MagicMock(deleted_count=10)
        
        count = error_logging_service.cleanup_old_errors(days=30)
        
        assert count == 10
        mock_db.errors.delete_many.assert_called_once()

def test_log_error_with_custom_formatter(error_logging_service):
    """Test logging an error with a custom formatter."""
    with patch('logging.Formatter') as mock_formatter:
        error_logging_service.set_formatter(mock_formatter())
        
        error_logging_service.log_error(
            message='Test error',
            error_type='TestError'
        )
        
        error_logging_service._logger.error.assert_called_once()

def test_log_batch_errors(error_logging_service):
    """Test logging multiple errors in batch."""
    errors = [
        {'message': 'Error 1', 'type': 'TestError1'},
        {'message': 'Error 2', 'type': 'TestError2'},
        {'message': 'Error 3', 'type': 'TestError3'}
    ]
    
    error_logging_service.log_batch_errors(errors)
    
    assert error_logging_service._logger.error.call_count == len(errors)
    calls = [call(f"{error['type']}: {error['message']}") for error in errors]
    error_logging_service._logger.error.assert_has_calls(calls)

def test_error_context_manager(error_logging_service):
    """Test using error logging service as a context manager."""
    with error_logging_service.error_context(
        user_id='12345',
        request_id='req-123'
    ):
        raise ValueError('Test error')
    
    error_logging_service._logger.exception.assert_called_once()
    args = error_logging_service._logger.exception.call_args[0]
    assert 'Test error' in args[0]

def test_log_error_with_tags(error_logging_service):
    """Test logging an error with tags."""
    tags = ['critical', 'security', 'auth']
    
    error_logging_service.log_error(
        message='Test error',
        error_type='TestError',
        tags=tags
    )
    
    error_logging_service._logger.error.assert_called_once()
    args = error_logging_service._logger.error.call_args[0]
    assert all(tag in args[0] for tag in tags)

def test_get_errors_by_type(error_logging_service):
    """Test retrieving errors by type."""
    error_type = 'TestError'
    
    with patch.object(error_logging_service, '_db') as mock_db:
        mock_db.errors.find.return_value = [
            {'message': 'Error 1', 'type': error_type},
            {'message': 'Error 2', 'type': error_type}
        ]
        
        errors = error_logging_service.get_errors_by_type(error_type)
        
        assert len(errors) == 2
        assert all(error['type'] == error_type for error in errors)
        mock_db.errors.find.assert_called_once_with({'type': error_type}) 