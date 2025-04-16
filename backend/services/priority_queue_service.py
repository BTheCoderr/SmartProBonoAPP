from datetime import datetime, timedelta
import heapq
import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import threading
import logging
from models.queue_models import queue_db, PriorityLevel

@dataclass
class QueuedCase:
    case_id: str
    priority: PriorityLevel
    timestamp: datetime
    user_id: str
    situation_type: str
    metadata: Dict
    assigned_lawyer_id: Optional[str] = None
    status: str = "pending"  # Default status for new cases
    
    def __lt__(self, other):
        # First compare by priority level
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value
        # Then by timestamp (FIFO within same priority)
        return self.timestamp < other.timestamp

class PriorityQueueService:
    """
    Service for managing the priority queue of cases.
    Uses an in-memory queue with database persistence.
    """
    
    def __init__(self):
        self.data_path = os.path.join('data', 'priority_queue')
        self.queue: List[QueuedCase] = []
        self.case_lookup: Dict[str, QueuedCase] = {}
        self._ensure_directories()
        self._queue_lock = threading.RLock()  # For thread safety
        self._load_queue()
        
        # Cache TTL (in seconds)
        self.cache_ttl = int(os.environ.get('QUEUE_CACHE_TTL', 60))
        self.last_refresh = datetime.now()
        
        # Schedule periodic snapshots for analytics
        self._setup_snapshot_scheduler()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_path, exist_ok=True)
    
    def _setup_snapshot_scheduler(self):
        """Set up scheduler for periodic queue snapshots"""
        try:
            # Import here to avoid issues if package is not installed
            from apscheduler.schedulers.background import BackgroundScheduler
            scheduler = BackgroundScheduler()
            
            # Record a snapshot every hour
            scheduler.add_job(
                queue_db.record_queue_snapshot, 
                'interval', 
                hours=1,
                id='queue_snapshot'
            )
            
            scheduler.start()
            logging.info("Queue snapshot scheduler started")
        except ImportError:
            logging.warning("APScheduler not available. Queue snapshots will not be automated.")
    
    def _refresh_from_db_if_needed(self):
        """Refresh the in-memory queue from the database if the cache has expired"""
        if (datetime.now() - self.last_refresh).total_seconds() > self.cache_ttl:
            self._load_queue_from_db()
            self.last_refresh = datetime.now()
    
    def _load_queue(self):
        """Load queue state from database or fallback to file"""
        with self._queue_lock:
            try:
                # First try loading from database
                self._load_queue_from_db()
                
                # If no cases were loaded and file exists, load from file (migration support)
                if not self.queue and os.path.exists(self._get_queue_file()):
                    self._load_queue_from_file()
                    # If we loaded from file, save to DB for migration
                    if self.queue:
                        self._save_queue_to_db()
            except Exception as e:
                logging.error(f"Error loading queue: {str(e)}")
                # Fallback to file-based storage
                self._load_queue_from_file()
    
    def _get_queue_file(self) -> str:
        """Get path to queue state file"""
        return os.path.join(self.data_path, 'queue_state.json')
    
    def _load_queue_from_db(self):
        """Load queue state from database"""
        active_cases = queue_db.get_active_cases()
        
        self.queue = []
        self.case_lookup = {}
        
        for case_data in active_cases:
            try:
                metadata = json.loads(case_data['metadata']) if case_data['metadata'] else {}
                timestamp = datetime.fromisoformat(case_data['timestamp'])
                
                case = QueuedCase(
                    case_id=case_data['case_id'],
                    priority=PriorityLevel[case_data['priority']],
                    timestamp=timestamp,
                    user_id=case_data['user_id'],
                    situation_type=case_data['situation_type'],
                    metadata=metadata,
                    assigned_lawyer_id=case_data.get('assigned_lawyer_id'),
                    status=case_data.get('status', 'pending')
                )
                heapq.heappush(self.queue, case)
                self.case_lookup[case.case_id] = case
            except (KeyError, ValueError) as e:
                logging.error(f"Error loading case {case_data.get('case_id')}: {str(e)}")
    
    def _load_queue_from_file(self):
        """Load queue state from file (legacy support)"""
        try:
            with open(self._get_queue_file(), 'r') as f:
                queue_data = json.load(f)
                
            self.queue = []
            self.case_lookup = {}
            
            for case_data in queue_data:
                try:
                    case = QueuedCase(
                        case_id=case_data['case_id'],
                        priority=PriorityLevel[case_data['priority']],
                        timestamp=datetime.fromisoformat(case_data['timestamp']),
                        user_id=case_data['user_id'],
                        situation_type=case_data['situation_type'],
                        metadata=case_data['metadata'],
                        assigned_lawyer_id=case_data.get('assigned_lawyer_id'),
                        status=case_data.get('status', 'pending')
                    )
                    heapq.heappush(self.queue, case)
                    self.case_lookup[case.case_id] = case
                except (KeyError, ValueError) as e:
                    logging.error(f"Error loading case from file: {str(e)}")
        except FileNotFoundError:
            # Initialize empty queue if no state file exists
            self.queue = []
            self.case_lookup = {}
    
    def _save_queue_to_db(self):
        """Save all active cases to the database"""
        for case in self.queue:
            queue_db.add_case(
                case_id=case.case_id,
                priority=case.priority,
                timestamp=case.timestamp,
                user_id=case.user_id,
                situation_type=case.situation_type,
                metadata=case.metadata,
                assigned_lawyer_id=case.assigned_lawyer_id,
                status=case.status
            )
    
    def add_case(self, case_id: str, priority: str, user_id: str,
                 situation_type: str, metadata: Dict, status: str = "pending") -> QueuedCase:
        """Add a new case to the priority queue"""
        with self._queue_lock:
            try:
                priority_level = PriorityLevel[priority.upper()]
            except KeyError:
                raise ValueError(f"Invalid priority level: {priority}")
            
            timestamp = datetime.now()
            
            # First add to the database for persistence
            queue_db.add_case(
                case_id=case_id,
                priority=priority_level,
                timestamp=timestamp,
                user_id=user_id,
                situation_type=situation_type,
                metadata=metadata,
                status=status
            )
            
            # Then update in-memory queue
            case = QueuedCase(
                case_id=case_id,
                priority=priority_level,
                timestamp=timestamp,
                user_id=user_id,
                situation_type=situation_type,
                metadata=metadata,
                status=status
            )
            
            heapq.heappush(self.queue, case)
            self.case_lookup[case_id] = case
            
            return case
    
    def get_next_case(self) -> Optional[QueuedCase]:
        """Get the next highest priority case from the queue"""
        self._refresh_from_db_if_needed()
        
        with self._queue_lock:
            if not self.queue:
                return None
                
            return self.queue[0]  # Peek without removing
    
    def assign_case(self, case_id: str, lawyer_id: str) -> Optional[QueuedCase]:
        """Assign a case to a lawyer and remove it from the queue"""
        with self._queue_lock:
            # First update the database
            db_success = queue_db.assign_case(case_id, lawyer_id)
            
            # Then update in-memory queue if DB update was successful
            case = self.case_lookup.get(case_id)
            if case and db_success:
                # Remove from queue and lookup
                self.queue.remove(case)
                heapq.heapify(self.queue)  # Restore heap property
                del self.case_lookup[case_id]
                
                # Update assignment for return value
                case.assigned_lawyer_id = lawyer_id
                return case
            elif db_success:
                # Case was in DB but not in memory, refresh from DB
                self._load_queue_from_db()
                
                # Create a return object with available information
                return QueuedCase(
                    case_id=case_id,
                    priority=PriorityLevel.MEDIUM,  # Default, actual value doesn't matter here
                    timestamp=datetime.now(),
                    user_id="",  # We don't have this info
                    situation_type="",  # We don't have this info
                    metadata={},
                    assigned_lawyer_id=lawyer_id
                )
            
            return None
    
    def update_priority(self, case_id: str, new_priority: str) -> Optional[QueuedCase]:
        """Update the priority of a case in the queue"""
        with self._queue_lock:
            try:
                new_priority_level = PriorityLevel[new_priority.upper()]
            except KeyError:
                raise ValueError(f"Invalid priority level: {new_priority}")
            
            # First update in the database
            db_success = queue_db.update_case_priority(case_id, new_priority_level)
            
            # Then update in-memory queue
            case = self.case_lookup.get(case_id)
            if case and db_success:
                # Remove from queue
                self.queue.remove(case)
                
                # Update priority and reinsert
                case.priority = new_priority_level
                heapq.heappush(self.queue, case)
                
                return case
            elif db_success:
                # Case was in DB but not in memory, refresh from DB
                self._load_queue_from_db()
                return self.case_lookup.get(case_id)
            
            return None
    
    def get_queue_position(self, case_id: str) -> Optional[int]:
        """Get the position of a case in the queue"""
        self._refresh_from_db_if_needed()
        
        with self._queue_lock:
            case = self.case_lookup.get(case_id)
            if not case:
                return None
                
            return self.queue.index(case) + 1
    
    def get_estimated_wait_time(self, case_id: str) -> Optional[timedelta]:
        """
        Estimate wait time for a case based on multiple factors:
        1. Position in queue
        2. Priority level
        3. Number of available lawyers
        4. Historical handling times
        5. Time of day and day of week
        """
        self._refresh_from_db_if_needed()
        
        position = self.get_queue_position(case_id)
        if not position:
            return None
            
        case = self.case_lookup[case_id]
        
        # Base handling times (in minutes) based on priority and complexity
        base_handling_times = {
            PriorityLevel.URGENT: {
                'police': 15,
                'rights': 20,
                'other': 25
            },
            PriorityLevel.HIGH: {
                'eviction': 30,
                'housing': 35,
                'rights': 30,
                'other': 40
            },
            PriorityLevel.MEDIUM: {
                'immigration': 45,
                'court': 40,
                'other': 50
            },
            PriorityLevel.LOW: {
                'legal_document': 30,
                'other': 60
            }
        }
        
        # Get base handling time for the case
        situation_type = case.situation_type
        base_time = base_handling_times[case.priority].get(
            situation_type,
            base_handling_times[case.priority]['other']
        )
        
        # Count cases ahead with higher or equal priority
        cases_ahead = sum(1 for c in self.queue[:position] 
                         if c.priority.value >= case.priority.value)
        
        # Time of day adjustment (simplified - could be enhanced with historical data)
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Business hours
            time_factor = 1.0
        elif 17 < current_hour <= 22:  # Evening
            time_factor = 1.5
        else:  # Late night/early morning
            time_factor = 2.0
        
        # Day of week adjustment (simplified)
        day_of_week = datetime.now().weekday()
        if day_of_week < 5:  # Weekday
            day_factor = 1.0
        else:  # Weekend
            day_factor = 1.5
        
        # Calculate estimated wait time
        wait_minutes = (
            base_time * cases_ahead * time_factor * day_factor
        )
        
        # Add uncertainty buffer based on queue length
        uncertainty_factor = 1.1 + (cases_ahead * 0.05)  # 10% base + 5% per case ahead
        wait_minutes *= min(uncertainty_factor, 2.0)  # Cap at 2x
        
        return timedelta(minutes=int(wait_minutes))
    
    def get_queue_status(self) -> Dict:
        """Get current status of the queue"""
        self._refresh_from_db_if_needed()
        
        with self._queue_lock:
            priority_counts = {level: 0 for level in PriorityLevel}
            for case in self.queue:
                priority_counts[case.priority] += 1
                
            return {
                'total_cases': len(self.queue),
                'cases_by_priority': {
                    level.name: priority_counts[level] for level in PriorityLevel
                },
                'average_wait_time': self._calculate_average_wait_time(),
                'longest_waiting_case': self._get_longest_waiting_case_info()
            }
    
    def _calculate_average_wait_time(self) -> Optional[float]:
        """Calculate the average estimated wait time for all cases in queue"""
        if not self.queue:
            return None
            
        wait_times = []
        for case in self.queue:
            wait_time = self.get_estimated_wait_time(case.case_id)
            if wait_time:
                wait_times.append(wait_time.total_seconds() / 60)  # Convert to minutes
                
        if not wait_times:
            return None
            
        return sum(wait_times) / len(wait_times)
    
    def _get_longest_waiting_case_info(self) -> Optional[Dict]:
        """Get information about the case that has been waiting the longest"""
        if not self.queue:
            return None
            
        # Find oldest case by timestamp
        oldest_case = min(self.queue, key=lambda x: x.timestamp)
        wait_time = self.get_estimated_wait_time(oldest_case.case_id)
        position = self.get_queue_position(oldest_case.case_id)
        
        return {
            'case_id': oldest_case.case_id,
            'wait_time': str(datetime.now() - oldest_case.timestamp),
            'estimated_completion': str(wait_time) if wait_time else None,
            'queue_position': position,
            'priority': oldest_case.priority.name
        }
        
    def get_case(self, case_id: str) -> Optional[QueuedCase]:
        """Get a case by ID"""
        self._refresh_from_db_if_needed()
        
        with self._queue_lock:
            return self.case_lookup.get(case_id)
        
    def get_queue_analytics(self) -> Dict:
        """
        Get comprehensive analytics on queue performance 
        - Response time metrics
        - Priority level distributions
        - Case type distributions
        - Wait time statistics
        """
        self._refresh_from_db_if_needed()
        
        with self._queue_lock:
            if not self.queue:
                return {
                    'total_cases': 0,
                    'average_wait_time': None,
                    'priority_distribution': {},
                    'situation_type_distribution': {},
                    'historical_queue_length': [],
                    'average_resolution_time': None,
                    'bottlenecks': []
                }
                
            # Calculate priority distribution
            priority_distribution = {level.name: 0 for level in PriorityLevel}
            for case in self.queue:
                priority_distribution[case.priority.name] += 1
                
            # Calculate situation type distribution
            situation_types = {}
            for case in self.queue:
                situation_type = case.situation_type
                situation_types[situation_type] = situation_types.get(situation_type, 0) + 1
                
            # Calculate wait times
            wait_times = []
            for case in self.queue:
                wait_time = datetime.now() - case.timestamp
                wait_times.append(wait_time.total_seconds() / 60)  # minutes
                
            avg_wait = sum(wait_times) / len(wait_times) if wait_times else None
            max_wait = max(wait_times) if wait_times else None
            min_wait = min(wait_times) if wait_times else None
            
            # Identify bottlenecks (areas with longest wait times)
            bottlenecks = []
            situation_wait_times = {}
            
            for case in self.queue:
                sit_type = case.situation_type
                wait_time = datetime.now() - case.timestamp
                
                if sit_type not in situation_wait_times:
                    situation_wait_times[sit_type] = []
                    
                situation_wait_times[sit_type].append(wait_time.total_seconds() / 60)
                
            for sit_type, times in situation_wait_times.items():
                avg_time = sum(times) / len(times)
                bottlenecks.append({
                    'situation_type': sit_type,
                    'average_wait_minutes': avg_time,
                    'case_count': len(times)
                })
                
            # Sort bottlenecks by average wait time (descending)
            bottlenecks.sort(key=lambda x: x['average_wait_minutes'], reverse=True)
            
            # Get historical queue data
            queue_history = queue_db.get_queue_history(limit=30)
            
            # Get lawyer performance metrics
            lawyer_performance = queue_db.get_lawyer_performance()
            
            return {
                'total_cases': len(self.queue),
                'active_cases': len(self.queue),
                'average_wait_time_minutes': avg_wait,
                'max_wait_time_minutes': max_wait,
                'min_wait_time_minutes': min_wait,
                'priority_distribution': priority_distribution,
                'situation_type_distribution': situation_types,
                'bottlenecks': bottlenecks[:3],  # Top 3 bottlenecks
                'queue_history': queue_history,
                'lawyer_performance': lawyer_performance
            }

# Create a global instance for service locator pattern
priority_queue_service = PriorityQueueService() 