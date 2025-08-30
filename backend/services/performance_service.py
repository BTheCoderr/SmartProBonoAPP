"""
Performance monitoring service for system performance tracking and optimization.
"""
import time
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available. Performance monitoring will be limited.")
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from flask import request, g, current_app
from database import db
from models.audit import PerformanceMetric, AuditEventType, AuditSeverity
from services.audit_service import audit_service
from services.alert_service import alert_service
from config.audit_config import PERFORMANCE_THRESHOLDS

logger = logging.getLogger(__name__)

class PerformanceService:
    """Service for monitoring and tracking system performance."""
    
    def __init__(self):
        self.metrics_cache = {}
        self.performance_history = {}
        self.alert_thresholds = PERFORMANCE_THRESHOLDS
    
    def monitor_endpoint_performance(
        self,
        endpoint: str,
        method: str = "GET",
        response_time_ms: int = None,
        status_code: int = None,
        user_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetric:
        """Monitor endpoint performance."""
        try:
            # Log performance metric
            metric = audit_service.log_performance_metric(
                metric_type="response_time",
                value=response_time_ms or 0,
                unit="ms",
                threshold=self.alert_thresholds.get("response_time", {}).get("critical_ms", 1000),
                endpoint=endpoint,
                user_id=user_id,
                audit_metadata={
                    "method": method,
                    "status_code": status_code,
                    **(metadata or {})
                }
            )
            
            # Check for performance alerts
            if response_time_ms:
                self._check_response_time_alert(endpoint, response_time_ms)
            
            # Track performance history
            self._track_performance_history(endpoint, "response_time", response_time_ms)
            
            return metric
            
        except Exception as e:
            logger.error(f"Error monitoring endpoint performance: {str(e)}")
            raise
    
    def monitor_database_performance(
        self,
        query_type: str,
        execution_time_ms: int,
        query_text: str = None,
        affected_rows: int = None,
        user_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetric:
        """Monitor database query performance."""
        try:
            # Log performance metric
            metric = audit_service.log_performance_metric(
                metric_type="database_query",
                value=execution_time_ms,
                unit="ms",
                threshold=self.alert_thresholds.get("database_queries", {}).get("critical_ms", 500),
                user_id=user_id,
                audit_metadata={
                    "query_type": query_type,
                    "query_text": query_text[:500] if query_text else None,  # Truncate long queries
                    "affected_rows": affected_rows,
                    **(metadata or {})
                }
            )
            
            # Check for database performance alerts
            self._check_database_performance_alert(query_type, execution_time_ms, query_text)
            
            # Track performance history
            self._track_performance_history("database", "query_time", execution_time_ms)
            
            return metric
            
        except Exception as e:
            logger.error(f"Error monitoring database performance: {str(e)}")
            raise
    
    def monitor_system_resources(
        self,
        user_id: Optional[int] = None
    ) -> Dict[str, PerformanceMetric]:
        """Monitor system resource usage."""
        try:
            metrics = {}
            
            if not PSUTIL_AVAILABLE:
                logger.warning("psutil not available. System resource monitoring disabled.")
                return metrics
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics["cpu_usage"] = audit_service.log_performance_metric(
                metric_type="cpu_usage",
                value=cpu_percent,
                unit="%",
                threshold=self.alert_thresholds.get("cpu_usage", {}).get("critical_percent", 70),
                user_id=user_id,
                audit_metadata={"timestamp": datetime.utcnow().isoformat()}
            )
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            metrics["memory_usage"] = audit_service.log_performance_metric(
                metric_type="memory_usage",
                value=memory_percent,
                unit="%",
                threshold=self.alert_thresholds.get("memory_usage", {}).get("critical_percent", 80),
                user_id=user_id,
                audit_metadata={
                    "total_memory_gb": round(memory.total / (1024**3), 2),
                    "available_memory_gb": round(memory.available / (1024**3), 2),
                    "used_memory_gb": round(memory.used / (1024**3), 2)
                }
            )
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics["disk_usage"] = audit_service.log_performance_metric(
                metric_type="disk_usage",
                value=disk_percent,
                unit="%",
                threshold=90,  # Alert if disk usage > 90%
                user_id=user_id,
                audit_metadata={
                    "total_disk_gb": round(disk.total / (1024**3), 2),
                    "used_disk_gb": round(disk.used / (1024**3), 2),
                    "free_disk_gb": round(disk.free / (1024**3), 2)
                }
            )
            
            # Check for system resource alerts
            self._check_system_resource_alerts(cpu_percent, memory_percent, disk_percent)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error monitoring system resources: {str(e)}")
            raise
    
    def monitor_file_operation(
        self,
        operation_type: str,
        file_path: str,
        file_size: int = None,
        processing_time_ms: int = None,
        user_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetric:
        """Monitor file operation performance."""
        try:
            # Log performance metric
            metric = audit_service.log_performance_metric(
                metric_type="file_operation",
                value=processing_time_ms or 0,
                unit="ms",
                threshold=self.alert_thresholds.get("file_operations", {}).get("critical_ms", 5000),
                user_id=user_id,
                audit_metadata={
                    "operation_type": operation_type,
                    "file_path": file_path,
                    "file_size": file_size,
                    **(metadata or {})
                }
            )
            
            # Check for file operation alerts
            if processing_time_ms:
                self._check_file_operation_alert(operation_type, processing_time_ms, file_size)
            
            return metric
            
        except Exception as e:
            logger.error(f"Error monitoring file operation: {str(e)}")
            raise
    
    def monitor_api_rate_limits(
        self,
        endpoint: str,
        current_usage: int,
        limit: int,
        window_seconds: int,
        user_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PerformanceMetric:
        """Monitor API rate limit usage."""
        try:
            usage_percent = (current_usage / limit) * 100
            
            # Log performance metric
            metric = audit_service.log_performance_metric(
                metric_type="rate_limit_usage",
                value=usage_percent,
                unit="%",
                threshold=90,  # Alert if usage > 90%
                user_id=user_id,
                audit_metadata={
                    "endpoint": endpoint,
                    "current_usage": current_usage,
                    "limit": limit,
                    "window_seconds": window_seconds,
                    **(metadata or {})
                }
            )
            
            # Check for rate limit alerts
            if usage_percent > 90:
                alert_service.send_performance_alert(
                    "rate_limit_usage",
                    usage_percent,
                    "%",
                    endpoint
                )
            
            return metric
            
        except Exception as e:
            logger.error(f"Error monitoring API rate limits: {str(e)}")
            raise
    
    def get_performance_summary(
        self,
        metric_type: Optional[str] = None,
        endpoint: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get performance summary for the specified period."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Query performance metrics
            query = PerformanceMetric.query.filter(
                PerformanceMetric.created_at >= start_date
            )
            
            if metric_type:
                query = query.filter(PerformanceMetric.metric_type == metric_type)
            
            if endpoint:
                query = query.filter(PerformanceMetric.endpoint == endpoint)
            
            metrics = query.order_by(PerformanceMetric.created_at.desc()).limit(1000).all()
            
            # Analyze performance data
            summary = {
                "metric_type": metric_type,
                "endpoint": endpoint,
                "period_days": days,
                "total_metrics": len(metrics),
                "metrics_by_type": {},
                "metrics_by_endpoint": {},
                "performance_statistics": {},
                "threshold_violations": 0,
                "performance_timeline": [],
                "top_slow_endpoints": {},
                "performance_trends": {}
            }
            
            metric_values = {}
            threshold_violations = 0
            
            for metric in metrics:
                # Count by type
                metric_type = metric.metric_type
                summary["metrics_by_type"][metric_type] = summary["metrics_by_type"].get(metric_type, 0) + 1
                
                # Count by endpoint
                endpoint = metric.endpoint
                if endpoint:
                    summary["metrics_by_endpoint"][endpoint] = summary["metrics_by_endpoint"].get(endpoint, 0) + 1
                
                # Track threshold violations
                if metric.exceeded_threshold:
                    threshold_violations += 1
                
                # Collect values for statistics
                if metric_type not in metric_values:
                    metric_values[metric_type] = []
                metric_values[metric_type].append(metric.value)
                
                # Track performance timeline
                summary["performance_timeline"].append({
                    "timestamp": metric.created_at.isoformat(),
                    "metric_type": metric_type,
                    "value": metric.value,
                    "unit": metric.unit,
                    "endpoint": endpoint,
                    "exceeded_threshold": metric.exceeded_threshold
                })
                
                # Track slow endpoints
                if metric_type == "response_time" and endpoint:
                    if endpoint not in summary["top_slow_endpoints"]:
                        summary["top_slow_endpoints"][endpoint] = []
                    summary["top_slow_endpoints"][endpoint].append(metric.value)
            
            # Calculate performance statistics
            for metric_type, values in metric_values.items():
                if values:
                    summary["performance_statistics"][metric_type] = {
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "count": len(values)
                    }
            
            # Calculate top slow endpoints
            for endpoint, values in summary["top_slow_endpoints"].items():
                if values:
                    summary["top_slow_endpoints"][endpoint] = {
                        "avg_response_time": sum(values) / len(values),
                        "max_response_time": max(values),
                        "request_count": len(values)
                    }
            
            # Sort top slow endpoints by average response time
            summary["top_slow_endpoints"] = dict(sorted(
                summary["top_slow_endpoints"].items(),
                key=lambda x: x[1]["avg_response_time"],
                reverse=True
            )[:10])
            
            summary["threshold_violations"] = threshold_violations
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {str(e)}")
            return {"error": str(e)}
    
    def get_system_health_status(self) -> Dict[str, Any]:
        """Get current system health status."""
        try:
            # Get current system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Determine health status
            health_status = "healthy"
            issues = []
            
            # Check CPU
            if cpu_percent > 80:
                health_status = "critical"
                issues.append(f"High CPU usage: {cpu_percent}%")
            elif cpu_percent > 60:
                health_status = "warning" if health_status == "healthy" else health_status
                issues.append(f"Elevated CPU usage: {cpu_percent}%")
            
            # Check Memory
            if memory.percent > 90:
                health_status = "critical"
                issues.append(f"High memory usage: {memory.percent}%")
            elif memory.percent > 80:
                health_status = "warning" if health_status == "healthy" else health_status
                issues.append(f"Elevated memory usage: {memory.percent}%")
            
            # Check Disk
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > 95:
                health_status = "critical"
                issues.append(f"High disk usage: {disk_percent:.1f}%")
            elif disk_percent > 85:
                health_status = "warning" if health_status == "healthy" else health_status
                issues.append(f"Elevated disk usage: {disk_percent:.1f}%")
            
            return {
                "status": health_status,
                "timestamp": datetime.utcnow().isoformat(),
                "issues": issues,
                "metrics": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "disk_percent": disk_percent,
                    "disk_free_gb": round(disk.free / (1024**3), 2)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system health status: {str(e)}")
            return {
                "status": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
    
    def performance_decorator(self, metric_type: str = "response_time", threshold: float = None):
        """Decorator for monitoring function performance."""
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                    
                    # Log performance metric
                    self.monitor_endpoint_performance(
                        endpoint=func.__name__,
                        method="FUNCTION",
                        response_time_ms=int(execution_time),
                        audit_metadata={
                            "function_name": func.__name__,
                            "module": func.__module__
                        }
                    )
                    
                    return result
                    
                except Exception as e:
                    execution_time = (time.time() - start_time) * 1000
                    
                    # Log performance metric even for errors
                    self.monitor_endpoint_performance(
                        endpoint=func.__name__,
                        method="FUNCTION_ERROR",
                        response_time_ms=int(execution_time),
                        status_code=500,
                        audit_metadata={
                            "function_name": func.__name__,
                            "module": func.__module__,
                            "error": str(e)
                        }
                    )
                    
                    raise
            
            return wrapper
        return decorator
    
    def _check_response_time_alert(self, endpoint: str, response_time_ms: int):
        """Check for response time alerts."""
        try:
            thresholds = self.alert_thresholds.get("response_time", {})
            
            if response_time_ms >= thresholds.get("alert_ms", 2000):
                alert_service.send_performance_alert(
                    "response_time",
                    response_time_ms,
                    "ms",
                    endpoint
                )
        except Exception as e:
            logger.error(f"Error checking response time alert: {str(e)}")
    
    def _check_database_performance_alert(self, query_type: str, execution_time_ms: int, query_text: str = None):
        """Check for database performance alerts."""
        try:
            thresholds = self.alert_thresholds.get("database_queries", {})
            
            if execution_time_ms >= thresholds.get("alert_ms", 1000):
                alert_service.send_performance_alert(
                    "database_query",
                    execution_time_ms,
                    "ms",
                    f"Database query: {query_type}"
                )
        except Exception as e:
            logger.error(f"Error checking database performance alert: {str(e)}")
    
    def _check_system_resource_alerts(self, cpu_percent: float, memory_percent: float, disk_percent: float):
        """Check for system resource alerts."""
        try:
            # Check CPU
            if cpu_percent >= self.alert_thresholds.get("cpu_usage", {}).get("alert_percent", 80):
                alert_service.send_performance_alert(
                    "cpu_usage",
                    cpu_percent,
                    "%"
                )
            
            # Check Memory
            if memory_percent >= self.alert_thresholds.get("memory_usage", {}).get("alert_percent", 90):
                alert_service.send_performance_alert(
                    "memory_usage",
                    memory_percent,
                    "%"
                )
            
            # Check Disk
            if disk_percent >= 95:
                alert_service.send_performance_alert(
                    "disk_usage",
                    disk_percent,
                    "%"
                )
        except Exception as e:
            logger.error(f"Error checking system resource alerts: {str(e)}")
    
    def _check_file_operation_alert(self, operation_type: str, processing_time_ms: int, file_size: int = None):
        """Check for file operation alerts."""
        try:
            thresholds = self.alert_thresholds.get("file_operations", {})
            
            if processing_time_ms >= thresholds.get("alert_ms", 10000):
                alert_service.send_performance_alert(
                    "file_operation",
                    processing_time_ms,
                    "ms",
                    f"File operation: {operation_type}"
                )
        except Exception as e:
            logger.error(f"Error checking file operation alert: {str(e)}")
    
    def _track_performance_history(self, endpoint: str, metric_type: str, value: float):
        """Track performance history for trend analysis."""
        try:
            key = f"{endpoint}_{metric_type}"
            if key not in self.performance_history:
                self.performance_history[key] = []
            
            self.performance_history[key].append({
                "timestamp": datetime.utcnow(),
                "value": value
            })
            
            # Keep only last 1000 entries
            if len(self.performance_history[key]) > 1000:
                self.performance_history[key] = self.performance_history[key][-1000:]
            
        except Exception as e:
            logger.error(f"Error tracking performance history: {str(e)}")

# Global performance service instance
performance_service = PerformanceService()
