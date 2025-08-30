#!/usr/bin/env python3
"""
Audit data cleanup script for SmartProBono.
This script removes old audit data based on retention policies.
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import db
from models.audit import AuditLog, UserActivity, SecurityEvent, PerformanceMetric, ComplianceRecord, APIAudit, DocumentAudit
from config.audit_config import AUDIT_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_audit_data():
    """Clean up old audit data based on retention policies."""
    try:
        # Get retention periods
        retention_days = AUDIT_CONFIG.get('retention_days', 90)
        security_retention_days = AUDIT_CONFIG.get('security_retention_days', 365)
        compliance_retention_days = AUDIT_CONFIG.get('compliance_retention_days', 2555)
        
        # Calculate cutoff dates
        audit_cutoff = datetime.utcnow() - timedelta(days=retention_days)
        security_cutoff = datetime.utcnow() - timedelta(days=security_retention_days)
        compliance_cutoff = datetime.utcnow() - timedelta(days=compliance_retention_days)
        performance_cutoff = datetime.utcnow() - timedelta(days=30)  # Keep performance data for 30 days
        
        # Clean up audit logs
        audit_logs_deleted = AuditLog.query.filter(AuditLog.created_at < audit_cutoff).delete()
        logger.info(f"Deleted {audit_logs_deleted} old audit logs")
        
        # Clean up user activities
        user_activities_deleted = UserActivity.query.filter(UserActivity.created_at < audit_cutoff).delete()
        logger.info(f"Deleted {user_activities_deleted} old user activities")
        
        # Clean up security events
        security_events_deleted = SecurityEvent.query.filter(SecurityEvent.created_at < security_cutoff).delete()
        logger.info(f"Deleted {security_events_deleted} old security events")
        
        # Clean up performance metrics
        performance_metrics_deleted = PerformanceMetric.query.filter(PerformanceMetric.created_at < performance_cutoff).delete()
        logger.info(f"Deleted {performance_metrics_deleted} old performance metrics")
        
        # Clean up API audits
        api_audits_deleted = APIAudit.query.filter(APIAudit.created_at < audit_cutoff).delete()
        logger.info(f"Deleted {api_audits_deleted} old API audits")
        
        # Clean up document audits
        document_audits_deleted = DocumentAudit.query.filter(DocumentAudit.created_at < audit_cutoff).delete()
        logger.info(f"Deleted {document_audits_deleted} old document audits")
        
        # Keep compliance records longer
        compliance_records_deleted = ComplianceRecord.query.filter(ComplianceRecord.created_at < compliance_cutoff).delete()
        logger.info(f"Deleted {compliance_records_deleted} old compliance records")
        
        # Commit changes
        db.session.commit()
        
        total_deleted = (audit_logs_deleted + user_activities_deleted + security_events_deleted + 
                        performance_metrics_deleted + api_audits_deleted + document_audits_deleted + 
                        compliance_records_deleted)
        
        logger.info(f"Cleanup completed. Total records deleted: {total_deleted}")
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    with app.app_context():
        cleanup_audit_data()
