# SmartProBono Audit System Integration Guide

## 🎯 Complete Audit System Implementation

This guide shows you how to integrate and use all the audit services we've created for your SmartProBono platform.

## 📋 Services Overview

### 1. **UserActivityService** - User Behavior Tracking
- Page views and navigation
- Form submissions and interactions
- File downloads and searches
- Session tracking and analytics

### 2. **DataAccessService** - Data Access & Modification Auditing
- Data access logging
- Modification tracking
- Bulk operations monitoring
- Data export auditing

### 3. **PerformanceService** - System Performance Monitoring
- Endpoint performance tracking
- Database query monitoring
- System resource usage
- Performance alerts

### 4. **ComplianceService** - Regulatory Compliance
- GDPR request handling
- CCPA compliance tracking
- Data retention management
- Consent management

### 5. **APIAuditService** - API Usage & Rate Limiting
- API request logging
- Rate limit management
- Performance metrics
- Usage analytics

### 6. **DocumentAuditService** - Document Access & Security
- Document access tracking
- Modification history
- Sharing and permissions
- Security monitoring

## 🔧 Integration Examples

### Basic Route Integration

```python
from services.user_activity_service import user_activity_service
from services.data_access_service import data_access_service
from services.performance_service import performance_service
from utils.audit_decorators import audit_route, security_audit, performance_audit

@app.route('/api/documents/<int:document_id>')
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="VIEW_DOCUMENT")
@security_audit(action="DOCUMENT_ACCESS")
@performance_audit(threshold_ms=1000)
def view_document(document_id):
    """View a document with comprehensive auditing."""
    
    # Track user activity
    user_activity_service.track_page_view(
        user_id=get_jwt_identity(),
        page_url=f"/api/documents/{document_id}",
        page_title="Document View",
        metadata={"document_id": document_id}
    )
    
    # Log data access
    data_access_service.log_data_access(
        user_id=get_jwt_identity(),
        resource_type="document",
        resource_id=str(document_id),
        action="READ",
        data_fields=["title", "content", "metadata"],
        result_count=1
    )
    
    # Get document (your existing logic)
    document = get_document(document_id)
    
    # Log document access
    document_audit_service.log_document_access(
        document_id=document_id,
        user_id=get_jwt_identity(),
        action="view",
        file_size=document.file_size,
        version=document.version
    )
    
    return jsonify(document.to_dict())
```

### Form Submission with Full Auditing

```python
@app.route('/api/forms/submit', methods=['POST'])
@jwt_required()
@audit_route(event_type=AuditEventType.USER_ACTIVITY, action="FORM_SUBMIT")
def submit_form():
    """Submit a form with comprehensive auditing."""
    
    user_id = get_jwt_identity()
    form_data = request.get_json()
    
    # Track form submission
    user_activity_service.track_form_submission(
        user_id=user_id,
        form_type="legal_intake",
        success=True,
        metadata={"form_fields": list(form_data.keys())}
    )
    
    # Log data modification
    data_access_service.log_data_modification(
        user_id=user_id,
        resource_type="form_submission",
        resource_id=str(uuid.uuid4()),
        action="CREATE",
        new_data=form_data,
        metadata={"form_type": "legal_intake"}
    )
    
    # Process form (your existing logic)
    result = process_form_submission(form_data)
    
    return jsonify({"status": "success", "result": result})
```

### API Endpoint with Rate Limiting

```python
@app.route('/api/legal/chat', methods=['POST'])
@jwt_required()
def legal_chat():
    """Legal chat endpoint with rate limiting and auditing."""
    
    user_id = get_jwt_identity()
    endpoint = request.path
    method = request.method
    
    # Check rate limits
    within_limit, rate_info = api_audit_service.check_rate_limit(
        user_id=user_id,
        endpoint=endpoint,
        method=method
    )
    
    if not within_limit:
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    # Track user activity
    user_activity_service.track_user_click(
        user_id=user_id,
        element_id="legal_chat_submit",
        page_url="/legal-chat",
        metadata={"action": "chat_submission"}
    )
    
    # Process request
    start_time = time.time()
    response_data = process_legal_chat(request.get_json())
    processing_time = int((time.time() - start_time) * 1000)
    
    # Log API usage
    api_audit_service.log_api_request(
        endpoint=endpoint,
        method=method,
        response_time_ms=processing_time,
        status_code=200,
        user_id=user_id,
        request_size=len(request.get_data()),
        response_size=len(json.dumps(response_data)),
        rate_limit_remaining=rate_info["remaining"]
    )
    
    return jsonify(response_data)
```

### Document Download with Security Auditing

```python
@app.route('/api/documents/<int:document_id>/download')
@jwt_required()
@audit_route(event_type=AuditEventType.DOCUMENT_ACCESS, action="DOCUMENT_DOWNLOAD")
def download_document(document_id):
    """Download document with security auditing."""
    
    user_id = get_jwt_identity()
    
    # Check permissions (your existing logic)
    if not has_document_access(user_id, document_id):
        # Log unauthorized access attempt
        audit_service.log_security_event(
            event_type="unauthorized_document_access",
            severity=AuditSeverity.HIGH,
            user_id=user_id,
            reason=f"Unauthorized access attempt to document {document_id}",
            blocked=True,
            response_action="deny_access"
        )
        return jsonify({"error": "Access denied"}), 403
    
    # Track user activity
    user_activity_service.track_file_download(
        user_id=user_id,
        file_name=f"document_{document_id}.pdf",
        file_type="pdf",
        page_url=f"/documents/{document_id}/download"
    )
    
    # Log document access
    document_audit_service.log_document_download(
        document_id=document_id,
        user_id=user_id,
        download_format="pdf",
        file_size=get_document_size(document_id),
        processing_time_ms=0
    )
    
    # Log data access
    data_access_service.log_data_access(
        user_id=user_id,
        resource_type="document",
        resource_id=str(document_id),
        action="DOWNLOAD",
        data_fields=["content", "metadata"],
        result_count=1
    )
    
    # Serve file (your existing logic)
    return send_file(get_document_path(document_id))
```

### GDPR Request Handling

```python
@app.route('/api/compliance/gdpr/request', methods=['POST'])
@jwt_required()
@audit_route(event_type=AuditEventType.COMPLIANCE, action="GDPR_REQUEST")
def handle_gdpr_request():
    """Handle GDPR data subject request."""
    
    user_id = get_jwt_identity()
    request_data = request.get_json()
    request_type = request_data.get('type')  # access, portability, deletion, etc.
    
    # Log GDPR request
    compliance_record = compliance_service.log_gdpr_request(
        user_id=user_id,
        request_type=request_type,
        data_subject=request_data.get('data_subject'),
        data_types=request_data.get('data_types'),
        legal_basis="data_subject_rights",
        description=f"GDPR {request_type} request from user {user_id}"
    )
    
    # Process request based on type
    if request_type == "access":
        # Provide data access
        user_data = get_user_data(user_id)
        result = {"data": user_data, "request_id": compliance_record.id}
    
    elif request_type == "deletion":
        # Process data deletion
        delete_user_data(user_id)
        result = {"status": "deleted", "request_id": compliance_record.id}
    
    elif request_type == "portability":
        # Export user data
        export_data = export_user_data(user_id)
        result = {"export_data": export_data, "request_id": compliance_record.id}
    
    # Update compliance record status
    compliance_service.update_compliance_record_status(
        record_id=compliance_record.id,
        new_status="completed",
        processed_by=user_id,
        processing_notes=f"GDPR {request_type} request processed"
    )
    
    return jsonify(result)
```

### Performance Monitoring Integration

```python
@app.route('/api/performance/monitor')
@jwt_required()
@performance_service.performance_decorator(metric_type="response_time", threshold=500)
def monitor_performance():
    """Monitor system performance."""
    
    # Get system health
    health_status = performance_service.get_system_health_status()
    
    # Get performance metrics
    performance_metrics = performance_service.get_performance_summary(days=7)
    
    # Get API performance
    api_metrics = api_audit_service.get_api_performance_metrics(days=7)
    
    return jsonify({
        "system_health": health_status,
        "performance_metrics": performance_metrics,
        "api_metrics": api_metrics
    })
```

## 🔄 Middleware Integration

### Automatic Request Auditing

The audit middleware automatically logs all requests. To enable it, add to your Flask app:

```python
from middleware.audit_middleware import AuditMiddleware

app = Flask(__name__)
audit_middleware = AuditMiddleware(app)
```

### Custom Middleware for Specific Routes

```python
@app.before_request
def before_request():
    """Custom before request handler."""
    g.start_time = time.time()
    g.user_id = get_jwt_identity() if hasattr(g, 'user_id') else None

@app.after_request
def after_request(response):
    """Custom after request handler."""
    if hasattr(g, 'start_time'):
        processing_time = int((time.time() - g.start_time) * 1000)
        
        # Log performance metric
        performance_service.monitor_endpoint_performance(
            endpoint=request.path,
            method=request.method,
            response_time_ms=processing_time,
            status_code=response.status_code,
            user_id=getattr(g, 'user_id', None)
        )
    
    return response
```

## 📊 Dashboard Integration

### Add Audit Dashboard to Frontend

```javascript
// In your React app
import AuditDashboard from './components/AuditDashboard';

// Add route
<Route path="/admin/audit" component={AuditDashboard} />

// Add navigation link
<Link to="/admin/audit">Audit Dashboard</Link>
```

### Real-time Updates

```javascript
// WebSocket integration for real-time updates
useEffect(() => {
    const ws = new WebSocket('ws://localhost:5000/audit-updates');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'audit_event') {
            // Update dashboard with new audit event
            updateAuditDashboard(data.event);
        }
    };
    
    return () => ws.close();
}, []);
```

## 🚨 Alert Configuration

### Email Alerts Setup

```python
# In your .env.audit file
AUDIT_EMAIL_ALERTS=true
AUDIT_EMAIL_RECIPIENTS=admin@smartprobono.org,security@smartprobono.org
AUDIT_SMTP_SERVER=smtp.gmail.com
AUDIT_SMTP_PORT=587
AUDIT_SMTP_USE_TLS=true
AUDIT_SMTP_USERNAME=your-email@gmail.com
AUDIT_SMTP_PASSWORD=your-app-password
```

### Slack Integration

```python
# In your .env.audit file
AUDIT_SLACK_ALERTS=true
AUDIT_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
AUDIT_SLACK_CHANNEL=#security-alerts
```

## 🔍 Monitoring and Maintenance

### Daily Cleanup Script

```bash
# Add to crontab
0 2 * * * cd /path/to/smartprobono && python cleanup_audit_data.py
```

### Performance Monitoring

```python
# Monitor system resources every 5 minutes
import schedule
import time

def monitor_system():
    performance_service.monitor_system_resources()

schedule.every(5).minutes.do(monitor_system)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Health Checks

```python
@app.route('/api/health/audit')
def audit_health_check():
    """Health check for audit system."""
    try:
        # Check database connectivity
        audit_service.get_audit_logs(limit=1)
        
        # Check system resources
        health_status = performance_service.get_system_health_status()
        
        return jsonify({
            "status": "healthy",
            "audit_system": "operational",
            "system_health": health_status
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
```

## 📈 Analytics and Reporting

### Generate Compliance Reports

```python
@app.route('/api/reports/compliance')
@jwt_required()
def generate_compliance_report():
    """Generate compliance report."""
    
    # Get compliance summary
    gdpr_summary = compliance_service.get_compliance_summary(
        record_type="gdpr_access",
        days=30
    )
    
    # Get data access summary
    data_access_summary = data_access_service.get_data_access_summary(days=30)
    
    # Get document access summary
    document_summary = document_audit_service.get_document_access_summary(days=30)
    
    return jsonify({
        "gdpr_compliance": gdpr_summary,
        "data_access": data_access_summary,
        "document_access": document_summary,
        "generated_at": datetime.utcnow().isoformat()
    })
```

### User Activity Analytics

```python
@app.route('/api/analytics/user-activity/<int:user_id>')
@jwt_required()
def get_user_activity_analytics(user_id):
    """Get user activity analytics."""
    
    # Get user activity summary
    activity_summary = user_activity_service.get_user_activity_summary(user_id, days=30)
    
    # Get user activity patterns
    activity_patterns = user_activity_service.get_user_activity_patterns(user_id, days=30)
    
    return jsonify({
        "user_id": user_id,
        "activity_summary": activity_summary,
        "activity_patterns": activity_patterns
    })
```

## 🛡️ Security Best Practices

### Sensitive Data Handling

```python
# Automatically redact sensitive fields
SENSITIVE_FIELDS = ['password', 'ssn', 'credit_card', 'api_key']

def sanitize_data(data):
    """Sanitize sensitive data for logging."""
    if isinstance(data, dict):
        return {k: "[REDACTED]" if k.lower() in SENSITIVE_FIELDS else v 
                for k, v in data.items()}
    return data
```

### Access Control

```python
# Ensure only admins can access audit data
@app.route('/api/audit/logs')
@jwt_required()
@admin_required
def get_audit_logs():
    """Get audit logs (admin only)."""
    # Implementation here
    pass
```

## 🚀 Deployment Checklist

- [ ] Apply database schema (`sql/audit_schema.sql`)
- [ ] Configure environment variables (`.env.audit`)
- [ ] Set up email/Slack alerts
- [ ] Configure log rotation
- [ ] Set up automated cleanup
- [ ] Add audit dashboard to frontend
- [ ] Test all audit services
- [ ] Configure monitoring and alerts
- [ ] Set up compliance reporting
- [ ] Train team on audit system usage

## 📞 Support

For questions or issues with the audit system:
- Check the logs in `logs/audit/`
- Review the configuration in `.env.audit`
- Test individual services with the test script
- Contact the development team

This comprehensive audit system provides complete visibility into your SmartProBono platform's security, performance, and compliance status! 🎉
