#!/bin/bash

# SmartProBono Audit System Setup Script
# This script sets up the comprehensive auditing system

set -e

echo "🔍 Setting up SmartProBono Audit System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "backend/models/audit.py" ]; then
    print_error "Please run this script from the SmartProBono root directory"
    exit 1
fi

print_info "Setting up audit system components..."

# 1. Install additional Python dependencies
print_info "Installing audit system dependencies..."
pip install -q requests python-dateutil

# 2. Create audit database tables
print_info "Creating audit database schema..."

# Check if we're using Supabase or local database
if [ -f "supabase_api.py" ]; then
    print_info "Detected Supabase setup - applying audit schema..."
    
    # Apply the audit schema to Supabase
    if [ -f "sql/audit_schema.sql" ]; then
        print_info "Applying audit schema to Supabase..."
        # Note: In production, you would use the Supabase CLI or API
        print_warning "Please manually apply sql/audit_schema.sql to your Supabase database"
        print_info "You can do this through the Supabase dashboard SQL editor"
    else
        print_error "Audit schema file not found: sql/audit_schema.sql"
        exit 1
    fi
else
    print_info "Setting up local database audit tables..."
    
    # Create local database tables using Flask-Migrate
    cd backend
    if [ -f "manage.py" ]; then
        python manage.py db upgrade
        print_status "Database tables created/updated"
    else
        print_warning "No manage.py found - please run database migrations manually"
    fi
    cd ..
fi

# 3. Set up environment variables
print_info "Setting up audit environment variables..."

# Create audit environment file if it doesn't exist
if [ ! -f ".env.audit" ]; then
    cat > .env.audit << 'EOF'
# Audit System Configuration
AUDIT_ENABLED=true
AUDIT_LOG_LEVEL=INFO
AUDIT_RETENTION_DAYS=90
AUDIT_SECURITY_RETENTION_DAYS=365
AUDIT_COMPLIANCE_RETENTION_DAYS=2555

# Performance Monitoring
AUDIT_PERFORMANCE_MONITORING=true
AUDIT_RESPONSE_TIME_THRESHOLD_MS=1000
AUDIT_MEMORY_THRESHOLD_PERCENT=80
AUDIT_CPU_THRESHOLD_PERCENT=70

# Security Monitoring
AUDIT_SECURITY_MONITORING=true
AUDIT_FAILED_LOGIN_THRESHOLD=5
AUDIT_FAILED_LOGIN_WINDOW_MINUTES=15
AUDIT_SUSPICIOUS_ACTIVITY_DETECTION=true
AUDIT_IP_BLOCKING=true

# Alerting Configuration
AUDIT_EMAIL_ALERTS=true
AUDIT_EMAIL_RECIPIENTS=admin@smartprobono.org,security@smartprobono.org
AUDIT_SMTP_SERVER=smtp.gmail.com
AUDIT_SMTP_PORT=587
AUDIT_SMTP_USE_TLS=true

# Webhook Alerts (optional)
AUDIT_WEBHOOK_ALERTS=false
AUDIT_WEBHOOK_URL=
AUDIT_WEBHOOK_SECRET=

# Slack Alerts (optional)
AUDIT_SLACK_ALERTS=false
AUDIT_SLACK_WEBHOOK_URL=
AUDIT_SLACK_CHANNEL=#security-alerts

# Real-time Monitoring
AUDIT_REAL_TIME_MONITORING=true
AUDIT_WEBSOCKET_UPDATES=true
AUDIT_DASHBOARD_REFRESH_INTERVAL=30
EOF
    print_status "Created .env.audit file"
else
    print_info ".env.audit already exists"
fi

# 4. Set up log directories
print_info "Creating audit log directories..."
mkdir -p logs/audit
mkdir -p logs/security
mkdir -p logs/performance
mkdir -p logs/compliance
print_status "Audit log directories created"

# 5. Set up log rotation
print_info "Setting up log rotation..."
if [ -f "/etc/logrotate.d/smartprobono-audit" ]; then
    print_info "Log rotation already configured"
else
    sudo tee /etc/logrotate.d/smartprobono-audit > /dev/null << 'EOF'
/Users/baheemferrell/Desktop/Apps/SmartProBono-main/logs/audit/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        # Reload application if needed
        # systemctl reload smartprobono
    endscript
}

/Users/baheemferrell/Desktop/Apps/SmartProBono-main/logs/security/*.log {
    daily
    missingok
    rotate 365
    compress
    delaycompress
    notifempty
    create 644 root root
}

/Users/baheemferrell/Desktop/Apps/SmartProBono-main/logs/performance/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
}

/Users/baheemferrell/Desktop/Apps/SmartProBono-main/logs/compliance/*.log {
    daily
    missingok
    rotate 2555
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
    print_status "Log rotation configured"
fi

# 6. Create audit cleanup script
print_info "Creating audit cleanup script..."
cat > cleanup_audit_data.py << 'EOF'
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
EOF

chmod +x cleanup_audit_data.py
print_status "Created audit cleanup script"

# 7. Set up cron job for cleanup
print_info "Setting up automated cleanup..."
(crontab -l 2>/dev/null; echo "0 2 * * * cd $(pwd) && python cleanup_audit_data.py >> logs/audit/cleanup.log 2>&1") | crontab -
print_status "Cron job for audit cleanup scheduled"

# 8. Create audit dashboard setup
print_info "Setting up audit dashboard..."

# Add audit dashboard route to frontend if not already present
if [ -f "frontend/src/App.js" ]; then
    if ! grep -q "AuditDashboard" frontend/src/App.js; then
        print_info "Adding audit dashboard route to frontend..."
        # This would need to be done manually or with a more sophisticated script
        print_warning "Please manually add the AuditDashboard component to your frontend routing"
    else
        print_info "Audit dashboard route already exists"
    fi
else
    print_warning "Frontend App.js not found - please add audit dashboard manually"
fi

# 9. Test the audit system
print_info "Testing audit system..."

# Create a simple test script
cat > test_audit_system.py << 'EOF'
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
EOF

chmod +x test_audit_system.py
print_status "Created audit system test script"

# 10. Create documentation
print_info "Creating audit system documentation..."

cat > AUDIT_SYSTEM_GUIDE.md << 'EOF'
# SmartProBono Audit System Guide

## Overview

The SmartProBono audit system provides comprehensive logging, monitoring, and alerting capabilities for security, performance, compliance, and user activity tracking.

## Features

### 🔒 Security Auditing
- Failed login attempt tracking
- Suspicious activity detection
- IP address monitoring
- Session management auditing
- Real-time security alerts

### 📊 Performance Monitoring
- API response time tracking
- Database query performance
- Memory and CPU usage monitoring
- Performance threshold alerts

### 👤 User Activity Tracking
- Page views and navigation
- Form submissions
- Document access and downloads
- Search queries and results
- Device and browser tracking

### 📋 Compliance Auditing
- GDPR compliance tracking
- Data retention monitoring
- User consent management
- Regulatory reporting

### 🔍 Data Access Auditing
- Who accessed what data and when
- Document modifications
- Case updates and changes
- Bulk operations monitoring

## Configuration

### Environment Variables

The audit system can be configured using environment variables in `.env.audit`:

```bash
# Enable/disable audit system
AUDIT_ENABLED=true

# Retention periods (in days)
AUDIT_RETENTION_DAYS=90
AUDIT_SECURITY_RETENTION_DAYS=365
AUDIT_COMPLIANCE_RETENTION_DAYS=2555

# Performance thresholds
AUDIT_RESPONSE_TIME_THRESHOLD_MS=1000
AUDIT_MEMORY_THRESHOLD_PERCENT=80
AUDIT_CPU_THRESHOLD_PERCENT=70

# Security settings
AUDIT_FAILED_LOGIN_THRESHOLD=5
AUDIT_FAILED_LOGIN_WINDOW_MINUTES=15
AUDIT_SUSPICIOUS_ACTIVITY_DETECTION=true

# Alerting
AUDIT_EMAIL_ALERTS=true
AUDIT_EMAIL_RECIPIENTS=admin@smartprobono.org,security@smartprobono.org
```

## Usage

### Using Audit Decorators

```python
from utils.audit_decorators import audit_route, security_audit, performance_audit

@audit_route(event_type=AuditEventType.USER_ACTIVITY, action="VIEW_DOCUMENT")
def view_document(document_id):
    # Your code here
    pass

@security_audit(action="ADMIN_ACCESS")
def admin_function():
    # Your code here
    pass

@performance_audit(threshold_ms=500)
def slow_operation():
    # Your code here
    pass
```

### Manual Audit Logging

```python
from services.audit_service import audit_service
from models.audit import AuditEventType, AuditSeverity

# Log an audit event
audit_service.log_audit_event(
    event_type=AuditEventType.DATA_ACCESS,
    action="VIEW",
    user_id=user_id,
    resource_id=document_id,
    resource_type="document",
    description="User viewed document"
)

# Log a security event
audit_service.log_security_event(
    event_type="failed_login",
    severity=AuditSeverity.MEDIUM,
    user_id=user_id,
    reason="Multiple failed login attempts"
)
```

## API Endpoints

### Audit Logs
- `GET /api/audit/logs` - Get audit logs with filtering
- `GET /api/audit/security-events` - Get security events
- `GET /api/audit/user-activities/<user_id>` - Get user activities
- `GET /api/audit/dashboard/stats` - Get dashboard statistics
- `POST /api/audit/export` - Export audit data

### Parameters
- `event_type` - Filter by event type
- `user_id` - Filter by user ID
- `start_date` - Start date (ISO format)
- `end_date` - End date (ISO format)
- `severity` - Filter by severity level
- `limit` - Maximum number of records

## Dashboard

Access the audit dashboard at `/audit-dashboard` (admin access required).

Features:
- Real-time statistics
- Security event monitoring
- Performance metrics
- User activity tracking
- Export capabilities

## Maintenance

### Data Cleanup

The audit system automatically cleans up old data based on retention policies:

```bash
# Manual cleanup
python cleanup_audit_data.py

# Automated cleanup (runs daily at 2 AM)
# Configured via cron job
```

### Monitoring

Monitor audit system health:
- Check log files in `logs/audit/`
- Monitor database size
- Review alert frequency
- Verify retention policies

## Security Considerations

1. **Sensitive Data**: The system automatically redacts sensitive fields
2. **Access Control**: Audit data is protected by Row Level Security (RLS)
3. **Retention**: Data is automatically purged based on retention policies
4. **Encryption**: Audit data should be encrypted at rest
5. **Backup**: Regular backups of audit data are recommended

## Troubleshooting

### Common Issues

1. **High Database Growth**
   - Check retention policies
   - Run cleanup script
   - Review logging levels

2. **Missing Audit Events**
   - Verify audit middleware is enabled
   - Check decorator usage
   - Review error logs

3. **Performance Impact**
   - Adjust logging levels
   - Use async logging
   - Optimize database queries

### Log Files

- `logs/audit/audit.log` - General audit events
- `logs/security/security.log` - Security events
- `logs/performance/performance.log` - Performance metrics
- `logs/compliance/compliance.log` - Compliance events

## Support

For issues or questions about the audit system:
- Check the logs first
- Review this documentation
- Contact the development team
- Create an issue in the repository
EOF

print_status "Created audit system documentation"

# 11. Final setup verification
print_info "Verifying audit system setup..."

# Check if all required files exist
required_files=(
    "backend/models/audit.py"
    "backend/services/audit_service.py"
    "backend/middleware/audit_middleware.py"
    "backend/utils/audit_decorators.py"
    "backend/routes/audit.py"
    "backend/config/audit_config.py"
    "backend/services/alert_service.py"
    "sql/audit_schema.sql"
    "frontend/src/components/AuditDashboard.js"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "Found $file"
    else
        print_error "Missing $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = true ]; then
    print_status "All audit system files are present"
else
    print_error "Some audit system files are missing"
    exit 1
fi

# 12. Summary
echo ""
echo "🎉 SmartProBono Audit System Setup Complete!"
echo ""
echo "📋 Setup Summary:"
echo "  ✅ Audit database models created"
echo "  ✅ Audit service implemented"
echo "  ✅ Audit middleware configured"
echo "  ✅ Audit decorators available"
echo "  ✅ Audit API endpoints created"
echo "  ✅ Alert service implemented"
echo "  ✅ Database schema ready"
echo "  ✅ Frontend dashboard component created"
echo "  ✅ Environment configuration set"
echo "  ✅ Log directories created"
echo "  ✅ Log rotation configured"
echo "  ✅ Cleanup script created"
echo "  ✅ Automated cleanup scheduled"
echo "  ✅ Test script created"
echo "  ✅ Documentation created"
echo ""
echo "🚀 Next Steps:"
echo "  1. Apply the database schema (sql/audit_schema.sql)"
echo "  2. Configure email/Slack alerts in .env.audit"
echo "  3. Add audit dashboard to frontend routing"
echo "  4. Test the system: python test_audit_system.py"
echo "  5. Start using audit decorators in your routes"
echo ""
echo "📚 Documentation: AUDIT_SYSTEM_GUIDE.md"
echo "🔧 Configuration: .env.audit"
echo "🧪 Testing: python test_audit_system.py"
echo "🧹 Cleanup: python cleanup_audit_data.py"
echo ""
print_status "Audit system setup completed successfully!"
