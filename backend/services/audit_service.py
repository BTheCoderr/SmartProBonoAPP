"""
Comprehensive audit service for system-wide auditing.
"""
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from flask import request, g, current_app
from database import db
from models.audit import (
    AuditLog, UserActivity, SecurityEvent, PerformanceMetric,
    ComplianceRecord, APIAudit, DocumentAudit,
    AuditEventType, AuditSeverity
)

logger = logging.getLogger(__name__)

class AuditService:
    """Centralized audit service for all system auditing needs."""
    
    def __init__(self):
        self.session_start_time = time.time()
    
    def log_audit_event(
        self,
        event_type: AuditEventType,
        action: str,
        user_id: Optional[int] = None,
        resource_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        description: Optional[str] = None,
        severity: AuditSeverity = AuditSeverity.LOW,
        metadata: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        status_code: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Log a general audit event."""
        try:
            # Get request context if available
            ip_address = getattr(request, 'remote_addr', None) if request else None
            user_agent = getattr(request, 'headers', {}).get('User-Agent') if request else None
            endpoint = getattr(request, 'path', None) if request else None
            method = getattr(request, 'method', None) if request else None
            session_id = getattr(g, 'session_id', None) if g else None
            
            # Use current user if not specified
            if not user_id and hasattr(g, 'user_id'):
                user_id = g.user_id
            
            audit_log = AuditLog(
                event_type=event_type,
                severity=severity,
                user_id=user_id,
                session_id=session_id,
                ip_address=ip_address,
                user_agent=user_agent,
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                request_data=json.dumps(request_data) if request_data else None,
                response_data=json.dumps(response_data) if response_data else None,
                error_message=error_message,
                processing_time_ms=processing_time_ms,
                resource_id=resource_id,
                resource_type=resource_type,
                action=action,
                description=description,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(audit_log)
            db.session.commit()
            
            logger.info(f"Audit event logged: {event_type.value}:{action} by user {user_id}")
            return audit_log
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {str(e)}")
            db.session.rollback()
            raise
    
    def log_user_activity(
        self,
        user_id: int,
        activity_type: str,
        page_url: Optional[str] = None,
        page_title: Optional[str] = None,
        action: Optional[str] = None,
        element_id: Optional[str] = None,
        element_class: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Log user activity."""
        try:
            # Get request context
            ip_address = getattr(request, 'remote_addr', None) if request else None
            user_agent = getattr(request, 'headers', {}).get('User-Agent') if request else None
            referrer = getattr(request, 'headers', {}).get('Referer') if request else None
            session_id = getattr(g, 'session_id', None) if g else None
            
            # Parse user agent for device info
            device_info = self._parse_user_agent(user_agent) if user_agent else {}
            
            activity = UserActivity(
                user_id=user_id,
                session_id=session_id,
                activity_type=activity_type,
                page_url=page_url,
                page_title=page_title,
                action=action,
                element_id=element_id,
                element_class=element_class,
                duration_seconds=duration_seconds,
                referrer=referrer,
                ip_address=ip_address,
                user_agent=user_agent,
                device_type=device_info.get('device_type'),
                browser=device_info.get('browser'),
                os=device_info.get('os'),
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(activity)
            db.session.commit()
            
            return activity
            
        except Exception as e:
            logger.error(f"Failed to log user activity: {str(e)}")
            db.session.rollback()
            raise
    
    def log_security_event(
        self,
        event_type: str,
        severity: AuditSeverity,
        user_id: Optional[int] = None,
        attack_type: Optional[str] = None,
        blocked: bool = False,
        reason: Optional[str] = None,
        response_action: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SecurityEvent:
        """Log security-related events."""
        try:
            # Get request context
            ip_address = getattr(request, 'remote_addr', None) if request else None
            user_agent = getattr(request, 'headers', {}).get('User-Agent') if request else None
            endpoint = getattr(request, 'path', None) if request else None
            
            security_event = SecurityEvent(
                event_type=event_type,
                severity=severity,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                endpoint=endpoint,
                attack_type=attack_type,
                blocked=blocked,
                reason=reason,
                response_action=response_action,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(security_event)
            db.session.commit()
            
            # Log critical security events
            if severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
                logger.warning(f"SECURITY ALERT: {event_type} - {reason}")
                self._send_security_alert(security_event)
            
            return security_event
            
        except Exception as e:
            logger.error(f"Failed to log security event: {str(e)}")
            db.session.rollback()
            raise
    
    def log_performance_metric(
        self,
        metric_type: str,
        value: float,
        unit: Optional[str] = None,
        threshold: Optional[float] = None,
        endpoint: Optional[str] = None,
        user_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetric:
        """Log performance metrics."""
        try:
            session_id = getattr(g, 'session_id', None) if g else None
            exceeded_threshold = threshold is not None and value > threshold
            
            metric = PerformanceMetric(
                metric_type=metric_type,
                endpoint=endpoint,
                value=value,
                unit=unit,
                threshold=threshold,
                exceeded_threshold=exceeded_threshold,
                user_id=user_id,
                session_id=session_id,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(metric)
            db.session.commit()
            
            # Alert if threshold exceeded
            if exceeded_threshold:
                logger.warning(f"Performance threshold exceeded: {metric_type} = {value}{unit}")
                self._send_performance_alert(metric)
            
            return metric
            
        except Exception as e:
            logger.error(f"Failed to log performance metric: {str(e)}")
            db.session.rollback()
            raise
    
    def log_api_usage(
        self,
        endpoint: str,
        method: str,
        response_time_ms: int,
        status_code: int,
        user_id: Optional[int] = None,
        api_key_id: Optional[str] = None,
        request_size: Optional[int] = None,
        response_size: Optional[int] = None,
        rate_limit_hit: bool = False,
        rate_limit_remaining: Optional[int] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> APIAudit:
        """Log API usage."""
        try:
            # Get request context
            ip_address = getattr(request, 'remote_addr', None) if request else None
            user_agent = getattr(request, 'headers', {}).get('User-Agent') if request else None
            
            api_audit = APIAudit(
                endpoint=endpoint,
                method=method,
                user_id=user_id,
                api_key_id=api_key_id,
                ip_address=ip_address,
                user_agent=user_agent,
                request_size=request_size,
                response_size=response_size,
                response_time_ms=response_time_ms,
                status_code=status_code,
                rate_limit_hit=rate_limit_hit,
                rate_limit_remaining=rate_limit_remaining,
                error_message=error_message,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(api_audit)
            db.session.commit()
            
            return api_audit
            
        except Exception as e:
            logger.error(f"Failed to log API usage: {str(e)}")
            db.session.rollback()
            raise
    
    def log_document_access(
        self,
        document_id: int,
        user_id: int,
        action: str,
        file_size: Optional[int] = None,
        processing_time_ms: Optional[int] = None,
        version: Optional[str] = None,
        changes_made: Optional[Dict[str, Any]] = None,
        shared_with: Optional[List[int]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentAudit:
        """Log document access and modifications."""
        try:
            # Get request context
            ip_address = getattr(request, 'remote_addr', None) if request else None
            user_agent = getattr(request, 'headers', {}).get('User-Agent') if request else None
            
            document_audit = DocumentAudit(
                document_id=document_id,
                user_id=user_id,
                action=action,
                ip_address=ip_address,
                user_agent=user_agent,
                file_size=file_size,
                processing_time_ms=processing_time_ms,
                version=version,
                changes_made=json.dumps(changes_made) if changes_made else None,
                shared_with=json.dumps(shared_with) if shared_with else None,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(document_audit)
            db.session.commit()
            
            return document_audit
            
        except Exception as e:
            logger.error(f"Failed to log document access: {str(e)}")
            db.session.rollback()
            raise
    
    def log_compliance_record(
        self,
        record_type: str,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None,
        status: str = "pending",
        description: Optional[str] = None,
        data_subject: Optional[str] = None,
        data_types: Optional[List[str]] = None,
        legal_basis: Optional[str] = None,
        retention_period: Optional[int] = None,
        processed_by: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ComplianceRecord:
        """Log compliance records."""
        try:
            record = ComplianceRecord(
                record_type=record_type,
                user_id=user_id,
                request_id=request_id,
                status=status,
                description=description,
                data_subject=data_subject,
                data_types=json.dumps(data_types) if data_types else None,
                legal_basis=legal_basis,
                retention_period=retention_period,
                processed_by=processed_by,
                processed_at=datetime.utcnow() if processed_by else None,
                audit_metadata=json.dumps(metadata) if metadata else None
            )
            
            db.session.add(record)
            db.session.commit()
            
            return record
            
        except Exception as e:
            logger.error(f"Failed to log compliance record: {str(e)}")
            db.session.rollback()
            raise
    
    def _parse_user_agent(self, user_agent: str) -> Dict[str, str]:
        """Parse user agent string for device information."""
        if not user_agent:
            return {}
        
        device_info = {}
        
        # Simple parsing - in production, use a proper user agent parser
        if 'Mobile' in user_agent or 'Android' in user_agent:
            device_info['device_type'] = 'mobile'
        elif 'Tablet' in user_agent or 'iPad' in user_agent:
            device_info['device_type'] = 'tablet'
        else:
            device_info['device_type'] = 'desktop'
        
        if 'Chrome' in user_agent:
            device_info['browser'] = 'Chrome'
        elif 'Firefox' in user_agent:
            device_info['browser'] = 'Firefox'
        elif 'Safari' in user_agent:
            device_info['browser'] = 'Safari'
        elif 'Edge' in user_agent:
            device_info['browser'] = 'Edge'
        
        if 'Windows' in user_agent:
            device_info['os'] = 'Windows'
        elif 'Mac' in user_agent:
            device_info['os'] = 'macOS'
        elif 'Linux' in user_agent:
            device_info['os'] = 'Linux'
        elif 'Android' in user_agent:
            device_info['os'] = 'Android'
        elif 'iOS' in user_agent:
            device_info['os'] = 'iOS'
        
        return device_info
    
    def _send_security_alert(self, security_event: SecurityEvent):
        """Send security alert notification."""
        logger.critical(f"SECURITY ALERT: {security_event.event_type} - {security_event.reason}")
        
        try:
            # Send email alert
            self._send_email_alert(security_event)
            
            # Send Slack alert if configured
            self._send_slack_alert(security_event)
            
            # Send webhook alert if configured
            self._send_webhook_alert(security_event)
            
            # Send WebSocket notification if available
            self._send_websocket_alert(security_event)
            
        except Exception as e:
            logger.error(f"Error sending security alert: {e}")
    
    def _send_performance_alert(self, metric: PerformanceMetric):
        """Send performance alert notification."""
        logger.warning(f"PERFORMANCE ALERT: {metric.metric_type} exceeded threshold")
        
        try:
            # Send email alert
            self._send_email_performance_alert(metric)
            
            # Send Slack alert if configured
            self._send_slack_performance_alert(metric)
            
            # Send webhook alert if configured
            self._send_webhook_performance_alert(metric)
            
            # Send WebSocket notification if available
            self._send_websocket_performance_alert(metric)
            
        except Exception as e:
            logger.error(f"Error sending performance alert: {e}")
    
    def get_audit_logs(
        self,
        event_type: Optional[AuditEventType] = None,
        user_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve audit logs with filtering."""
        query = AuditLog.query
        
        if event_type:
            query = query.filter(AuditLog.event_type == event_type)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)
        
        return query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    
    def get_security_events(
        self,
        severity: Optional[AuditSeverity] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[SecurityEvent]:
        """Retrieve security events with filtering."""
        query = SecurityEvent.query
        
        if severity:
            query = query.filter(SecurityEvent.severity == severity)
        if start_date:
            query = query.filter(SecurityEvent.created_at >= start_date)
        if end_date:
            query = query.filter(SecurityEvent.created_at <= end_date)
        
        return query.order_by(SecurityEvent.created_at.desc()).limit(limit).all()
    
    def get_user_activities(
        self,
        user_id: int,
        activity_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[UserActivity]:
        """Retrieve user activities with filtering."""
        query = UserActivity.query.filter(UserActivity.user_id == user_id)
        
        if activity_type:
            query = query.filter(UserActivity.activity_type == activity_type)
        if start_date:
            query = query.filter(UserActivity.created_at >= start_date)
        if end_date:
            query = query.filter(UserActivity.created_at <= end_date)
        
        return query.order_by(UserActivity.created_at.desc()).limit(limit).all()
    
    def _send_email_alert(self, security_event: SecurityEvent):
        """Send security alert via email."""
        try:
            import requests
            import os
            
            # Get email configuration
            email_api_key = os.environ.get('RESEND_API_KEY')
            if not email_api_key:
                logger.warning("RESEND_API_KEY not configured, skipping email alert")
                return
            
            # Prepare email content
            subject = f"🚨 SECURITY ALERT: {security_event.event_type}"
            
            html_content = f"""
            <h2>🚨 Security Alert</h2>
            <p><strong>Event Type:</strong> {security_event.event_type}</p>
            <p><strong>Severity:</strong> {security_event.severity}</p>
            <p><strong>Reason:</strong> {security_event.reason}</p>
            <p><strong>Timestamp:</strong> {security_event.timestamp}</p>
            <p><strong>User ID:</strong> {security_event.user_id or 'N/A'}</p>
            <p><strong>IP Address:</strong> {security_event.ip_address or 'N/A'}</p>
            <p><strong>User Agent:</strong> {security_event.user_agent or 'N/A'}</p>
            
            <h3>Details:</h3>
            <p>{security_event.details or 'No additional details available'}</p>
            
            <p><em>This is an automated security alert from SmartProBono.</em></p>
            """
            
            # Send email
            response = requests.post(
                'https://api.resend.com/emails',
                headers={'Authorization': f'Bearer {email_api_key}'},
                json={
                    'from': 'SmartProBono Security <security@smartprobono.org>',
                    'to': ['security@smartprobono.org', 'admin@smartprobono.org'],
                    'subject': subject,
                    'html': html_content
                }
            , timeout=30)
            
            if response.status_code == 200:
                logger.info("Security alert email sent successfully")
            else:
                logger.error(f"Failed to send security alert email: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending security alert email: {e}")
    
    def _send_slack_alert(self, security_event: SecurityEvent):
        """Send security alert to Slack."""
        try:
            import requests
            import os
            
            slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
            if not slack_webhook_url:
                logger.warning("SLACK_WEBHOOK_URL not configured, skipping Slack alert")
                return
            
            # Prepare Slack message
            color = "danger" if security_event.severity == "critical" else "warning"
            
            slack_message = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"🚨 Security Alert: {security_event.event_type}",
                        "fields": [
                            {"title": "Severity", "value": security_event.severity, "short": True},
                            {"title": "Reason", "value": security_event.reason, "short": False},
                            {"title": "Timestamp", "value": security_event.timestamp, "short": True},
                            {"title": "User ID", "value": str(security_event.user_id or "N/A"), "short": True},
                            {"title": "IP Address", "value": security_event.ip_address or "N/A", "short": True}
                        ],
                        "footer": "SmartProBono Security System",
                        "ts": int(security_event.timestamp.timestamp())
                    }
                ]
            }
            
            # Send to Slack
            response = requests.post(slack_webhook_url, json=slack_message, timeout=30)
            
            if response.status_code == 200:
                logger.info("Security alert sent to Slack successfully")
            else:
                logger.error(f"Failed to send security alert to Slack: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending security alert to Slack: {e}")
    
    def _send_webhook_alert(self, security_event: SecurityEvent):
        """Send security alert via webhook."""
        try:
            import requests
            import os
            
            webhook_url = os.environ.get('SECURITY_WEBHOOK_URL')
            if not webhook_url:
                logger.warning("SECURITY_WEBHOOK_URL not configured, skipping webhook alert")
                return
            
            # Prepare webhook payload
            payload = {
                "event_type": "security_alert",
                "timestamp": security_event.timestamp.isoformat(),
                "data": {
                    "event_type": security_event.event_type,
                    "severity": security_event.severity,
                    "reason": security_event.reason,
                    "user_id": security_event.user_id,
                    "ip_address": security_event.ip_address,
                    "user_agent": security_event.user_agent,
                    "details": security_event.details
                }
            }
            
            # Send webhook
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                logger.info("Security alert sent via webhook successfully")
            else:
                logger.error(f"Failed to send security alert via webhook: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending security alert via webhook: {e}")
    
    def _send_websocket_alert(self, security_event: SecurityEvent):
        """Send security alert via WebSocket."""
        try:
            # Import WebSocket functions
            from websocket_server import send_notification
            
            # Send real-time notification
            import asyncio
            import threading
            
            def send_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(send_notification(
                    "security_alert",
                    {
                        "event_type": security_event.event_type,
                        "severity": security_event.severity,
                        "reason": security_event.reason,
                        "timestamp": security_event.timestamp.isoformat(),
                        "user_id": security_event.user_id
                    }
                ))
                loop.close()
            
            thread = threading.Thread(target=send_async)
            thread.start()
            
            logger.info("Security alert sent via WebSocket")
            
        except Exception as e:
            logger.error(f"Error sending security alert via WebSocket: {e}")
    
    def _send_email_performance_alert(self, metric: PerformanceMetric):
        """Send performance alert via email."""
        try:
            import requests
            import os
            
            email_api_key = os.environ.get('RESEND_API_KEY')
            if not email_api_key:
                logger.warning("RESEND_API_KEY not configured, skipping performance email alert")
                return
            
            subject = f"⚠️ PERFORMANCE ALERT: {metric.metric_type}"
            
            html_content = f"""
            <h2>⚠️ Performance Alert</h2>
            <p><strong>Metric Type:</strong> {metric.metric_type}</p>
            <p><strong>Current Value:</strong> {metric.value}</p>
            <p><strong>Threshold:</strong> {metric.threshold}</p>
            <p><strong>Timestamp:</strong> {metric.timestamp}</p>
            <p><strong>Description:</strong> {metric.description or 'Performance metric exceeded threshold'}</p>
            
            <h3>Details:</h3>
            <p>This alert indicates that the system performance has degraded and may require attention.</p>
            
            <p><em>This is an automated performance alert from SmartProBono.</em></p>
            """
            
            response = requests.post(
                'https://api.resend.com/emails',
                headers={'Authorization': f'Bearer {email_api_key}'},
                json={
                    'from': 'SmartProBono Performance <performance@smartprobono.org>',
                    'to': ['performance@smartprobono.org', 'admin@smartprobono.org'],
                    'subject': subject,
                    'html': html_content
                }
            , timeout=30)
            
            if response.status_code == 200:
                logger.info("Performance alert email sent successfully")
            else:
                logger.error(f"Failed to send performance alert email: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending performance alert email: {e}")
    
    def _send_slack_performance_alert(self, metric: PerformanceMetric):
        """Send performance alert to Slack."""
        try:
            import requests
            import os
            
            slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
            if not slack_webhook_url:
                logger.warning("SLACK_WEBHOOK_URL not configured, skipping performance Slack alert")
                return
            
            slack_message = {
                "attachments": [
                    {
                        "color": "warning",
                        "title": f"⚠️ Performance Alert: {metric.metric_type}",
                        "fields": [
                            {"title": "Current Value", "value": str(metric.value), "short": True},
                            {"title": "Threshold", "value": str(metric.threshold), "short": True},
                            {"title": "Timestamp", "value": metric.timestamp, "short": True},
                            {"title": "Description", "value": metric.description or "Performance metric exceeded threshold", "short": False}
                        ],
                        "footer": "SmartProBono Performance Monitor",
                        "ts": int(metric.timestamp.timestamp())
                    }
                ]
            }
            
            response = requests.post(slack_webhook_url, json=slack_message, timeout=30)
            
            if response.status_code == 200:
                logger.info("Performance alert sent to Slack successfully")
            else:
                logger.error(f"Failed to send performance alert to Slack: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending performance alert to Slack: {e}")
    
    def _send_webhook_performance_alert(self, metric: PerformanceMetric):
        """Send performance alert via webhook."""
        try:
            import requests
            import os
            
            webhook_url = os.environ.get('PERFORMANCE_WEBHOOK_URL')
            if not webhook_url:
                logger.warning("PERFORMANCE_WEBHOOK_URL not configured, skipping performance webhook alert")
                return
            
            payload = {
                "event_type": "performance_alert",
                "timestamp": metric.timestamp.isoformat(),
                "data": {
                    "metric_type": metric.metric_type,
                    "value": metric.value,
                    "threshold": metric.threshold,
                    "description": metric.description
                }
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                logger.info("Performance alert sent via webhook successfully")
            else:
                logger.error(f"Failed to send performance alert via webhook: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending performance alert via webhook: {e}")
    
    def _send_websocket_performance_alert(self, metric: PerformanceMetric):
        """Send performance alert via WebSocket."""
        try:
            from websocket_server import send_notification
            
            import asyncio
            import threading
            
            def send_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(send_notification(
                    "performance_alert",
                    {
                        "metric_type": metric.metric_type,
                        "value": metric.value,
                        "threshold": metric.threshold,
                        "timestamp": metric.timestamp.isoformat(),
                        "description": metric.description
                    }
                ))
                loop.close()
            
            thread = threading.Thread(target=send_async)
            thread.start()
            
            logger.info("Performance alert sent via WebSocket")
            
        except Exception as e:
            logger.error(f"Error sending performance alert via WebSocket: {e}")

# Global audit service instance
audit_service = AuditService()
