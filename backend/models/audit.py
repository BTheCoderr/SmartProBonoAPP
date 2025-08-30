"""
Audit models for comprehensive system auditing.
"""
from datetime import datetime
from database import db
import json
import enum

class AuditEventType(enum.Enum):
    """Types of audit events"""
    SECURITY = "security"
    USER_ACTIVITY = "user_activity"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    PERFORMANCE = "performance"
    API_USAGE = "api_usage"
    DOCUMENT_ACCESS = "document_access"
    COMPLIANCE = "compliance"
    SYSTEM = "system"

class AuditSeverity(enum.Enum):
    """Severity levels for audit events"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditLog(db.Model):
    """General system audit trail"""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.Enum(AuditEventType), nullable=False)
    severity = db.Column(db.Enum(AuditSeverity), default=AuditSeverity.LOW)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 support
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    method = db.Column(db.String(10), nullable=True)
    status_code = db.Column(db.Integer, nullable=True)
    request_data = db.Column(db.Text, nullable=True)  # JSON string
    response_data = db.Column(db.Text, nullable=True)  # JSON string
    error_message = db.Column(db.Text, nullable=True)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    resource_id = db.Column(db.String(255), nullable=True)  # ID of affected resource
    resource_type = db.Column(db.String(100), nullable=True)  # Type of affected resource
    action = db.Column(db.String(100), nullable=False)  # CREATE, READ, UPDATE, DELETE, etc.
    description = db.Column(db.Text, nullable=True)
    audit_metadata = db.Column(db.Text, nullable=True)  # Additional JSON data
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<AuditLog {self.event_type.value}:{self.action} by {self.user_id}>'

    @property
    def request_data_dict(self):
        """Get request data as dictionary"""
        if self.request_data:
            try:
                return json.loads(self.request_data)
            except json.JSONDecodeError:
                return {}
        return {}

    @property
    def response_data_dict(self):
        """Get response data as dictionary"""
        if self.response_data:
            try:
                return json.loads(self.response_data)
            except json.JSONDecodeError:
                return {}
        return {}

    @property
    def metadata_dict(self):
        """Get metadata as dictionary"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except json.JSONDecodeError:
                return {}
        return {}

class UserActivity(db.Model):
    """User interaction tracking"""
    __tablename__ = 'user_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(255), nullable=True)
    activity_type = db.Column(db.String(100), nullable=False)  # login, logout, page_view, etc.
    page_url = db.Column(db.String(500), nullable=True)
    page_title = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(100), nullable=True)  # click, submit, download, etc.
    element_id = db.Column(db.String(255), nullable=True)  # ID of clicked element
    element_class = db.Column(db.String(255), nullable=True)  # Class of clicked element
    duration_seconds = db.Column(db.Integer, nullable=True)  # Time spent on page
    referrer = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    device_type = db.Column(db.String(50), nullable=True)  # desktop, mobile, tablet
    browser = db.Column(db.String(100), nullable=True)
    os = db.Column(db.String(100), nullable=True)
    audit_metadata = db.Column(db.Text, nullable=True)  # Additional JSON data
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<UserActivity {self.activity_type} by {self.user_id}>'

class SecurityEvent(db.Model):
    """Security-related events"""
    __tablename__ = 'security_events'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)  # failed_login, suspicious_activity, etc.
    severity = db.Column(db.Enum(AuditSeverity), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    attack_type = db.Column(db.String(100), nullable=True)  # brute_force, sql_injection, etc.
    blocked = db.Column(db.Boolean, default=False)
    reason = db.Column(db.Text, nullable=True)
    response_action = db.Column(db.String(100), nullable=True)  # block_ip, lock_account, etc.
    audit_metadata = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<SecurityEvent {self.event_type}:{self.severity.value}>'

class PerformanceMetric(db.Model):
    """System performance data"""
    __tablename__ = 'performance_metrics'

    id = db.Column(db.Integer, primary_key=True)
    metric_type = db.Column(db.String(100), nullable=False)  # response_time, memory_usage, etc.
    endpoint = db.Column(db.String(255), nullable=True)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=True)  # ms, MB, %, etc.
    threshold = db.Column(db.Float, nullable=True)  # Alert threshold
    exceeded_threshold = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)
    audit_metadata = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<PerformanceMetric {self.metric_type}:{self.value}{self.unit}>'

class ComplianceRecord(db.Model):
    """Regulatory compliance tracking"""
    __tablename__ = 'compliance_records'

    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(100), nullable=False)  # gdpr_request, data_retention, etc.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    request_id = db.Column(db.String(255), nullable=True)  # External request ID
    status = db.Column(db.String(50), nullable=False)  # pending, completed, failed
    description = db.Column(db.Text, nullable=True)
    data_subject = db.Column(db.String(255), nullable=True)  # Person whose data is involved
    data_types = db.Column(db.Text, nullable=True)  # JSON array of data types
    legal_basis = db.Column(db.String(100), nullable=True)  # consent, legitimate_interest, etc.
    retention_period = db.Column(db.Integer, nullable=True)  # Days
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    audit_metadata = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ComplianceRecord {self.record_type}:{self.status}>'

class APIAudit(db.Model):
    """API usage auditing"""
    __tablename__ = 'api_audits'

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    api_key_id = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    request_size = db.Column(db.Integer, nullable=True)  # Bytes
    response_size = db.Column(db.Integer, nullable=True)  # Bytes
    response_time_ms = db.Column(db.Integer, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    rate_limit_hit = db.Column(db.Boolean, default=False)
    rate_limit_remaining = db.Column(db.Integer, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    audit_metadata = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<APIAudit {self.method} {self.endpoint}:{self.status_code}>'

class DocumentAudit(db.Model):
    """Document access and modification tracking"""
    __tablename__ = 'document_audits'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # view, download, edit, delete, share
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    version = db.Column(db.String(50), nullable=True)
    changes_made = db.Column(db.Text, nullable=True)  # JSON of changes
    shared_with = db.Column(db.Text, nullable=True)  # JSON of shared users
    audit_metadata = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<DocumentAudit {self.action} doc:{self.document_id} by {self.user_id}>'
