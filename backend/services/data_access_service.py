"""
Data access auditing service for tracking data modifications and access patterns.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from flask import request, g, current_app
from database import db
from models.audit import AuditLog, AuditEventType, AuditSeverity
from services.audit_service import audit_service

logger = logging.getLogger(__name__)

class DataAccessService:
    """Service for auditing data access and modifications."""
    
    def __init__(self):
        self.access_patterns = {}
        self.modification_history = {}
        self.sensitive_data_access = {}
    
    def log_data_access(
        self,
        user_id: int,
        resource_type: str,
        resource_id: str,
        action: str,
        data_fields: Optional[List[str]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        result_count: int = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log data access event."""
        try:
            # Determine if this is sensitive data access
            is_sensitive = self._is_sensitive_data_access(resource_type, data_fields)
            
            # Log the access event
            audit_log = audit_service.log_audit_event(
                event_type=AuditEventType.DATA_ACCESS,
                action=action,
                user_id=user_id,
                resource_id=resource_id,
                resource_type=resource_type,
                description=f"Data access: {action} on {resource_type}",
                severity=AuditSeverity.MEDIUM if is_sensitive else AuditSeverity.LOW,
                metadata={
                    "data_fields": data_fields,
                    "query_params": query_params,
                    "result_count": result_count,
                    "is_sensitive": is_sensitive,
                    **(metadata or {})
                }
            )
            
            # Track access patterns
            self._track_access_pattern(user_id, resource_type, action, is_sensitive)
            
            # Log sensitive data access separately
            if is_sensitive:
                self._log_sensitive_data_access(user_id, resource_type, resource_id, action, data_fields)
            
            return audit_log
            
        except Exception as e:
            logger.error(f"Error logging data access: {str(e)}")
            raise
    
    def log_data_modification(
        self,
        user_id: int,
        resource_type: str,
        resource_id: str,
        action: str,
        old_data: Optional[Dict[str, Any]] = None,
        new_data: Optional[Dict[str, Any]] = None,
        changed_fields: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log data modification event."""
        try:
            # Determine severity based on action and data sensitivity
            severity = self._get_modification_severity(action, resource_type, changed_fields)
            
            # Calculate changes
            changes = self._calculate_changes(old_data, new_data, changed_fields)
            
            # Log the modification event
            audit_log = audit_service.log_audit_event(
                event_type=AuditEventType.DATA_MODIFICATION,
                action=action,
                user_id=user_id,
                resource_id=resource_id,
                resource_type=resource_type,
                description=f"Data modification: {action} on {resource_type}",
                severity=severity,
                metadata={
                    "old_data": old_data,
                    "new_data": new_data,
                    "changed_fields": changed_fields,
                    "changes": changes,
                    "change_count": len(changes) if changes else 0,
                    **(metadata or {})
                }
            )
            
            # Track modification history
            self._track_modification_history(user_id, resource_type, resource_id, action, changes)
            
            # Check for suspicious modifications
            self._check_suspicious_modifications(user_id, resource_type, action, changes)
            
            return audit_log
            
        except Exception as e:
            logger.error(f"Error logging data modification: {str(e)}")
            raise
    
    def log_bulk_operation(
        self,
        user_id: int,
        operation_type: str,
        resource_type: str,
        affected_count: int,
        operation_details: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log bulk data operations."""
        try:
            # Determine severity based on operation type and count
            severity = self._get_bulk_operation_severity(operation_type, affected_count)
            
            # Log the bulk operation
            audit_log = audit_service.log_audit_event(
                event_type=AuditEventType.DATA_MODIFICATION,
                action=f"BULK_{operation_type.upper()}",
                user_id=user_id,
                resource_type=resource_type,
                description=f"Bulk operation: {operation_type} on {affected_count} {resource_type} records",
                severity=severity,
                metadata={
                    "operation_type": operation_type,
                    "affected_count": affected_count,
                    "operation_details": operation_details,
                    **(metadata or {})
                }
            )
            
            # Track bulk operations
            self._track_bulk_operation(user_id, operation_type, resource_type, affected_count)
            
            return audit_log
            
        except Exception as e:
            logger.error(f"Error logging bulk operation: {str(e)}")
            raise
    
    def log_data_export(
        self,
        user_id: int,
        export_type: str,
        resource_type: str,
        record_count: int,
        export_format: str,
        export_fields: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log data export events."""
        try:
            # Determine if this is sensitive data export
            is_sensitive = self._is_sensitive_data_export(export_fields)
            
            # Log the export event
            audit_log = audit_service.log_audit_event(
                event_type=AuditEventType.DATA_ACCESS,
                action="EXPORT",
                user_id=user_id,
                resource_type=resource_type,
                description=f"Data export: {export_type} of {record_count} {resource_type} records",
                severity=AuditSeverity.HIGH if is_sensitive else AuditSeverity.MEDIUM,
                metadata={
                    "export_type": export_type,
                    "record_count": record_count,
                    "export_format": export_format,
                    "export_fields": export_fields,
                    "is_sensitive": is_sensitive,
                    **(metadata or {})
                }
            )
            
            # Track data exports
            self._track_data_export(user_id, export_type, resource_type, record_count, is_sensitive)
            
            return audit_log
            
        except Exception as e:
            logger.error(f"Error logging data export: {str(e)}")
            raise
    
    def log_data_deletion(
        self,
        user_id: int,
        resource_type: str,
        resource_id: str,
        deletion_reason: str = None,
        soft_delete: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """Log data deletion events."""
        try:
            # Log the deletion event
            audit_log = audit_service.log_audit_event(
                event_type=AuditEventType.DATA_MODIFICATION,
                action="DELETE",
                user_id=user_id,
                resource_id=resource_id,
                resource_type=resource_type,
                description=f"Data deletion: {resource_type} record deleted",
                severity=AuditSeverity.HIGH,
                metadata={
                    "deletion_reason": deletion_reason,
                    "soft_delete": soft_delete,
                    **(metadata or {})
                }
            )
            
            # Track deletions
            self._track_data_deletion(user_id, resource_type, resource_id, soft_delete)
            
            return audit_log
            
        except Exception as e:
            logger.error(f"Error logging data deletion: {str(e)}")
            raise
    
    def get_data_access_summary(
        self,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get summary of data access patterns."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Build query filters
            filters = {
                "start_date": start_date,
                "limit": 1000
            }
            
            if user_id:
                filters["user_id"] = user_id
            
            # Get audit logs
            logs = audit_service.get_audit_logs(
                event_type=AuditEventType.DATA_ACCESS,
                **filters
            )
            
            # Filter by resource type if specified
            if resource_type:
                logs = [log for log in logs if log.resource_type == resource_type]
            
            # Analyze access patterns
            summary = {
                "user_id": user_id,
                "resource_type": resource_type,
                "period_days": days,
                "total_access_events": len(logs),
                "access_by_action": {},
                "access_by_resource_type": {},
                "access_by_user": {},
                "sensitive_data_access": 0,
                "most_accessed_resources": {},
                "access_timeline": [],
                "peak_access_hours": [],
                "access_patterns": {}
            }
            
            hourly_access = {}
            
            for log in logs:
                # Count by action
                action = log.action
                summary["access_by_action"][action] = summary["access_by_action"].get(action, 0) + 1
                
                # Count by resource type
                resource_type = log.resource_type
                if resource_type:
                    summary["access_by_resource_type"][resource_type] = summary["access_by_resource_type"].get(resource_type, 0) + 1
                
                # Count by user
                user_id = log.user_id
                if user_id:
                    summary["access_by_user"][user_id] = summary["access_by_user"].get(user_id, 0) + 1
                
                # Check for sensitive data access
                metadata = log.metadata_dict
                if metadata and metadata.get("is_sensitive", False):
                    summary["sensitive_data_access"] += 1
                
                # Track most accessed resources
                resource_id = log.resource_id
                if resource_id:
                    key = f"{resource_type}:{resource_id}"
                    summary["most_accessed_resources"][key] = summary["most_accessed_resources"].get(key, 0) + 1
                
                # Track access timeline
                summary["access_timeline"].append({
                    "timestamp": log.created_at.isoformat(),
                    "action": action,
                    "resource_type": resource_type,
                    "resource_id": resource_id,
                    "user_id": user_id
                })
                
                # Track hourly access
                hour = log.created_at.hour
                hourly_access[hour] = hourly_access.get(hour, 0) + 1
            
            # Find peak access hours
            if hourly_access:
                peak_hour = max(hourly_access, key=hourly_access.get)
                summary["peak_access_hours"] = [hour for hour, count in hourly_access.items() if count >= hourly_access[peak_hour] * 0.8]
            
            # Sort dictionaries by count
            summary["access_by_action"] = dict(sorted(summary["access_by_action"].items(), key=lambda x: x[1], reverse=True))
            summary["access_by_resource_type"] = dict(sorted(summary["access_by_resource_type"].items(), key=lambda x: x[1], reverse=True))
            summary["most_accessed_resources"] = dict(sorted(summary["most_accessed_resources"].items(), key=lambda x: x[1], reverse=True)[:20])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data access summary: {str(e)}")
            return {"error": str(e)}
    
    def get_data_modification_summary(
        self,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get summary of data modification patterns."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Build query filters
            filters = {
                "start_date": start_date,
                "limit": 1000
            }
            
            if user_id:
                filters["user_id"] = user_id
            
            # Get audit logs
            logs = audit_service.get_audit_logs(
                event_type=AuditEventType.DATA_MODIFICATION,
                **filters
            )
            
            # Filter by resource type if specified
            if resource_type:
                logs = [log for log in logs if log.resource_type == resource_type]
            
            # Analyze modification patterns
            summary = {
                "user_id": user_id,
                "resource_type": resource_type,
                "period_days": days,
                "total_modifications": len(logs),
                "modifications_by_action": {},
                "modifications_by_resource_type": {},
                "modifications_by_user": {},
                "bulk_operations": 0,
                "deletions": 0,
                "most_modified_resources": {},
                "modification_timeline": [],
                "change_statistics": {
                    "total_changes": 0,
                    "average_changes_per_modification": 0,
                    "fields_most_commonly_changed": {}
                }
            }
            
            total_changes = 0
            field_change_counts = {}
            
            for log in logs:
                # Count by action
                action = log.action
                summary["modifications_by_action"][action] = summary["modifications_by_action"].get(action, 0) + 1
                
                # Count by resource type
                resource_type = log.resource_type
                if resource_type:
                    summary["modifications_by_resource_type"][resource_type] = summary["modifications_by_resource_type"].get(resource_type, 0) + 1
                
                # Count by user
                user_id = log.user_id
                if user_id:
                    summary["modifications_by_user"][user_id] = summary["modifications_by_user"].get(user_id, 0) + 1
                
                # Count specific operations
                if action.startswith("BULK_"):
                    summary["bulk_operations"] += 1
                elif action == "DELETE":
                    summary["deletions"] += 1
                
                # Track most modified resources
                resource_id = log.resource_id
                if resource_id:
                    key = f"{resource_type}:{resource_id}"
                    summary["most_modified_resources"][key] = summary["most_modified_resources"].get(key, 0) + 1
                
                # Track modification timeline
                summary["modification_timeline"].append({
                    "timestamp": log.created_at.isoformat(),
                    "action": action,
                    "resource_type": resource_type,
                    "resource_id": resource_id,
                    "user_id": user_id
                })
                
                # Analyze changes
                metadata = log.metadata_dict
                if metadata:
                    change_count = metadata.get("change_count", 0)
                    total_changes += change_count
                    
                    changed_fields = metadata.get("changed_fields", [])
                    for field in changed_fields:
                        field_change_counts[field] = field_change_counts.get(field, 0) + 1
            
            # Calculate change statistics
            summary["change_statistics"]["total_changes"] = total_changes
            if len(logs) > 0:
                summary["change_statistics"]["average_changes_per_modification"] = total_changes / len(logs)
            summary["change_statistics"]["fields_most_commonly_changed"] = dict(sorted(field_change_counts.items(), key=lambda x: x[1], reverse=True)[:20])
            
            # Sort dictionaries by count
            summary["modifications_by_action"] = dict(sorted(summary["modifications_by_action"].items(), key=lambda x: x[1], reverse=True))
            summary["modifications_by_resource_type"] = dict(sorted(summary["modifications_by_resource_type"].items(), key=lambda x: x[1], reverse=True))
            summary["most_modified_resources"] = dict(sorted(summary["most_modified_resources"].items(), key=lambda x: x[1], reverse=True)[:20])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data modification summary: {str(e)}")
            return {"error": str(e)}
    
    def _is_sensitive_data_access(self, resource_type: str, data_fields: Optional[List[str]]) -> bool:
        """Check if this is access to sensitive data."""
        sensitive_fields = [
            'password', 'ssn', 'credit_card', 'bank_account', 'api_key',
            'token', 'secret', 'personal_id', 'phone', 'address'
        ]
        
        if not data_fields:
            return False
        
        return any(field.lower() in sensitive_fields for field in data_fields)
    
    def _is_sensitive_data_export(self, export_fields: Optional[List[str]]) -> bool:
        """Check if this is export of sensitive data."""
        return self._is_sensitive_data_access("export", export_fields)
    
    def _get_modification_severity(self, action: str, resource_type: str, changed_fields: Optional[List[str]]) -> AuditSeverity:
        """Determine severity of data modification."""
        if action == "DELETE":
            return AuditSeverity.HIGH
        elif action.startswith("BULK_"):
            return AuditSeverity.HIGH
        elif self._is_sensitive_data_access(resource_type, changed_fields):
            return AuditSeverity.HIGH
        elif action in ["UPDATE", "MODIFY"]:
            return AuditSeverity.MEDIUM
        else:
            return AuditSeverity.LOW
    
    def _get_bulk_operation_severity(self, operation_type: str, affected_count: int) -> AuditSeverity:
        """Determine severity of bulk operation."""
        if operation_type.upper() == "DELETE":
            return AuditSeverity.CRITICAL
        elif affected_count > 1000:
            return AuditSeverity.HIGH
        elif affected_count > 100:
            return AuditSeverity.MEDIUM
        else:
            return AuditSeverity.LOW
    
    def _calculate_changes(self, old_data: Optional[Dict[str, Any]], new_data: Optional[Dict[str, Any]], changed_fields: Optional[List[str]]) -> Optional[Dict[str, Any]]:
        """Calculate changes between old and new data."""
        if not old_data or not new_data:
            return None
        
        changes = {}
        
        if changed_fields:
            for field in changed_fields:
                if field in old_data and field in new_data:
                    changes[field] = {
                        "old_value": old_data[field],
                        "new_value": new_data[field]
                    }
        else:
            # Compare all fields
            all_fields = set(old_data.keys()) | set(new_data.keys())
            for field in all_fields:
                old_value = old_data.get(field)
                new_value = new_data.get(field)
                if old_value != new_value:
                    changes[field] = {
                        "old_value": old_value,
                        "new_value": new_value
                    }
        
        return changes
    
    def _track_access_pattern(self, user_id: int, resource_type: str, action: str, is_sensitive: bool):
        """Track user access patterns."""
        try:
            key = f"{user_id}_{resource_type}"
            if key not in self.access_patterns:
                self.access_patterns[key] = {
                    "total_access": 0,
                    "sensitive_access": 0,
                    "actions": {},
                    "last_access": None
                }
            
            pattern = self.access_patterns[key]
            pattern["total_access"] += 1
            pattern["actions"][action] = pattern["actions"].get(action, 0) + 1
            pattern["last_access"] = datetime.utcnow()
            
            if is_sensitive:
                pattern["sensitive_access"] += 1
            
        except Exception as e:
            logger.error(f"Error tracking access pattern: {str(e)}")
    
    def _track_modification_history(self, user_id: int, resource_type: str, resource_id: str, action: str, changes: Optional[Dict[str, Any]]):
        """Track modification history."""
        try:
            key = f"{user_id}_{resource_type}_{resource_id}"
            if key not in self.modification_history:
                self.modification_history[key] = []
            
            self.modification_history[key].append({
                "timestamp": datetime.utcnow(),
                "action": action,
                "changes": changes
            })
            
            # Keep only last 50 modifications per resource
            if len(self.modification_history[key]) > 50:
                self.modification_history[key] = self.modification_history[key][-50:]
            
        except Exception as e:
            logger.error(f"Error tracking modification history: {str(e)}")
    
    def _log_sensitive_data_access(self, user_id: int, resource_type: str, resource_id: str, action: str, data_fields: Optional[List[str]]):
        """Log sensitive data access separately."""
        try:
            key = f"{user_id}_{resource_type}"
            if key not in self.sensitive_data_access:
                self.sensitive_data_access[key] = []
            
            self.sensitive_data_access[key].append({
                "timestamp": datetime.utcnow(),
                "resource_id": resource_id,
                "action": action,
                "data_fields": data_fields
            })
            
            # Keep only last 100 sensitive accesses per user/resource type
            if len(self.sensitive_data_access[key]) > 100:
                self.sensitive_data_access[key] = self.sensitive_data_access[key][-100:]
            
        except Exception as e:
            logger.error(f"Error logging sensitive data access: {str(e)}")
    
    def _track_bulk_operation(self, user_id: int, operation_type: str, resource_type: str, affected_count: int):
        """Track bulk operations."""
        try:
            # This could be extended to track bulk operation patterns
            # and detect potential abuse
            pass
        except Exception as e:
            logger.error(f"Error tracking bulk operation: {str(e)}")
    
    def _track_data_export(self, user_id: int, export_type: str, resource_type: str, record_count: int, is_sensitive: bool):
        """Track data exports."""
        try:
            # This could be extended to track export patterns
            # and detect potential data exfiltration
            pass
        except Exception as e:
            logger.error(f"Error tracking data export: {str(e)}")
    
    def _track_data_deletion(self, user_id: int, resource_type: str, resource_id: str, soft_delete: bool):
        """Track data deletions."""
        try:
            # This could be extended to track deletion patterns
            # and detect potential data destruction
            pass
        except Exception as e:
            logger.error(f"Error tracking data deletion: {str(e)}")
    
    def _check_suspicious_modifications(self, user_id: int, resource_type: str, action: str, changes: Optional[Dict[str, Any]]):
        """Check for suspicious modification patterns."""
        try:
            # This could be extended to detect suspicious patterns like:
            # - Mass deletions
            # - Unusual modification times
            # - Modification of critical fields
            # - Rapid successive modifications
            pass
        except Exception as e:
            logger.error(f"Error checking suspicious modifications: {str(e)}")

# Global data access service instance
data_access_service = DataAccessService()
