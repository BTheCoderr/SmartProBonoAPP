"""
API auditing service for comprehensive API usage tracking and rate limiting.
"""
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from flask import request, g, current_app
from database import db
from models.audit import APIAudit, AuditEventType, AuditSeverity
from services.audit_service import audit_service
from services.alert_service import alert_service
from config.audit_config import AUDIT_CONFIG

logger = logging.getLogger(__name__)

class APIAuditService:
    """Service for auditing API usage and managing rate limits."""
    
    def __init__(self):
        self.rate_limit_cache = {}
        self.api_usage_patterns = {}
        self.endpoint_statistics = {}
        self.rate_limit_rules = AUDIT_CONFIG.get('api_auditing', {}).get('rate_limits', {})
    
    def log_api_request(
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
        """Log API request with comprehensive tracking."""
        try:
            # Log API audit
            api_audit = audit_service.log_api_usage(
                endpoint=endpoint,
                method=method,
                response_time_ms=response_time_ms,
                status_code=status_code,
                user_id=user_id,
                api_key_id=api_key_id,
                request_size=request_size,
                response_size=response_size,
                rate_limit_hit=rate_limit_hit,
                rate_limit_remaining=rate_limit_remaining,
                error_message=error_message,
                metadata=metadata
            )
            
            # Update endpoint statistics
            self._update_endpoint_statistics(endpoint, method, response_time_ms, status_code)
            
            # Track API usage patterns
            self._track_api_usage_pattern(user_id, endpoint, method, response_time_ms, status_code)
            
            # Check for API performance alerts
            self._check_api_performance_alerts(endpoint, response_time_ms, status_code)
            
            # Check for rate limit violations
            if rate_limit_hit:
                self._handle_rate_limit_violation(user_id, endpoint, method)
            
            return api_audit
            
        except Exception as e:
            logger.error(f"Error logging API request: {str(e)}")
            raise
    
    def check_rate_limit(
        self,
        user_id: Optional[int] = None,
        api_key_id: Optional[str] = None,
        endpoint: str = None,
        method: str = "GET"
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is within rate limits."""
        try:
            # Determine rate limit key
            if user_id:
                rate_limit_key = f"user_{user_id}"
            elif api_key_id:
                rate_limit_key = f"api_key_{api_key_id}"
            else:
                # Use IP address as fallback
                ip_address = request.remote_addr if request else "unknown"
                rate_limit_key = f"ip_{ip_address}"
            
            # Get rate limit rules for endpoint
            endpoint_rules = self.rate_limit_rules.get(endpoint, {})
            default_rules = self.rate_limit_rules.get('default', {'limit': 100, 'window': 3600})
            
            limit = endpoint_rules.get('limit', default_rules['limit'])
            window_seconds = endpoint_rules.get('window', default_rules['window'])
            
            # Check current usage
            current_usage = self._get_current_usage(rate_limit_key, window_seconds)
            
            # Check if limit exceeded
            within_limit = current_usage < limit
            remaining = max(0, limit - current_usage)
            
            # Update usage count
            if within_limit:
                self._increment_usage(rate_limit_key)
            
            return within_limit, {
                "limit": limit,
                "current_usage": current_usage,
                "remaining": remaining,
                "window_seconds": window_seconds,
                "reset_time": datetime.utcnow() + timedelta(seconds=window_seconds)
            }
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {str(e)}")
            return True, {"error": str(e)}
    
    def get_api_usage_summary(
        self,
        endpoint: Optional[str] = None,
        user_id: Optional[int] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get API usage summary for the specified period."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query API audits
            query = APIAudit.query.filter(
                APIAudit.created_at >= start_date
            )
            
            if endpoint:
                query = query.filter(APIAudit.endpoint == endpoint)
            
            if user_id:
                query = query.filter(APIAudit.user_id == user_id)
            
            audits = query.order_by(APIAudit.created_at.desc()).limit(1000).all()
            
            # Analyze API usage
            summary = {
                "endpoint": endpoint,
                "user_id": user_id,
                "period_days": days,
                "total_requests": len(audits),
                "requests_by_endpoint": {},
                "requests_by_method": {},
                "requests_by_user": {},
                "requests_by_status": {},
                "response_time_statistics": {},
                "rate_limit_violations": 0,
                "error_rate": 0,
                "api_usage_timeline": [],
                "top_endpoints": {},
                "top_users": {},
                "performance_metrics": {
                    "avg_response_time": 0,
                    "max_response_time": 0,
                    "min_response_time": 0,
                    "p95_response_time": 0,
                    "p99_response_time": 0
                }
            }
            
            response_times = []
            error_count = 0
            
            for audit in audits:
                # Count by endpoint
                endpoint = audit.endpoint
                summary["requests_by_endpoint"][endpoint] = summary["requests_by_endpoint"].get(endpoint, 0) + 1
                
                # Count by method
                method = audit.method
                summary["requests_by_method"][method] = summary["requests_by_method"].get(method, 0) + 1
                
                # Count by user
                user_id = audit.user_id
                if user_id:
                    summary["requests_by_user"][user_id] = summary["requests_by_user"].get(user_id, 0) + 1
                
                # Count by status
                status_code = audit.status_code
                status_range = f"{status_code // 100}xx"
                summary["requests_by_status"][status_range] = summary["requests_by_status"].get(status_range, 0) + 1
                
                # Track response times
                response_time = audit.response_time_ms
                if response_time:
                    response_times.append(response_time)
                
                # Count errors
                if status_code >= 400:
                    error_count += 1
                
                # Count rate limit violations
                if audit.rate_limit_hit:
                    summary["rate_limit_violations"] += 1
                
                # Track API usage timeline
                summary["api_usage_timeline"].append({
                    "timestamp": audit.created_at.isoformat(),
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": status_code,
                    "response_time_ms": response_time,
                    "user_id": user_id,
                    "rate_limit_hit": audit.rate_limit_hit
                })
            
            # Calculate error rate
            if len(audits) > 0:
                summary["error_rate"] = (error_count / len(audits)) * 100
            
            # Calculate response time statistics
            if response_times:
                response_times.sort()
                summary["performance_metrics"]["avg_response_time"] = sum(response_times) / len(response_times)
                summary["performance_metrics"]["max_response_time"] = max(response_times)
                summary["performance_metrics"]["min_response_time"] = min(response_times)
                
                # Calculate percentiles
                p95_index = int(len(response_times) * 0.95)
                p99_index = int(len(response_times) * 0.99)
                summary["performance_metrics"]["p95_response_time"] = response_times[p95_index] if p95_index < len(response_times) else response_times[-1]
                summary["performance_metrics"]["p99_response_time"] = response_times[p99_index] if p99_index < len(response_times) else response_times[-1]
            
            # Sort dictionaries by count
            summary["requests_by_endpoint"] = dict(sorted(summary["requests_by_endpoint"].items(), key=lambda x: x[1], reverse=True))
            summary["requests_by_method"] = dict(sorted(summary["requests_by_method"].items(), key=lambda x: x[1], reverse=True))
            summary["requests_by_user"] = dict(sorted(summary["requests_by_user"].items(), key=lambda x: x[1], reverse=True))
            
            # Get top endpoints and users
            summary["top_endpoints"] = dict(list(summary["requests_by_endpoint"].items())[:10])
            summary["top_users"] = dict(list(summary["requests_by_user"].items())[:10])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting API usage summary: {str(e)}")
            return {"error": str(e)}
    
    def get_rate_limit_status(
        self,
        user_id: Optional[int] = None,
        api_key_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get current rate limit status for user or API key."""
        try:
            # Determine rate limit key
            if user_id:
                rate_limit_key = f"user_{user_id}"
            elif api_key_id:
                rate_limit_key = f"api_key_{api_key_id}"
            else:
                return {"error": "Either user_id or api_key_id must be provided"}
            
            # Get all rate limit rules
            status = {
                "rate_limit_key": rate_limit_key,
                "endpoints": {},
                "overall_status": "within_limits"
            }
            
            for endpoint, rules in self.rate_limit_rules.items():
                if endpoint == 'default':
                    continue
                
                limit = rules.get('limit', 100)
                window_seconds = rules.get('window', 3600)
                
                current_usage = self._get_current_usage(rate_limit_key, window_seconds)
                remaining = max(0, limit - current_usage)
                within_limit = current_usage < limit
                
                status["endpoints"][endpoint] = {
                    "limit": limit,
                    "current_usage": current_usage,
                    "remaining": remaining,
                    "within_limit": within_limit,
                    "window_seconds": window_seconds,
                    "reset_time": datetime.utcnow() + timedelta(seconds=window_seconds)
                }
                
                if not within_limit:
                    status["overall_status"] = "rate_limited"
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting rate limit status: {str(e)}")
            return {"error": str(e)}
    
    def get_api_performance_metrics(
        self,
        endpoint: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get API performance metrics."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query API audits
            query = APIAudit.query.filter(
                APIAudit.created_at >= start_date
            )
            
            if endpoint:
                query = query.filter(APIAudit.endpoint == endpoint)
            
            audits = query.all()
            
            # Calculate performance metrics
            metrics = {
                "endpoint": endpoint,
                "period_days": days,
                "total_requests": len(audits),
                "response_times": {
                    "avg_ms": 0,
                    "min_ms": 0,
                    "max_ms": 0,
                    "p50_ms": 0,
                    "p95_ms": 0,
                    "p99_ms": 0
                },
                "throughput": {
                    "requests_per_minute": 0,
                    "requests_per_hour": 0,
                    "requests_per_day": 0
                },
                "error_rates": {
                    "4xx_rate": 0,
                    "5xx_rate": 0,
                    "overall_error_rate": 0
                },
                "rate_limiting": {
                    "rate_limit_hits": 0,
                    "rate_limit_hit_rate": 0
                }
            }
            
            if not audits:
                return metrics
            
            # Calculate response time metrics
            response_times = [audit.response_time_ms for audit in audits if audit.response_time_ms]
            if response_times:
                response_times.sort()
                metrics["response_times"]["avg_ms"] = sum(response_times) / len(response_times)
                metrics["response_times"]["min_ms"] = min(response_times)
                metrics["response_times"]["max_ms"] = max(response_times)
                metrics["response_times"]["p50_ms"] = response_times[int(len(response_times) * 0.5)]
                metrics["response_times"]["p95_ms"] = response_times[int(len(response_times) * 0.95)]
                metrics["response_times"]["p99_ms"] = response_times[int(len(response_times) * 0.99)]
            
            # Calculate throughput
            total_seconds = (datetime.utcnow() - start_date).total_seconds()
            if total_seconds > 0:
                metrics["throughput"]["requests_per_minute"] = len(audits) / (total_seconds / 60)
                metrics["throughput"]["requests_per_hour"] = len(audits) / (total_seconds / 3600)
                metrics["throughput"]["requests_per_day"] = len(audits) / (total_seconds / 86400)
            
            # Calculate error rates
            error_4xx = sum(1 for audit in audits if 400 <= audit.status_code < 500)
            error_5xx = sum(1 for audit in audits if 500 <= audit.status_code < 600)
            total_errors = error_4xx + error_5xx
            
            metrics["error_rates"]["4xx_rate"] = (error_4xx / len(audits)) * 100
            metrics["error_rates"]["5xx_rate"] = (error_5xx / len(audits)) * 100
            metrics["error_rates"]["overall_error_rate"] = (total_errors / len(audits)) * 100
            
            # Calculate rate limiting metrics
            rate_limit_hits = sum(1 for audit in audits if audit.rate_limit_hit)
            metrics["rate_limiting"]["rate_limit_hits"] = rate_limit_hits
            metrics["rate_limiting"]["rate_limit_hit_rate"] = (rate_limit_hits / len(audits)) * 100
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting API performance metrics: {str(e)}")
            return {"error": str(e)}
    
    def _update_endpoint_statistics(self, endpoint: str, method: str, response_time_ms: int, status_code: int):
        """Update endpoint statistics."""
        try:
            key = f"{endpoint}_{method}"
            if key not in self.endpoint_statistics:
                self.endpoint_statistics[key] = {
                    "request_count": 0,
                    "total_response_time": 0,
                    "min_response_time": float('inf'),
                    "max_response_time": 0,
                    "error_count": 0,
                    "last_updated": datetime.utcnow()
                }
            
            stats = self.endpoint_statistics[key]
            stats["request_count"] += 1
            stats["total_response_time"] += response_time_ms
            stats["min_response_time"] = min(stats["min_response_time"], response_time_ms)
            stats["max_response_time"] = max(stats["max_response_time"], response_time_ms)
            stats["last_updated"] = datetime.utcnow()
            
            if status_code >= 400:
                stats["error_count"] += 1
            
        except Exception as e:
            logger.error(f"Error updating endpoint statistics: {str(e)}")
    
    def _track_api_usage_pattern(self, user_id: Optional[int], endpoint: str, method: str, response_time_ms: int, status_code: int):
        """Track API usage patterns."""
        try:
            if not user_id:
                return
            
            key = f"user_{user_id}"
            if key not in self.api_usage_patterns:
                self.api_usage_patterns[key] = {
                    "endpoints": {},
                    "methods": {},
                    "response_times": [],
                    "error_count": 0,
                    "last_activity": datetime.utcnow()
                }
            
            pattern = self.api_usage_patterns[key]
            pattern["endpoints"][endpoint] = pattern["endpoints"].get(endpoint, 0) + 1
            pattern["methods"][method] = pattern["methods"].get(method, 0) + 1
            pattern["response_times"].append(response_time_ms)
            pattern["last_activity"] = datetime.utcnow()
            
            if status_code >= 400:
                pattern["error_count"] += 1
            
            # Keep only last 1000 response times
            if len(pattern["response_times"]) > 1000:
                pattern["response_times"] = pattern["response_times"][-1000:]
            
        except Exception as e:
            logger.error(f"Error tracking API usage pattern: {str(e)}")
    
    def _check_api_performance_alerts(self, endpoint: str, response_time_ms: int, status_code: int):
        """Check for API performance alerts."""
        try:
            # Check response time alerts
            if response_time_ms > 5000:  # 5 seconds
                alert_service.send_performance_alert(
                    "api_response_time",
                    response_time_ms,
                    "ms",
                    endpoint
                )
            
            # Check error rate alerts
            if status_code >= 500:
                alert_service.send_performance_alert(
                    "api_error_rate",
                    100,  # 100% error for this request
                    "%",
                    endpoint
                )
            
        except Exception as e:
            logger.error(f"Error checking API performance alerts: {str(e)}")
    
    def _handle_rate_limit_violation(self, user_id: Optional[int], endpoint: str, method: str):
        """Handle rate limit violation."""
        try:
            # Log security event
            audit_service.log_audit_event(
                event_type=AuditEventType.SECURITY,
                action="RATE_LIMIT_VIOLATION",
                user_id=user_id,
                description=f"Rate limit violation: {method} {endpoint}",
                severity=AuditSeverity.MEDIUM,
                metadata={
                    "endpoint": endpoint,
                    "method": method,
                    "user_id": user_id
                }
            )
            
            # Send alert
            alert_service.send_performance_alert(
                "rate_limit_violation",
                100,  # 100% rate limit hit
                "%",
                endpoint
            )
            
        except Exception as e:
            logger.error(f"Error handling rate limit violation: {str(e)}")
    
    def _get_current_usage(self, rate_limit_key: str, window_seconds: int) -> int:
        """Get current usage count for rate limit key."""
        try:
            if rate_limit_key not in self.rate_limit_cache:
                return 0
            
            # Get current time
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=window_seconds)
            
            # Count requests within window
            usage_count = 0
            for timestamp in self.rate_limit_cache[rate_limit_key]:
                if timestamp >= window_start:
                    usage_count += 1
            
            return usage_count
            
        except Exception as e:
            logger.error(f"Error getting current usage: {str(e)}")
            return 0
    
    def _increment_usage(self, rate_limit_key: str):
        """Increment usage count for rate limit key."""
        try:
            if rate_limit_key not in self.rate_limit_cache:
                self.rate_limit_cache[rate_limit_key] = []
            
            # Add current timestamp
            self.rate_limit_cache[rate_limit_key].append(datetime.utcnow())
            
            # Clean up old entries (older than 24 hours)
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            self.rate_limit_cache[rate_limit_key] = [
                timestamp for timestamp in self.rate_limit_cache[rate_limit_key]
                if timestamp >= cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error incrementing usage: {str(e)}")

# Global API audit service instance
api_audit_service = APIAuditService()
