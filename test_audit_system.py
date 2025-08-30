#!/usr/bin/env python3
"""
Test script for the audit system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.audit_service import audit_service
from models.audit import AuditEventType, AuditSeverity

def test_audit_system():
    """Test the audit system functionality."""
    print("Testing audit system...")
    
    try:
        # Test audit event logging
        audit_log = audit_service.log_audit_event(
            event_type=AuditEventType.SYSTEM,
            action="TEST",
            description="Testing audit system",
            severity=AuditSeverity.LOW,
            metadata={"test": True}
        )
        print(f"✅ Audit event logged: {audit_log.id}")
        
        # Test security event logging
        security_event = audit_service.log_security_event(
            event_type="test_security_event",
            severity=AuditSeverity.MEDIUM,
            reason="Testing security event logging"
        )
        print(f"✅ Security event logged: {security_event.id}")
        
        # Test performance metric logging
        performance_metric = audit_service.log_performance_metric(
            metric_type="test_metric",
            value=100.0,
            unit="ms",
            threshold=200.0
        )
        print(f"✅ Performance metric logged: {performance_metric.id}")
        
        print("✅ All audit system tests passed!")
        
    except Exception as e:
        print(f"❌ Audit system test failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    
    with app.app_context():
        test_audit_system()
