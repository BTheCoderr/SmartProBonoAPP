from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, cast
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.database import db, DatabaseConfig
import logging
from models.queue_models import QueueCase, QueueHistory
from models.queue_models import PriorityLevel

logger = logging.getLogger(__name__)

class QueueDatabase:
    """Database access layer for queue operations."""

    @staticmethod
    def add_case(case_id: str, priority: PriorityLevel, timestamp: datetime,
                user_id: str, situation_type: str, metadata: Dict[str, Any],
                assigned_lawyer_id: Optional[str] = None) -> bool:
        """Add a new case to the queue database.
        
        Returns:
            bool: True if the case was added successfully, False otherwise.
        """
        try:
            session = DatabaseConfig.get_session()
            queue_case = QueueCase(
                case_id=case_id,
                priority=priority.name,
                timestamp=timestamp,
                user_id=user_id,
                situation_type=situation_type,
                metadata=str(metadata),
                assigned_lawyer_id=assigned_lawyer_id,
                status='assigned' if assigned_lawyer_id else 'pending'
            )
            session.add(queue_case)  # type: ignore
            DatabaseConfig.commit_session()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error adding case to queue: {str(e)}")
            DatabaseConfig.get_session().rollback()  # type: ignore
            return False

    @staticmethod
    def get_active_cases() -> List[Dict[str, Any]]:
        """Get all active cases from the queue.
        
        Returns:
            List[Dict[str, Any]]: List of active cases.
        """
        try:
            cases = QueueCase.query.filter(QueueCase.status == 'pending').all()  # type: ignore
            return [case.to_dict() for case in cases]
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving active cases: {str(e)}")
            return []

    @staticmethod
    def assign_case(case_id: str, lawyer_id: str) -> bool:
        """Assign a case to a lawyer.
        
        Returns:
            bool: True if the case was assigned successfully, False otherwise.
        """
        try:
            session = DatabaseConfig.get_session()
            case = QueueCase.query.filter(QueueCase.case_id == case_id).first()  # type: ignore
            if not case:
                return False
                
            case.assigned_lawyer_id = lawyer_id
            case.assigned_at = datetime.utcnow()
            case.status = 'assigned'
            DatabaseConfig.commit_session()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error assigning case: {str(e)}")
            DatabaseConfig.get_session().rollback()  # type: ignore
            return False

    @staticmethod
    def update_case_priority(case_id: str, new_priority: PriorityLevel) -> bool:
        """Update a case's priority.
        
        Returns:
            bool: True if the priority was updated successfully, False otherwise.
        """
        try:
            case = QueueCase.query.filter(QueueCase.case_id == case_id).first()  # type: ignore
            if not case:
                return False

            case.priority = new_priority.name
            DatabaseConfig.commit_session()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating case priority: {str(e)}")
            DatabaseConfig.get_session().rollback()  # type: ignore
            return False

    @staticmethod
    def record_queue_snapshot() -> bool:
        """Record a snapshot of the current queue state for analytics.
        
        Returns:
            bool: True if the snapshot was recorded successfully, False otherwise.
        """
        try:
            session = DatabaseConfig.get_session()
            
            # Count cases by priority
            total_cases = QueueCase.query.filter(QueueCase.status == 'pending').count()  # type: ignore
            urgent_cases = QueueCase.query.filter(QueueCase.status == 'pending', QueueCase.priority == PriorityLevel.URGENT.name).count()  # type: ignore
            high_cases = QueueCase.query.filter(QueueCase.status == 'pending', QueueCase.priority == PriorityLevel.HIGH.name).count()  # type: ignore
            medium_cases = QueueCase.query.filter(QueueCase.status == 'pending', QueueCase.priority == PriorityLevel.MEDIUM.name).count()  # type: ignore
            low_cases = QueueCase.query.filter(QueueCase.status == 'pending', QueueCase.priority == PriorityLevel.LOW.name).count()  # type: ignore
            
            # Calculate average wait time (time since case was added)
            avg_wait_time = None
            oldest_case = QueueCase.query.filter(QueueCase.status == 'pending').order_by(QueueCase.timestamp).first()  # type: ignore
            if oldest_case:
                oldest_time = (datetime.utcnow() - oldest_case.timestamp).total_seconds() / 60  # in minutes
            else:
                oldest_time = 0
                
            snapshot = QueueHistory(
                total_cases=total_cases,
                urgent_cases=urgent_cases,
                high_cases=high_cases,
                medium_cases=medium_cases,
                low_cases=low_cases,
                average_wait_time=avg_wait_time,
                longest_wait_time=oldest_time
            )
            
            session.add(snapshot)  # type: ignore
            DatabaseConfig.commit_session()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error recording queue snapshot: {str(e)}")
            DatabaseConfig.get_session().rollback()  # type: ignore
            return False

    @staticmethod
    def get_queue_history(limit: int = 30) -> List[Dict[str, Any]]:
        """Get queue history snapshots.
        
        Args:
            limit: Maximum number of snapshots to return.
            
        Returns:
            List of queue history snapshots.
        """
        try:
            snapshots = QueueHistory.query.order_by(QueueHistory.timestamp.desc()).limit(limit).all()  # type: ignore
            return [snapshot.to_dict() for snapshot in snapshots]
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving queue history: {str(e)}")
            return []

    @staticmethod
    def get_lawyer_performance() -> List[Dict[str, Any]]:
        """Get performance metrics for lawyers.
        
        Returns:
            List of lawyer performance metrics.
        """
        try:
            # Get all cases that have been assigned or completed
            completed_cases = QueueCase.query.filter(  # type: ignore
                QueueCase.status.in_(['assigned', 'completed'])
            ).all()
            
            # Group by lawyer_id
            lawyer_stats = {}
            for case in completed_cases:
                if case.assigned_lawyer_id not in lawyer_stats:
                    lawyer_stats[case.assigned_lawyer_id] = {
                        'lawyer_id': case.assigned_lawyer_id,
                        'lawyer_name': f"{case.assigned_lawyer.first_name} {case.assigned_lawyer.last_name}" if case.assigned_lawyer else "Unknown",
                        'total_cases': 0,
                        'completed_cases': 0,
                        'avg_resolution_time': 0,
                        'case_priorities': {'URGENT': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
                    }
                
                lawyer_stats[case.assigned_lawyer_id]['total_cases'] += 1
                lawyer_stats[case.assigned_lawyer_id]['case_priorities'][case.priority] += 1
                
                if case.status == 'completed':
                    lawyer_stats[case.assigned_lawyer_id]['completed_cases'] += 1
            
            return list(lawyer_stats.values())
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving lawyer performance: {str(e)}")
            return []

# Create a global instance
queue_db = QueueDatabase() 