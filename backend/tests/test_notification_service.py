import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from bson import ObjectId
from services.notification_service import NotificationService
from services.websocket_service import WebSocketService

@pytest.fixture
def notification_service():
    """Create a notification service instance with mocked dependencies."""
    with patch('services.notification_service.WebSocketService') as mock_ws, \
         patch('services.notification_service.get_redis') as mock_redis:
        mock_redis.return_value = MagicMock()
        service = NotificationService()
        yield service

@pytest.fixture
def sample_notification():
    """Create a sample notification object."""
    return {
        '_id': str(ObjectId()),
        'user_id': str(ObjectId()),
        'title': 'Test Notification',
        'message': 'This is a test notification',
        'type': 'info',
        'category': 'test',
        'isRead': False,
        'createdAt': datetime.utcnow(),
        'metadata': {
            'link': '/test',
            'action': 'view'
        }
    }

def test_create_notification(notification_service, sample_notification):
    """Test creating a new notification."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.insert_one.return_value = MagicMock(
            inserted_id=ObjectId(sample_notification['_id'])
        )
        
        result = notification_service.create_notification(
            user_id=sample_notification['user_id'],
            title=sample_notification['title'],
            message=sample_notification['message'],
            type=sample_notification['type'],
            category=sample_notification['category'],
            metadata=sample_notification['metadata']
        )
        
        assert result == sample_notification['_id']
        mock_db.notifications.insert_one.assert_called_once()

def test_get_user_notifications(notification_service, sample_notification):
    """Test retrieving user notifications."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.find.return_value = [sample_notification]
        
        notifications = notification_service.get_user_notifications(
            user_id=sample_notification['user_id']
        )
        
        assert len(notifications) == 1
        assert notifications[0]['title'] == sample_notification['title']
        mock_db.notifications.find.assert_called_once()

def test_mark_notification_as_read(notification_service, sample_notification):
    """Test marking a notification as read."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.update_one.return_value = MagicMock(modified_count=1)
        
        success = notification_service.mark_as_read(
            notification_id=sample_notification['_id'],
            user_id=sample_notification['user_id']
        )
        
        assert success is True
        mock_db.notifications.update_one.assert_called_once()

def test_mark_all_notifications_as_read(notification_service, sample_notification):
    """Test marking all notifications as read for a user."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.update_many.return_value = MagicMock(modified_count=5)
        
        count = notification_service.mark_all_as_read(
            user_id=sample_notification['user_id']
        )
        
        assert count == 5
        mock_db.notifications.update_many.assert_called_once()

def test_delete_notification(notification_service, sample_notification):
    """Test deleting a notification."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.delete_one.return_value = MagicMock(deleted_count=1)
        
        success = notification_service.delete_notification(
            notification_id=sample_notification['_id'],
            user_id=sample_notification['user_id']
        )
        
        assert success is True
        mock_db.notifications.delete_one.assert_called_once()

def test_get_unread_count(notification_service, sample_notification):
    """Test getting unread notification count."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.count_documents.return_value = 3
        
        count = notification_service.get_unread_count(
            user_id=sample_notification['user_id']
        )
        
        assert count == 3
        mock_db.notifications.count_documents.assert_called_once()

def test_broadcast_notification(notification_service):
    """Test broadcasting a notification to multiple users."""
    user_ids = [str(ObjectId()) for _ in range(3)]
    notification_data = {
        'title': 'Broadcast Test',
        'message': 'Test broadcast message',
        'type': 'info'
    }
    
    with patch.object(notification_service, '_db') as mock_db, \
         patch.object(notification_service, '_ws') as mock_ws:
        mock_db.notifications.insert_many.return_value = MagicMock(
            inserted_ids=[ObjectId() for _ in range(3)]
        )
        
        notification_ids = notification_service.broadcast_notification(
            user_ids=user_ids,
            **notification_data
        )
        
        assert len(notification_ids) == 3
        mock_db.notifications.insert_many.assert_called_once()
        assert mock_ws.broadcast_to_users.call_count == 1

def test_cleanup_old_notifications(notification_service):
    """Test cleaning up old notifications."""
    days_old = 30
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.delete_many.return_value = MagicMock(deleted_count=10)
        
        count = notification_service.cleanup_old_notifications(days=days_old)
        
        assert count == 10
        mock_db.notifications.delete_many.assert_called_once()

def test_get_notification_stats(notification_service):
    """Test getting notification statistics."""
    with patch.object(notification_service, '_db') as mock_db:
        mock_db.notifications.aggregate.return_value = [
            {'_id': 'info', 'count': 5},
            {'_id': 'warning', 'count': 3},
            {'_id': 'error', 'count': 2}
        ]
        
        stats = notification_service.get_notification_stats()
        
        assert len(stats) == 3
        assert sum(item['count'] for item in stats) == 10
        mock_db.notifications.aggregate.assert_called_once()

def test_get_user_notification_preferences(notification_service):
    """Test getting user notification preferences."""
    user_id = str(ObjectId())
    default_preferences = {
        'email': True,
        'push': True,
        'sms': False
    }
    
    with patch.object(notification_service, '_redis') as mock_redis:
        mock_redis.hgetall.return_value = {
            'email': '1',
            'push': '1',
            'sms': '0'
        }
        
        preferences = notification_service.get_user_preferences(user_id)
        
        assert preferences == default_preferences
        mock_redis.hgetall.assert_called_once()

def test_update_user_notification_preferences(notification_service):
    """Test updating user notification preferences."""
    user_id = str(ObjectId())
    preferences = {
        'email': False,
        'push': True,
        'sms': True
    }
    
    with patch.object(notification_service, '_redis') as mock_redis:
        success = notification_service.update_user_preferences(
            user_id=user_id,
            preferences=preferences
        )
        
        assert success is True
        assert mock_redis.hmset.call_count == 1

def test_invalid_notification_type(notification_service):
    """Test creating a notification with invalid type."""
    with pytest.raises(ValueError):
        notification_service.create_notification(
            user_id=str(ObjectId()),
            title='Test',
            message='Test message',
            type='invalid_type'
        )

def test_invalid_user_id(notification_service):
    """Test operations with invalid user ID."""
    with pytest.raises(ValueError):
        notification_service.get_user_notifications(user_id='invalid_id') 