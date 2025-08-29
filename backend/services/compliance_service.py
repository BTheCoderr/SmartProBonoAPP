"""
Compliance auditing service for regulatory requirements and data governance.
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from flask import request, g, current_app
from database import db
from models.audit import ComplianceRecord, AuditEventType, AuditSeverity
from services.audit_service import audit_service
from services.alert_service import alert_service
from config.audit_config import COMPLIANCE_REQUIREMENTS

logger = logging.getLogger(__name__)

class ComplianceService:
    """Service for managing compliance auditing and regulatory requirements."""
    
    def __init__(self):
        self.compliance_rules = COMPLIANCE_REQUIREMENTS
        self.data_retention_policies = {}
        self.consent_records = {}
    
    def log_gdpr_request(
        self,
        user_id: int,
        request_type: str,
        request_id: str = None,
        data_subject: str = None,
        data_types: Optional[List[str]] = None,
        legal_basis: str = "consent",
        description: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log GDPR data subject request."""
        try:
            # Generate request ID if not provided
            if not request_id:
                request_id = f"GDPR_{request_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type=f"gdpr_{request_type}",
                user_id=user_id,
                request_id=request_id,
                status="pending",
                description=description or f"GDPR {request_type} request",
                data_subject=data_subject,
                data_types=data_types,
                legal_basis=legal_basis,
                retention_period=self.compliance_rules.get("gdpr", {}).get("data_retention_days", 2555),
                metadata=metadata
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action=f"GDPR_{request_type.upper()}",
                user_id=user_id,
                resource_id=request_id,
                resource_type="gdpr_request",
                description=f"GDPR {request_type} request received",
                severity=AuditSeverity.HIGH,
                metadata={
                    "request_type": request_type,
                    "request_id": request_id,
                    "data_subject": data_subject,
                    "data_types": data_types,
                    "legal_basis": legal_basis
                }
            )
            
            # Send compliance alert
            alert_service.send_compliance_alert(
                f"gdpr_{request_type}",
                "pending",
                user_id,
                f"GDPR {request_type} request received"
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging GDPR request: {str(e)}")
            raise
    
    def log_ccpa_request(
        self,
        user_id: int,
        request_type: str,
        request_id: str = None,
        data_subject: str = None,
        data_types: Optional[List[str]] = None,
        description: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log CCPA consumer request."""
        try:
            # Generate request ID if not provided
            if not request_id:
                request_id = f"CCPA_{request_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type=f"ccpa_{request_type}",
                user_id=user_id,
                request_id=request_id,
                status="pending",
                description=description or f"CCPA {request_type} request",
                data_subject=data_subject,
                data_types=data_types,
                legal_basis="consumer_rights",
                retention_period=self.compliance_rules.get("ccpa", {}).get("data_retention_days", 1095),
                metadata=metadata
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action=f"CCPA_{request_type.upper()}",
                user_id=user_id,
                resource_id=request_id,
                resource_type="ccpa_request",
                description=f"CCPA {request_type} request received",
                severity=AuditSeverity.HIGH,
                metadata={
                    "request_type": request_type,
                    "request_id": request_id,
                    "data_subject": data_subject,
                    "data_types": data_types
                }
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging CCPA request: {str(e)}")
            raise
    
    def log_data_retention_event(
        self,
        user_id: int,
        data_type: str,
        retention_action: str,
        record_count: int = None,
        retention_period_days: int = None,
        description: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log data retention policy event."""
        try:
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type="data_retention",
                user_id=user_id,
                status="completed",
                description=description or f"Data retention: {retention_action} for {data_type}",
                data_types=[data_type],
                legal_basis="data_retention_policy",
                retention_period=retention_period_days,
                metadata={
                    "retention_action": retention_action,
                    "record_count": record_count,
                    "data_type": data_type,
                    **(metadata or {})
                }
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action=f"DATA_RETENTION_{retention_action.upper()}",
                user_id=user_id,
                resource_type="data_retention",
                description=f"Data retention: {retention_action} for {data_type}",
                severity=AuditSeverity.MEDIUM,
                metadata={
                    "retention_action": retention_action,
                    "data_type": data_type,
                    "record_count": record_count,
                    "retention_period_days": retention_period_days
                }
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging data retention event: {str(e)}")
            raise
    
    def log_consent_event(
        self,
        user_id: int,
        consent_type: str,
        consent_given: bool,
        consent_method: str = "explicit",
        consent_version: str = None,
        data_processing_purposes: Optional[List[str]] = None,
        description: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log user consent event."""
        try:
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type="consent_management",
                user_id=user_id,
                status="completed",
                description=description or f"Consent {consent_type}: {'given' if consent_given else 'withdrawn'}",
                legal_basis="consent",
                metadata={
                    "consent_type": consent_type,
                    "consent_given": consent_given,
                    "consent_method": consent_method,
                    "consent_version": consent_version,
                    "data_processing_purposes": data_processing_purposes,
                    **(metadata or {})
                }
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action=f"CONSENT_{'GIVEN' if consent_given else 'WITHDRAWN'}",
                user_id=user_id,
                resource_type="consent",
                description=f"Consent {consent_type}: {'given' if consent_given else 'withdrawn'}",
                severity=AuditSeverity.MEDIUM,
                metadata={
                    "consent_type": consent_type,
                    "consent_given": consent_given,
                    "consent_method": consent_method,
                    "consent_version": consent_version,
                    "data_processing_purposes": data_processing_purposes
                }
            )
            
            # Track consent records
            self._track_consent_record(user_id, consent_type, consent_given, consent_version)
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging consent event: {str(e)}")
            raise
    
    def log_data_breach_event(
        self,
        breach_type: str,
        affected_users: int,
        data_types_affected: Optional[List[str]] = None,
        breach_description: str = None,
        containment_actions: Optional[List[str]] = None,
        notification_sent: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log data breach event."""
        try:
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type="data_breach",
                status="investigating",
                description=breach_description or f"Data breach: {breach_type}",
                data_types=data_types_affected,
                legal_basis="breach_notification_requirement",
                metadata={
                    "breach_type": breach_type,
                    "affected_users": affected_users,
                    "data_types_affected": data_types_affected,
                    "containment_actions": containment_actions,
                    "notification_sent": notification_sent,
                    **(metadata or {})
                }
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action="DATA_BREACH_DETECTED",
                resource_type="data_breach",
                description=f"Data breach detected: {breach_type}",
                severity=AuditSeverity.CRITICAL,
                metadata={
                    "breach_type": breach_type,
                    "affected_users": affected_users,
                    "data_types_affected": data_types_affected,
                    "containment_actions": containment_actions,
                    "notification_sent": notification_sent
                }
            )
            
            # Send critical compliance alert
            alert_service.send_compliance_alert(
                "data_breach",
                "investigating",
                None,
                f"Data breach detected: {breach_type} affecting {affected_users} users"
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging data breach event: {str(e)}")
            raise
    
    def log_privacy_policy_acceptance(
        self,
        user_id: int,
        policy_version: str,
        acceptance_method: str = "click",
        ip_address: str = None,
        user_agent: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log privacy policy acceptance."""
        try:
            # Log compliance record
            record = audit_service.log_compliance_record(
                record_type="privacy_policy_acceptance",
                user_id=user_id,
                status="completed",
                description=f"Privacy policy v{policy_version} accepted",
                legal_basis="consent",
                metadata={
                    "policy_version": policy_version,
                    "acceptance_method": acceptance_method,
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    **(metadata or {})
                }
            )
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action="PRIVACY_POLICY_ACCEPTED",
                user_id=user_id,
                resource_type="privacy_policy",
                description=f"Privacy policy v{policy_version} accepted",
                severity=AuditSeverity.LOW,
                metadata={
                    "policy_version": policy_version,
                    "acceptance_method": acceptance_method,
                    "ip_address": ip_address,
                    "user_agent": user_agent
                }
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error logging privacy policy acceptance: {str(e)}")
            raise
    
    def update_compliance_record_status(
        self,
        record_id: int,
        new_status: str,
        processed_by: int,
        processing_notes: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Update compliance record status."""
        try:
            # Get the record
            record = ComplianceRecord.query.get(record_id)
            if not record:
                raise ValueError(f"Compliance record {record_id} not found")
            
            # Update status
            old_status = record.status
            record.status = new_status
            record.processed_by = processed_by
            record.processed_at = datetime.utcnow()
            
            if processing_notes:
                record.description = f"{record.description} - {processing_notes}"
            
            if metadata:
                existing_metadata = record.metadata_dict
                existing_metadata.update(metadata)
                record.metadata = json.dumps(existing_metadata)
            
            db.session.commit()
            
            # Log status change
            audit_service.log_audit_event(
                event_type=AuditEventType.COMPLIANCE,
                action="STATUS_UPDATE",
                user_id=processed_by,
                resource_id=str(record_id),
                resource_type="compliance_record",
                description=f"Compliance record status changed: {old_status} -> {new_status}",
                severity=AuditSeverity.MEDIUM,
                metadata={
                    "record_id": record_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "processed_by": processed_by,
                    "processing_notes": processing_notes
                }
            )
            
            return record
            
        except Exception as e:
            logger.error(f"Error updating compliance record status: {str(e)}")
            db.session.rollback()
            raise
    
    def get_compliance_summary(
        self,
        record_type: Optional[str] = None,
        status: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get compliance summary for the specified period."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query compliance records
            query = ComplianceRecord.query.filter(
                ComplianceRecord.created_at >= start_date
            )
            
            if record_type:
                query = query.filter(ComplianceRecord.record_type == record_type)
            
            if status:
                query = query.filter(ComplianceRecord.status == status)
            
            records = query.order_by(ComplianceRecord.created_at.desc()).limit(1000).all()
            
            # Analyze compliance data
            summary = {
                "record_type": record_type,
                "status": status,
                "period_days": days,
                "total_records": len(records),
                "records_by_type": {},
                "records_by_status": {},
                "records_by_user": {},
                "processing_times": {},
                "compliance_timeline": [],
                "pending_requests": 0,
                "overdue_requests": 0,
                "compliance_metrics": {
                    "gdpr_requests": 0,
                    "ccpa_requests": 0,
                    "consent_events": 0,
                    "data_retention_events": 0,
                    "breach_events": 0
                }
            }
            
            for record in records:
                # Count by type
                record_type = record.record_type
                summary["records_by_type"][record_type] = summary["records_by_type"].get(record_type, 0) + 1
                
                # Count by status
                status = record.status
                summary["records_by_status"][status] = summary["records_by_status"].get(status, 0) + 1
                
                # Count by user
                user_id = record.user_id
                if user_id:
                    summary["records_by_user"][user_id] = summary["records_by_user"].get(user_id, 0) + 1
                
                # Track processing times
                if record.processed_at:
                    processing_time = (record.processed_at - record.created_at).total_seconds() / 3600  # hours
                    if record_type not in summary["processing_times"]:
                        summary["processing_times"][record_type] = []
                    summary["processing_times"][record_type].append(processing_time)
                
                # Track compliance timeline
                summary["compliance_timeline"].append({
                    "timestamp": record.created_at.isoformat(),
                    "record_type": record_type,
                    "status": status,
                    "user_id": user_id,
                    "description": record.description
                })
                
                # Count pending requests
                if status == "pending":
                    summary["pending_requests"] += 1
                    
                    # Check for overdue requests (GDPR: 30 days, CCPA: 45 days)
                    days_since_created = (datetime.utcnow() - record.created_at).days
                    if record_type.startswith("gdpr") and days_since_created > 30:
                        summary["overdue_requests"] += 1
                    elif record_type.startswith("ccpa") and days_since_created > 45:
                        summary["overdue_requests"] += 1
                
                # Count compliance metrics
                if record_type.startswith("gdpr"):
                    summary["compliance_metrics"]["gdpr_requests"] += 1
                elif record_type.startswith("ccpa"):
                    summary["compliance_metrics"]["ccpa_requests"] += 1
                elif record_type == "consent_management":
                    summary["compliance_metrics"]["consent_events"] += 1
                elif record_type == "data_retention":
                    summary["compliance_metrics"]["data_retention_events"] += 1
                elif record_type == "data_breach":
                    summary["compliance_metrics"]["breach_events"] += 1
            
            # Calculate average processing times
            for record_type, times in summary["processing_times"].items():
                if times:
                    summary["processing_times"][record_type] = {
                        "average_hours": sum(times) / len(times),
                        "min_hours": min(times),
                        "max_hours": max(times),
                        "count": len(times)
                    }
            
            # Sort dictionaries by count
            summary["records_by_type"] = dict(sorted(summary["records_by_type"].items(), key=lambda x: x[1], reverse=True))
            summary["records_by_status"] = dict(sorted(summary["records_by_status"].items(), key=lambda x: x[1], reverse=True))
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting compliance summary: {str(e)}")
            return {"error": str(e)}
    
    def check_data_retention_compliance(self) -> Dict[str, Any]:
        """Check data retention compliance across all data types."""
        try:
            compliance_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_compliance": "compliant",
                "violations": [],
                "recommendations": [],
                "data_types": {}
            }
            
            # Check each compliance rule
            for regulation, rules in self.compliance_rules.items():
                retention_days = rules.get("data_retention_days", 0)
                
                if retention_days > 0:
                    cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
                    
                    # This would need to be implemented based on your data models
                    # For now, we'll create a placeholder structure
                    compliance_status["data_types"][regulation] = {
                        "retention_days": retention_days,
                        "cutoff_date": cutoff_date.isoformat(),
                        "status": "compliant",
                        "records_to_review": 0
                    }
            
            return compliance_status
            
        except Exception as e:
            logger.error(f"Error checking data retention compliance: {str(e)}")
            return {"error": str(e)}
    
    def _track_consent_record(self, user_id: int, consent_type: str, consent_given: bool, consent_version: str = None):
        """Track consent records for compliance."""
        try:
            key = f"{user_id}_{consent_type}"
            if key not in self.consent_records:
                self.consent_records[key] = []
            
            self.consent_records[key].append({
                "timestamp": datetime.utcnow(),
                "consent_given": consent_given,
                "consent_version": consent_version
            })
            
            # Keep only last 100 consent records per user/type
            if len(self.consent_records[key]) > 100:
                self.consent_records[key] = self.consent_records[key][-100:]
            
        except Exception as e:
            logger.error(f"Error tracking consent record: {str(e)}")

# Global compliance service instance
compliance_service = ComplianceService()
