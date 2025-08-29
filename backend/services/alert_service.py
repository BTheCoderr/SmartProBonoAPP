"""
Real-time alerting service for audit events.
"""
import logging
import smtplib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from database import db
from models.audit import SecurityEvent, AuditLog, AuditSeverity
from config.audit_config import (
    AUDIT_CONFIG, ALERT_TEMPLATES, SECURITY_THRESHOLDS,
    PERFORMANCE_THRESHOLDS, COMPLIANCE_REQUIREMENTS
)

logger = logging.getLogger(__name__)

class AlertService:
    """Service for managing real-time alerts and notifications."""
    
    def __init__(self):
        self.alert_history = []
        self.rate_limits = {}
    
    def check_and_send_alerts(self, audit_event: AuditLog):
        """Check if an audit event should trigger an alert and send it."""
        try:
            # Check if alerting is enabled
            if not AUDIT_CONFIG.get('alerting', {}).get('enabled', False):
                return
            
            # Determine alert type based on event
            alert_type = self._determine_alert_type(audit_event)
            
            if alert_type:
                # Check rate limiting
                if self._is_rate_limited(alert_type, audit_event):
                    return
                
                # Send alert
                self._send_alert(alert_type, audit_event)
                
                # Record alert in history
                self._record_alert(alert_type, audit_event)
                
        except Exception as e:
            logger.error(f"Error in alert service: {str(e)}")
    
    def check_security_thresholds(self, event_type: str, count: int, window_minutes: int = 15):
        """Check if security thresholds have been exceeded."""
        try:
            thresholds = SECURITY_THRESHOLDS.get(event_type, {})
            
            if count >= thresholds.get('alert_count', float('inf')):
                return 'critical'
            elif count >= thresholds.get('critical_count', float('inf')):
                return 'high'
            elif count >= thresholds.get('warning_count', float('inf')):
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error checking security thresholds: {str(e)}")
            return 'low'
    
    def check_performance_thresholds(self, metric_type: str, value: float, unit: str = ''):
        """Check if performance thresholds have been exceeded."""
        try:
            thresholds = PERFORMANCE_THRESHOLDS.get(metric_type, {})
            
            if value >= thresholds.get('alert_ms', float('inf')):
                return 'critical'
            elif value >= thresholds.get('critical_ms', float('inf')):
                return 'high'
            elif value >= thresholds.get('warning_ms', float('inf')):
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error checking performance thresholds: {str(e)}")
            return 'low'
    
    def send_security_alert(self, security_event: SecurityEvent):
        """Send security alert immediately."""
        try:
            if security_event.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
                self._send_email_alert('security_breach', {
                    'event_type': security_event.event_type,
                    'severity': security_event.severity.value,
                    'timestamp': security_event.created_at.isoformat(),
                    'user_id': security_event.user_id,
                    'ip_address': security_event.ip_address,
                    'description': security_event.reason
                })
                
                # Send to webhook if configured
                self._send_webhook_alert('security_breach', {
                    'event_type': security_event.event_type,
                    'severity': security_event.severity.value,
                    'timestamp': security_event.created_at.isoformat(),
                    'user_id': security_event.user_id,
                    'ip_address': security_event.ip_address,
                    'description': security_event.reason,
                    'blocked': security_event.blocked,
                    'response_action': security_event.response_action
                })
                
        except Exception as e:
            logger.error(f"Error sending security alert: {str(e)}")
    
    def send_performance_alert(self, metric_type: str, value: float, unit: str, endpoint: str = None):
        """Send performance alert."""
        try:
            severity = self.check_performance_thresholds(metric_type, value, unit)
            
            if severity in ['high', 'critical']:
                self._send_email_alert('performance_degradation', {
                    'metric_type': metric_type,
                    'value': value,
                    'unit': unit,
                    'threshold': PERFORMANCE_THRESHOLDS.get(metric_type, {}).get('critical_ms', 'N/A'),
                    'timestamp': datetime.utcnow().isoformat(),
                    'endpoint': endpoint or 'N/A'
                })
                
        except Exception as e:
            logger.error(f"Error sending performance alert: {str(e)}")
    
    def send_compliance_alert(self, record_type: str, status: str, user_id: int = None, description: str = None):
        """Send compliance alert."""
        try:
            self._send_email_alert('compliance_violation', {
                'record_type': record_type,
                'status': status,
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': user_id,
                'description': description
            })
            
        except Exception as e:
            logger.error(f"Error sending compliance alert: {str(e)}")
    
    def _determine_alert_type(self, audit_event: AuditLog) -> Optional[str]:
        """Determine what type of alert should be sent for an audit event."""
        try:
            # Security events
            if audit_event.event_type.value == 'security':
                if audit_event.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
                    return 'security_breach'
            
            # Performance events
            elif audit_event.event_type.value == 'performance':
                if audit_event.processing_time_ms and audit_event.processing_time_ms > 2000:
                    return 'performance_degradation'
            
            # Compliance events
            elif audit_event.event_type.value == 'compliance':
                return 'compliance_violation'
            
            # Data modification events
            elif audit_event.event_type.value == 'data_modification':
                if audit_event.action in ['DELETE', 'BULK_DELETE']:
                    return 'data_modification'
            
            return None
            
        except Exception as e:
            logger.error(f"Error determining alert type: {str(e)}")
            return None
    
    def _is_rate_limited(self, alert_type: str, audit_event: AuditLog) -> bool:
        """Check if alerts are rate limited."""
        try:
            # Simple rate limiting - max 1 alert per type per 5 minutes
            now = datetime.utcnow()
            key = f"{alert_type}_{audit_event.user_id}_{audit_event.ip_address}"
            
            if key in self.rate_limits:
                last_alert = self.rate_limits[key]
                if now - last_alert < timedelta(minutes=5):
                    return True
            
            self.rate_limits[key] = now
            return False
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {str(e)}")
            return False
    
    def _send_alert(self, alert_type: str, audit_event: AuditLog):
        """Send alert based on type."""
        try:
            if alert_type == 'security_breach':
                self._send_security_alert_data(alert_type, audit_event)
            elif alert_type == 'performance_degradation':
                self._send_performance_alert_data(alert_type, audit_event)
            elif alert_type == 'compliance_violation':
                self._send_compliance_alert_data(alert_type, audit_event)
            elif alert_type == 'data_modification':
                self._send_data_modification_alert_data(alert_type, audit_event)
                
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
    
    def _send_security_alert_data(self, alert_type: str, audit_event: AuditLog):
        """Send security alert with audit event data."""
        try:
            data = {
                'event_type': audit_event.event_type.value,
                'severity': audit_event.severity.value,
                'timestamp': audit_event.created_at.isoformat(),
                'user_id': audit_event.user_id,
                'ip_address': audit_event.ip_address,
                'description': audit_event.description,
                'endpoint': audit_event.endpoint,
                'action': audit_event.action
            }
            
            self._send_email_alert(alert_type, data)
            self._send_webhook_alert(alert_type, data)
            
        except Exception as e:
            logger.error(f"Error sending security alert data: {str(e)}")
    
    def _send_performance_alert_data(self, alert_type: str, audit_event: AuditLog):
        """Send performance alert with audit event data."""
        try:
            data = {
                'metric_type': 'response_time',
                'value': audit_event.processing_time_ms,
                'unit': 'ms',
                'threshold': 1000,
                'timestamp': audit_event.created_at.isoformat(),
                'endpoint': audit_event.endpoint
            }
            
            self._send_email_alert(alert_type, data)
            
        except Exception as e:
            logger.error(f"Error sending performance alert data: {str(e)}")
    
    def _send_compliance_alert_data(self, alert_type: str, audit_event: AuditLog):
        """Send compliance alert with audit event data."""
        try:
            data = {
                'record_type': audit_event.resource_type or 'unknown',
                'status': audit_event.action,
                'timestamp': audit_event.created_at.isoformat(),
                'user_id': audit_event.user_id,
                'description': audit_event.description
            }
            
            self._send_email_alert(alert_type, data)
            
        except Exception as e:
            logger.error(f"Error sending compliance alert data: {str(e)}")
    
    def _send_data_modification_alert_data(self, alert_type: str, audit_event: AuditLog):
        """Send data modification alert with audit event data."""
        try:
            data = {
                'event_type': 'data_modification',
                'action': audit_event.action,
                'resource_type': audit_event.resource_type,
                'resource_id': audit_event.resource_id,
                'timestamp': audit_event.created_at.isoformat(),
                'user_id': audit_event.user_id,
                'description': audit_event.description
            }
            
            self._send_email_alert(alert_type, data)
            
        except Exception as e:
            logger.error(f"Error sending data modification alert data: {str(e)}")
    
    def _send_email_alert(self, alert_type: str, data: Dict[str, Any]):
        """Send email alert."""
        try:
            email_config = AUDIT_CONFIG.get('alerting', {}).get('email_alerts', {})
            
            if not email_config.get('enabled', False):
                return
            
            template = ALERT_TEMPLATES.get(alert_type, {})
            if not template:
                return
            
            # Format email content
            subject = template.get('subject', 'Alert').format(**data)
            body = template.get('body', 'Alert triggered').format(**data)
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = email_config.get('from', 'noreply@smartprobono.org')
            msg['To'] = ', '.join(email_config.get('recipients', []))
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(email_config.get('smtp_server', 'localhost'), 
                                email_config.get('smtp_port', 587))
            
            if email_config.get('use_tls', True):
                server.starttls()
            
            # Note: In production, use proper authentication
            # server.login(email_config.get('username'), email_config.get('password'))
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error sending email alert: {str(e)}")
    
    def _send_webhook_alert(self, alert_type: str, data: Dict[str, Any]):
        """Send webhook alert."""
        try:
            webhook_config = AUDIT_CONFIG.get('alerting', {}).get('webhook_alerts', {})
            
            if not webhook_config.get('enabled', False):
                return
            
            webhook_url = webhook_config.get('url')
            if not webhook_url:
                return
            
            import requests
            
            payload = {
                'alert_type': alert_type,
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            if webhook_config.get('secret'):
                headers['Authorization'] = f"Bearer {webhook_config['secret']}"
            
            response = requests.post(webhook_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Webhook alert sent: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error sending webhook alert: {str(e)}")
    
    def _send_slack_alert(self, alert_type: str, data: Dict[str, Any]):
        """Send Slack alert."""
        try:
            slack_config = AUDIT_CONFIG.get('alerting', {}).get('slack_alerts', {})
            
            if not slack_config.get('enabled', False):
                return
            
            webhook_url = slack_config.get('webhook_url')
            if not webhook_url:
                return
            
            import requests
            
            # Format Slack message
            template = ALERT_TEMPLATES.get(alert_type, {})
            message = template.get('body', 'Alert triggered').format(**data)
            
            payload = {
                'channel': slack_config.get('channel', '#security-alerts'),
                'text': f"🚨 {template.get('subject', 'Alert')}",
                'attachments': [{
                    'color': 'danger' if alert_type == 'security_breach' else 'warning',
                    'text': message,
                    'footer': 'SmartProBono Security System',
                    'ts': int(datetime.utcnow().timestamp())
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Slack alert sent: {alert_type}")
            
        except Exception as e:
            logger.error(f"Error sending Slack alert: {str(e)}")
    
    def _record_alert(self, alert_type: str, audit_event: AuditLog):
        """Record alert in history."""
        try:
            alert_record = {
                'alert_type': alert_type,
                'audit_event_id': audit_event.id,
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': audit_event.user_id,
                'ip_address': audit_event.ip_address,
                'severity': audit_event.severity.value
            }
            
            self.alert_history.append(alert_record)
            
            # Keep only last 1000 alerts in memory
            if len(self.alert_history) > 1000:
                self.alert_history = self.alert_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error recording alert: {str(e)}")
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history."""
        return self.alert_history[-limit:]
    
    def get_alert_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get alert statistics for the specified time period."""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Filter alerts by time
            recent_alerts = [
                alert for alert in self.alert_history
                if datetime.fromisoformat(alert['timestamp']) >= cutoff_time
            ]
            
            # Count by type
            alert_counts = {}
            for alert in recent_alerts:
                alert_type = alert['alert_type']
                alert_counts[alert_type] = alert_counts.get(alert_type, 0) + 1
            
            return {
                'total_alerts': len(recent_alerts),
                'alerts_by_type': alert_counts,
                'time_period_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Error getting alert statistics: {str(e)}")
            return {'total_alerts': 0, 'alerts_by_type': {}, 'time_period_hours': hours}

# Global alert service instance
alert_service = AlertService()
