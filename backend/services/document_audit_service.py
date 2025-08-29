"""
Document auditing service for tracking document access, modifications, and sharing.
"""
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from flask import request, g, current_app
from database import db
from models.audit import DocumentAudit, AuditEventType, AuditSeverity
from services.audit_service import audit_service
from services.alert_service import alert_service

logger = logging.getLogger(__name__)

class DocumentAuditService:
    """Service for auditing document access and modifications."""
    
    def __init__(self):
        self.document_access_patterns = {}
        self.document_modification_history = {}
        self.document_sharing_records = {}
        self.sensitive_document_types = ['legal_document', 'contract', 'agreement', 'confidential']
    
    def log_document_access(
        self,
        document_id: int,
        user_id: int,
        action: str,
        file_size: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document access event."""
        try:
            # Determine if this is sensitive document access
            is_sensitive = self._is_sensitive_document_access(document_id, action)
            
            # Log document audit
            document_audit = audit_service.log_document_access(
                document_id=document_id,
                user_id=user_id,
                action=action,
                file_size=file_size,
                processing_time_ms=processing_time_ms,
                version=version,
                metadata={
                    "is_sensitive": is_sensitive,
                    **(metadata or {})
                }
            )
            
            # Track document access patterns
            self._track_document_access_pattern(user_id, document_id, action, is_sensitive)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.DOCUMENT_ACCESS,
                action=action.upper(),
                user_id=user_id,
                resource_id=str(document_id),
                resource_type="document",
                description=f"Document {action}: document {document_id}",
                severity=AuditSeverity.HIGH if is_sensitive else AuditSeverity.MEDIUM,
                metadata={
                    "document_id": document_id,
                    "action": action,
                    "file_size": file_size,
                    "processing_time_ms": processing_time_ms,
                    "version": version,
                    "is_sensitive": is_sensitive
                }
            )
            
            # Check for suspicious document access
            self._check_suspicious_document_access(user_id, document_id, action)
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Error logging document access: {str(e)}")
            raise
    
    def log_document_modification(
        self,
        document_id: int,
        user_id: int,
        modification_type: str,
        changes_made: Optional[Dict[str, Any]] = None,
        file_size: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document modification event."""
        try:
            # Log document audit
            document_audit = audit_service.log_document_access(
                document_id=document_id,
                user_id=user_id,
                action=modification_type,
                file_size=file_size,
                processing_time_ms=processing_time_ms,
                version=version,
                changes_made=changes_made,
                metadata=metadata
            )
            
            # Track modification history
            self._track_document_modification_history(user_id, document_id, modification_type, changes_made)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.DOCUMENT_ACCESS,
                action=f"DOCUMENT_{modification_type.upper()}",
                user_id=user_id,
                resource_id=str(document_id),
                resource_type="document",
                description=f"Document {modification_type}: document {document_id}",
                severity=AuditSeverity.HIGH,
                metadata={
                    "document_id": document_id,
                    "modification_type": modification_type,
                    "changes_made": changes_made,
                    "file_size": file_size,
                    "processing_time_ms": processing_time_ms,
                    "version": version
                }
            )
            
            # Check for suspicious modifications
            self._check_suspicious_document_modification(user_id, document_id, modification_type, changes_made)
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Error logging document modification: {str(e)}")
            raise
    
    def log_document_sharing(
        self,
        document_id: int,
        user_id: int,
        shared_with: List[int],
        sharing_method: str = "direct",
        permissions: Optional[List[str]] = None,
        expiration_date: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document sharing event."""
        try:
            # Log document audit
            document_audit = audit_service.log_document_access(
                document_id=document_id,
                user_id=user_id,
                action="share",
                shared_with=shared_with,
                metadata={
                    "sharing_method": sharing_method,
                    "permissions": permissions,
                    "expiration_date": expiration_date.isoformat() if expiration_date else None,
                    "shared_user_count": len(shared_with),
                    **(metadata or {})
                }
            )
            
            # Track sharing records
            self._track_document_sharing_record(user_id, document_id, shared_with, sharing_method, permissions)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.DOCUMENT_ACCESS,
                action="DOCUMENT_SHARE",
                user_id=user_id,
                resource_id=str(document_id),
                resource_type="document",
                description=f"Document shared: document {document_id} with {len(shared_with)} users",
                severity=AuditSeverity.HIGH,
                metadata={
                    "document_id": document_id,
                    "shared_with": shared_with,
                    "sharing_method": sharing_method,
                    "permissions": permissions,
                    "expiration_date": expiration_date.isoformat() if expiration_date else None,
                    "shared_user_count": len(shared_with)
                }
            )
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Error logging document sharing: {str(e)}")
            raise
    
    def log_document_download(
        self,
        document_id: int,
        user_id: int,
        download_format: str = "original",
        file_size: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document download event."""
        try:
            # Log document audit
            document_audit = audit_service.log_document_access(
                document_id=document_id,
                user_id=user_id,
                action="download",
                file_size=file_size,
                processing_time_ms=processing_time_ms,
                version=version,
                metadata={
                    "download_format": download_format,
                    **(metadata or {})
                }
            )
            
            # Track download patterns
            self._track_document_access_pattern(user_id, document_id, "download", False)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.DOCUMENT_ACCESS,
                action="DOCUMENT_DOWNLOAD",
                user_id=user_id,
                resource_id=str(document_id),
                resource_type="document",
                description=f"Document downloaded: document {document_id} in {download_format} format",
                severity=AuditSeverity.MEDIUM,
                metadata={
                    "document_id": document_id,
                    "download_format": download_format,
                    "file_size": file_size,
                    "processing_time_ms": processing_time_ms,
                    "version": version
                }
            )
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Error logging document download: {str(e)}")
            raise
    
    def log_document_deletion(
        self,
        document_id: int,
        user_id: int,
        deletion_reason: str = None,
        soft_delete: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document deletion event."""
        try:
            # Log document audit
            document_audit = audit_service.log_document_access(
                document_id=document_id,
                user_id=user_id,
                action="delete",
                metadata={
                    "deletion_reason": deletion_reason,
                    "soft_delete": soft_delete,
                    **(metadata or {})
                }
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.DOCUMENT_ACCESS,
                action="DOCUMENT_DELETE",
                user_id=user_id,
                resource_id=str(document_id),
                resource_type="document",
                description=f"Document deleted: document {document_id}",
                severity=AuditSeverity.HIGH,
                metadata={
                    "document_id": document_id,
                    "deletion_reason": deletion_reason,
                    "soft_delete": soft_delete
                }
            )
            
            # Send alert for document deletion
            alert_service.send_performance_alert(
                "document_deletion",
                100,  # 100% deletion
                "%",
                f"Document {document_id} deleted"
            )
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Error logging document deletion: {str(e)}")
            raise
    
    def get_document_access_summary(
        self,
        document_id: Optional[int] = None,
        user_id: Optional[int] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get document access summary for the specified period."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query document audits
            query = DocumentAudit.query.filter(
                DocumentAudit.created_at >= start_date
            )
            
            if document_id:
                query = query.filter(DocumentAudit.document_id == document_id)
            
            if user_id:
                query = query.filter(DocumentAudit.user_id == user_id)
            
            audits = query.order_by(DocumentAudit.created_at.desc()).limit(1000).all()
            
            # Analyze document access
            summary = {
                "document_id": document_id,
                "user_id": user_id,
                "period_days": days,
                "total_access_events": len(audits),
                "access_by_action": {},
                "access_by_user": {},
                "access_by_document": {},
                "sensitive_document_access": 0,
                "most_accessed_documents": {},
                "most_active_users": {},
                "access_timeline": [],
                "sharing_events": 0,
                "download_events": 0,
                "modification_events": 0,
                "deletion_events": 0
            }
            
            for audit in audits:
                # Count by action
                action = audit.action
                summary["access_by_action"][action] = summary["access_by_action"].get(action, 0) + 1
                
                # Count by user
                user_id = audit.user_id
                summary["access_by_user"][user_id] = summary["access_by_user"].get(user_id, 0) + 1
                
                # Count by document
                document_id = audit.document_id
                summary["access_by_document"][document_id] = summary["access_by_document"].get(document_id, 0) + 1
                
                # Check for sensitive document access
                metadata = audit.metadata_dict
                if metadata and metadata.get("is_sensitive", False):
                    summary["sensitive_document_access"] += 1
                
                # Count specific events
                if action == "share":
                    summary["sharing_events"] += 1
                elif action == "download":
                    summary["download_events"] += 1
                elif action in ["edit", "modify", "update"]:
                    summary["modification_events"] += 1
                elif action == "delete":
                    summary["deletion_events"] += 1
                
                # Track access timeline
                summary["access_timeline"].append({
                    "timestamp": audit.created_at.isoformat(),
                    "action": action,
                    "document_id": document_id,
                    "user_id": user_id,
                    "file_size": audit.file_size,
                    "processing_time_ms": audit.processing_time_ms
                })
            
            # Get most accessed documents and active users
            summary["most_accessed_documents"] = dict(sorted(summary["access_by_document"].items(), key=lambda x: x[1], reverse=True)[:20])
            summary["most_active_users"] = dict(sorted(summary["access_by_user"].items(), key=lambda x: x[1], reverse=True)[:20])
            
            # Sort access by action
            summary["access_by_action"] = dict(sorted(summary["access_by_action"].items(), key=lambda x: x[1], reverse=True))
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting document access summary: {str(e)}")
            return {"error": str(e)}
    
    def get_document_security_report(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get document security report."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query document audits
            audits = DocumentAudit.query.filter(
                DocumentAudit.created_at >= start_date
            ).all()
            
            # Analyze security patterns
            report = {
                "period_days": days,
                "total_events": len(audits),
                "security_metrics": {
                    "sensitive_document_access": 0,
                    "unauthorized_access_attempts": 0,
                    "bulk_downloads": 0,
                    "suspicious_access_patterns": 0,
                    "document_sharing_violations": 0
                },
                "risk_indicators": [],
                "recommendations": [],
                "access_patterns": {},
                "user_behavior_analysis": {}
            }
            
            user_access_counts = {}
            document_access_counts = {}
            
            for audit in audits:
                user_id = audit.user_id
                document_id = audit.document_id
                action = audit.action
                
                # Count user access
                user_access_counts[user_id] = user_access_counts.get(user_id, 0) + 1
                
                # Count document access
                document_access_counts[document_id] = document_access_counts.get(document_id, 0) + 1
                
                # Check for sensitive document access
                metadata = audit.metadata_dict
                if metadata and metadata.get("is_sensitive", False):
                    report["security_metrics"]["sensitive_document_access"] += 1
                
                # Check for bulk downloads (same user, multiple documents in short time)
                if action == "download":
                    # This would need more sophisticated logic to detect bulk downloads
                    pass
                
                # Check for suspicious access patterns
                if self._is_suspicious_access_pattern(user_id, document_id, action):
                    report["security_metrics"]["suspicious_access_patterns"] += 1
                    report["risk_indicators"].append({
                        "type": "suspicious_access",
                        "user_id": user_id,
                        "document_id": document_id,
                        "action": action,
                        "timestamp": audit.created_at.isoformat()
                    })
            
            # Analyze user behavior
            for user_id, access_count in user_access_counts.items():
                if access_count > 100:  # High access count threshold
                    report["user_behavior_analysis"][user_id] = {
                        "access_count": access_count,
                        "risk_level": "high" if access_count > 500 else "medium",
                        "recommendation": "Review user access patterns"
                    }
            
            # Generate recommendations
            if report["security_metrics"]["sensitive_document_access"] > 50:
                report["recommendations"].append("Consider implementing additional access controls for sensitive documents")
            
            if report["security_metrics"]["suspicious_access_patterns"] > 10:
                report["recommendations"].append("Investigate suspicious access patterns and consider user access reviews")
            
            if len(report["user_behavior_analysis"]) > 5:
                report["recommendations"].append("Review high-activity users and their access patterns")
            
            return report
            
        except Exception as e:
            logger.error(f"Error getting document security report: {str(e)}")
            return {"error": str(e)}
    
    def _is_sensitive_document_access(self, document_id: int, action: str) -> bool:
        """Check if this is access to a sensitive document."""
        try:
            # This would need to be implemented based on your document model
            # For now, we'll use a simple heuristic
            sensitive_actions = ['download', 'share', 'delete']
            return action in sensitive_actions
        except Exception as e:
            logger.error(f"Error checking sensitive document access: {str(e)}")
            return False
    
    def _track_document_access_pattern(self, user_id: int, document_id: int, action: str, is_sensitive: bool):
        """Track document access patterns."""
        try:
            key = f"user_{user_id}"
            if key not in self.document_access_patterns:
                self.document_access_patterns[key] = {
                    "total_access": 0,
                    "sensitive_access": 0,
                    "documents_accessed": set(),
                    "actions": {},
                    "last_access": None
                }
            
            pattern = self.document_access_patterns[key]
            pattern["total_access"] += 1
            pattern["documents_accessed"].add(document_id)
            pattern["actions"][action] = pattern["actions"].get(action, 0) + 1
            pattern["last_access"] = datetime.utcnow()
            
            if is_sensitive:
                pattern["sensitive_access"] += 1
            
        except Exception as e:
            logger.error(f"Error tracking document access pattern: {str(e)}")
    
    def _track_document_modification_history(self, user_id: int, document_id: int, modification_type: str, changes_made: Optional[Dict[str, Any]]):
        """Track document modification history."""
        try:
            key = f"document_{document_id}"
            if key not in self.document_modification_history:
                self.document_modification_history[key] = []
            
            self.document_modification_history[key].append({
                "timestamp": datetime.utcnow(),
                "user_id": user_id,
                "modification_type": modification_type,
                "changes_made": changes_made
            })
            
            # Keep only last 100 modifications per document
            if len(self.document_modification_history[key]) > 100:
                self.document_modification_history[key] = self.document_modification_history[key][-100:]
            
        except Exception as e:
            logger.error(f"Error tracking document modification history: {str(e)}")
    
    def _track_document_sharing_record(self, user_id: int, document_id: int, shared_with: List[int], sharing_method: str, permissions: Optional[List[str]]):
        """Track document sharing records."""
        try:
            key = f"document_{document_id}"
            if key not in self.document_sharing_records:
                self.document_sharing_records[key] = []
            
            self.document_sharing_records[key].append({
                "timestamp": datetime.utcnow(),
                "shared_by": user_id,
                "shared_with": shared_with,
                "sharing_method": sharing_method,
                "permissions": permissions
            })
            
            # Keep only last 50 sharing records per document
            if len(self.document_sharing_records[key]) > 50:
                self.document_sharing_records[key] = self.document_sharing_records[key][-50:]
            
        except Exception as e:
            logger.error(f"Error tracking document sharing record: {str(e)}")
    
    def _check_suspicious_document_access(self, user_id: int, document_id: int, action: str):
        """Check for suspicious document access patterns."""
        try:
            # This would implement logic to detect suspicious patterns like:
            # - Accessing many documents in a short time
            # - Accessing documents outside normal hours
            # - Accessing documents from unusual locations
            # - Repeated failed access attempts
            pass
        except Exception as e:
            logger.error(f"Error checking suspicious document access: {str(e)}")
    
    def _check_suspicious_document_modification(self, user_id: int, document_id: int, modification_type: str, changes_made: Optional[Dict[str, Any]]):
        """Check for suspicious document modifications."""
        try:
            # This would implement logic to detect suspicious modifications like:
            # - Mass modifications
            # - Modifications to critical fields
            # - Modifications outside normal hours
            # - Unusual modification patterns
            pass
        except Exception as e:
            logger.error(f"Error checking suspicious document modification: {str(e)}")
    
    def _is_suspicious_access_pattern(self, user_id: int, document_id: int, action: str) -> bool:
        """Check if this represents a suspicious access pattern."""
        try:
            # Simple heuristic - can be made more sophisticated
            # Check if user is accessing many documents in a short time
            key = f"user_{user_id}"
            if key in self.document_access_patterns:
                pattern = self.document_access_patterns[key]
                if pattern["total_access"] > 50 and len(pattern["documents_accessed"]) > 20:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking suspicious access pattern: {str(e)}")
            return False

# Global document audit service instance
document_audit_service = DocumentAuditService()
