import pytest
from datetime import datetime, timedelta
from services.priority_queue_service import PriorityQueueService, PriorityLevel, QueuedCase

@pytest.fixture
def queue_service():
    """Create a fresh priority queue service for each test"""
    service = PriorityQueueService()
    service.queue = []  # Clear any existing cases
    service.case_lookup = {}
    return service

def test_add_case(queue_service):
    """Test adding a case to the queue"""
    case = queue_service.add_case(
        case_id="TEST-001",
        priority="HIGH",
        user_id="user123",
        situation_type="police",
        metadata={"description": "Test case"}
    )
    
    assert case.case_id == "TEST-001"
    assert case.priority == PriorityLevel.HIGH
    assert case.user_id == "user123"
    assert len(queue_service.queue) == 1
    assert "TEST-001" in queue_service.case_lookup

def test_priority_ordering(queue_service):
    """Test that cases are ordered correctly by priority"""
    # Add cases in non-priority order
    queue_service.add_case("TEST-001", "LOW", "user1", "other", {})
    queue_service.add_case("TEST-002", "URGENT", "user2", "police", {})
    queue_service.add_case("TEST-003", "MEDIUM", "user3", "court", {})
    
    # Check ordering
    next_case = queue_service.get_next_case()
    assert next_case.case_id == "TEST-002"  # URGENT should be first
    assert next_case.priority == PriorityLevel.URGENT

def test_fifo_within_priority(queue_service):
    """Test FIFO ordering within same priority level"""
    # Add cases with same priority
    queue_service.add_case("TEST-001", "HIGH", "user1", "rights", {})
    queue_service.add_case("TEST-002", "HIGH", "user2", "rights", {})
    
    # First case added should be first in queue
    position1 = queue_service.get_queue_position("TEST-001")
    position2 = queue_service.get_queue_position("TEST-002")
    assert position1 < position2

def test_update_priority(queue_service):
    """Test updating case priority"""
    case = queue_service.add_case("TEST-001", "LOW", "user1", "other", {})
    updated_case = queue_service.update_priority("TEST-001", "HIGH")
    
    assert updated_case.priority == PriorityLevel.HIGH
    assert queue_service.get_next_case().case_id == "TEST-001"

def test_assign_case(queue_service):
    """Test assigning a case to a lawyer"""
    queue_service.add_case("TEST-001", "HIGH", "user1", "rights", {})
    assigned_case = queue_service.assign_case("TEST-001", "LAWYER-001")
    
    assert assigned_case.assigned_lawyer_id == "LAWYER-001"
    assert "TEST-001" not in queue_service.case_lookup
    assert len(queue_service.queue) == 0

def test_wait_time_calculation(queue_service):
    """Test wait time estimation"""
    # Add cases with different priorities
    queue_service.add_case("TEST-001", "URGENT", "user1", "police", {})
    queue_service.add_case("TEST-002", "HIGH", "user2", "rights", {})
    queue_service.add_case("TEST-003", "LOW", "user3", "other", {})
    
    # Check wait times
    wait_time = queue_service.get_estimated_wait_time("TEST-003")  # LOW priority case
    assert wait_time > timedelta(minutes=15)  # Should wait for URGENT and HIGH cases

def test_queue_status(queue_service):
    """Test queue status reporting"""
    queue_service.add_case("TEST-001", "URGENT", "user1", "police", {})
    queue_service.add_case("TEST-002", "HIGH", "user2", "rights", {})
    
    status = queue_service.get_queue_status()
    assert status["total_cases"] == 2
    assert status["priority_breakdown"]["URGENT"] == 1
    assert status["priority_breakdown"]["HIGH"] == 1
    assert status["next_case"] == "TEST-001"

def test_invalid_priority(queue_service):
    """Test handling of invalid priority levels"""
    with pytest.raises(ValueError):
        queue_service.add_case("TEST-001", "INVALID", "user1", "other", {})

def test_case_not_found(queue_service):
    """Test handling of non-existent cases"""
    assert queue_service.get_queue_position("NONEXISTENT") is None
    assert queue_service.assign_case("NONEXISTENT", "LAWYER-001") is None
    assert queue_service.update_priority("NONEXISTENT", "HIGH") is None 