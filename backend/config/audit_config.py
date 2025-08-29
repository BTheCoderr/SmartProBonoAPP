"""
Audit configuration for comprehensive system auditing.
"""
from typing import Dict, List, Any
from datetime import timedelta

# Audit configuration
AUDIT_CONFIG = {
    # General audit settings
    'enabled': True,
    'log_level': 'INFO',
    'retention_days': 90,
    'security_retention_days': 365,
    'compliance_retention_days': 2555,  # 7 years
    
    # Performance monitoring
    'performance_monitoring': {
        'enabled': True,
        'response_time_threshold_ms': 1000,
        'memory_usage_threshold_percent': 80,
        'cpu_usage_threshold_percent': 70,
        'database_query_threshold_ms': 500,
        'alert_on_threshold_exceeded': True
    },
    
    # Security monitoring
    'security_monitoring': {
        'enabled': True,
        'failed_login_threshold': 5,
        'failed_login_window_minutes': 15,
        'suspicious_activity_detection': True,
        'ip_blocking_enabled': True,
        'rate_limiting_enabled': True,
        'alert_on_security_events': True
    },
    
    # Data access auditing
    'data_access_auditing': {
        'enabled': True,
        'log_all_queries': False,  # Set to True for detailed query logging
        'log_sensitive_data_access': True,
        'log_bulk_operations': True,
        'log_data_exports': True,
        'log_data_deletions': True
    },
    
    # User activity tracking
    'user_activity_tracking': {
        'enabled': True,
        'track_page_views': True,
        'track_clicks': True,
        'track_form_submissions': True,
        'track_file_downloads': True,
        'track_search_queries': True,
        'session_tracking': True,
        'device_fingerprinting': True
    },
    
    # API auditing
    'api_auditing': {
        'enabled': True,
        'log_all_requests': True,
        'log_request_payloads': True,
        'log_response_payloads': False,  # Set to True for debugging
        'log_headers': True,
        'rate_limit_tracking': True,
        'error_tracking': True
    },
    
    # Document auditing
    'document_auditing': {
        'enabled': True,
        'track_document_views': True,
        'track_document_downloads': True,
        'track_document_edits': True,
        'track_document_sharing': True,
        'track_document_deletions': True,
        'version_control': True,
        'change_tracking': True
    },
    
    # Compliance auditing
    'compliance_auditing': {
        'enabled': True,
        'gdpr_compliance': True,
        'ccpa_compliance': True,
        'data_retention_tracking': True,
        'consent_tracking': True,
        'data_subject_requests': True,
        'breach_notification': True
    },
    
    # Alerting configuration
    'alerting': {
        'enabled': True,
        'email_alerts': {
            'enabled': True,
            'recipients': ['admin@smartprobono.org', 'security@smartprobono.org'],
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'use_tls': True
        },
        'webhook_alerts': {
            'enabled': False,
            'url': None,
            'secret': None
        },
        'slack_alerts': {
            'enabled': False,
            'webhook_url': None,
            'channel': '#security-alerts'
        }
    },
    
    # Sensitive data handling
    'sensitive_data': {
        'fields_to_redact': [
            'password', 'token', 'secret', 'key', 'ssn', 'credit_card',
            'bank_account', 'api_key', 'auth_token', 'session_id'
        ],
        'headers_to_redact': [
            'authorization', 'cookie', 'x-api-key', 'x-auth-token'
        ],
        'endpoints_to_exclude': [
            '/api/auth/login', '/api/auth/register', '/api/auth/reset-password'
        ]
    },
    
    # Database configuration
    'database': {
        'audit_table_prefix': 'audit_',
        'batch_insert_size': 100,
        'async_logging': True,
        'connection_pool_size': 10
    },
    
    # Real-time monitoring
    'real_time_monitoring': {
        'enabled': True,
        'websocket_updates': True,
        'dashboard_refresh_interval_seconds': 30,
        'live_alerts': True
    }
}

# Audit event types and their configurations
AUDIT_EVENT_CONFIGS = {
    'security': {
        'enabled': True,
        'severity_threshold': 'medium',
        'alert_immediately': True,
        'retention_days': 365
    },
    'user_activity': {
        'enabled': True,
        'severity_threshold': 'low',
        'alert_immediately': False,
        'retention_days': 90
    },
    'data_access': {
        'enabled': True,
        'severity_threshold': 'medium',
        'alert_immediately': False,
        'retention_days': 180
    },
    'data_modification': {
        'enabled': True,
        'severity_threshold': 'medium',
        'alert_immediately': True,
        'retention_days': 180
    },
    'performance': {
        'enabled': True,
        'severity_threshold': 'high',
        'alert_immediately': True,
        'retention_days': 30
    },
    'api_usage': {
        'enabled': True,
        'severity_threshold': 'low',
        'alert_immediately': False,
        'retention_days': 90
    },
    'document_access': {
        'enabled': True,
        'severity_threshold': 'medium',
        'alert_immediately': False,
        'retention_days': 180
    },
    'compliance': {
        'enabled': True,
        'severity_threshold': 'high',
        'alert_immediately': True,
        'retention_days': 2555  # 7 years
    },
    'system': {
        'enabled': True,
        'severity_threshold': 'medium',
        'alert_immediately': False,
        'retention_days': 90
    }
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'response_time': {
        'warning_ms': 500,
        'critical_ms': 1000,
        'alert_ms': 2000
    },
    'memory_usage': {
        'warning_percent': 70,
        'critical_percent': 80,
        'alert_percent': 90
    },
    'cpu_usage': {
        'warning_percent': 60,
        'critical_percent': 70,
        'alert_percent': 80
    },
    'database_queries': {
        'warning_ms': 200,
        'critical_ms': 500,
        'alert_ms': 1000
    },
    'file_operations': {
        'warning_ms': 1000,
        'critical_ms': 5000,
        'alert_ms': 10000
    }
}

# Security thresholds
SECURITY_THRESHOLDS = {
    'failed_logins': {
        'warning_count': 3,
        'critical_count': 5,
        'alert_count': 10,
        'window_minutes': 15
    },
    'suspicious_requests': {
        'warning_count': 10,
        'critical_count': 20,
        'alert_count': 50,
        'window_minutes': 60
    },
    'rate_limit_violations': {
        'warning_count': 5,
        'critical_count': 10,
        'alert_count': 20,
        'window_minutes': 60
    },
    'unauthorized_access_attempts': {
        'warning_count': 1,
        'critical_count': 3,
        'alert_count': 5,
        'window_minutes': 60
    }
}

# Compliance requirements
COMPLIANCE_REQUIREMENTS = {
    'gdpr': {
        'data_retention_days': 2555,  # 7 years
        'consent_tracking_required': True,
        'data_subject_rights': True,
        'breach_notification_hours': 72,
        'privacy_by_design': True
    },
    'ccpa': {
        'data_retention_days': 1095,  # 3 years
        'opt_out_tracking': True,
        'data_sale_tracking': True,
        'consumer_rights': True
    },
    'hipaa': {
        'data_retention_days': 2555,  # 7 years
        'access_logging_required': True,
        'audit_trail_required': True,
        'encryption_required': True
    },
    'sox': {
        'data_retention_days': 2555,  # 7 years
        'financial_data_tracking': True,
        'change_control_required': True,
        'segregation_of_duties': True
    }
}

# Alert templates
ALERT_TEMPLATES = {
    'security_breach': {
        'subject': 'Security Alert: {event_type}',
        'body': '''
Security Event Detected:

Event Type: {event_type}
Severity: {severity}
Time: {timestamp}
User: {user_id}
IP Address: {ip_address}
Description: {description}

Please investigate immediately.

SmartProBono Security System
        ''',
        'priority': 'high'
    },
    'performance_degradation': {
        'subject': 'Performance Alert: {metric_type}',
        'body': '''
Performance Threshold Exceeded:

Metric: {metric_type}
Value: {value} {unit}
Threshold: {threshold} {unit}
Time: {timestamp}
Endpoint: {endpoint}

Please investigate performance issues.

SmartProBono Monitoring System
        ''',
        'priority': 'medium'
    },
    'compliance_violation': {
        'subject': 'Compliance Alert: {record_type}',
        'body': '''
Compliance Event:

Record Type: {record_type}
Status: {status}
Time: {timestamp}
User: {user_id}
Description: {description}

Please review compliance requirements.

SmartProBono Compliance System
        ''',
        'priority': 'high'
    }
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    'default_time_range_hours': 24,
    'refresh_interval_seconds': 30,
    'max_data_points': 1000,
    'charts': {
        'enabled': True,
        'types': ['line', 'bar', 'pie', 'area'],
        'colors': ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
    },
    'widgets': {
        'security_events': True,
        'performance_metrics': True,
        'user_activities': True,
        'api_usage': True,
        'compliance_status': True,
        'system_health': True
    }
}

# Export configuration
EXPORT_CONFIG = {
    'formats': ['csv', 'json', 'xlsx'],
    'max_records_per_export': 10000,
    'compression_enabled': True,
    'encryption_enabled': True,
    'retention_days': 30
}

# Integration configuration
INTEGRATION_CONFIG = {
    'external_apis': {
        'enabled': False,
        'endpoints': [],
        'authentication': {
            'type': 'bearer',
            'token': None
        }
    },
    'webhooks': {
        'enabled': False,
        'endpoints': [],
        'retry_attempts': 3,
        'timeout_seconds': 30
    },
    'siem_integration': {
        'enabled': False,
        'endpoint': None,
        'format': 'cef',
        'authentication': {
            'type': 'basic',
            'username': None,
            'password': None
        }
    }
}
