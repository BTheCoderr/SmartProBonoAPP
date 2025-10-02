"""
Advanced Analytics Service
Provides comprehensive business intelligence and reporting capabilities
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import pandas as pd
import numpy as np
from sqlalchemy import func, and_, or_, desc, asc

# Import models
try:
    from models.audit import PerformanceMetric, UserActivity
except ImportError:
    try:
        from models.audit import PerformanceMetric, UserActivity
    except ImportError:
        # Define a fallback for type hints
        PerformanceMetric = Any
        UserActivity = Any

logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of analytics metrics"""
    USER_ACTIVITY = "user_activity"
    SYSTEM_PERFORMANCE = "system_performance"
    BUSINESS_METRICS = "business_metrics"
    SECURITY_METRICS = "security_metrics"
    LEGAL_METRICS = "legal_metrics"

class TimeRange(Enum):
    """Time range options for analytics"""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"

@dataclass
class AnalyticsMetric:
    """Represents an analytics metric"""
    metric_id: str
    metric_type: MetricType
    name: str
    value: float
    timestamp: datetime
    dimensions: Dict[str, Any]
    metadata: Dict[str, Any]

@dataclass
class AnalyticsReport:
    """Represents an analytics report"""
    report_id: str
    report_type: str
    title: str
    description: str
    data: Dict[str, Any]
    generated_at: datetime
    time_range: TimeRange
    filters: Dict[str, Any]

class AdvancedAnalyticsService:
    """Service for advanced analytics and business intelligence"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.metrics_cache = {}
        self.reports_cache = {}
        
    def track_user_activity(self, user_id: int, activity_type: str, details: Dict[str, Any] = None):
        """Track user activity for analytics"""
        try:
            # Create user activity record
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                details=details or {},
                created_at=datetime.now()
            )
            
            self.db.add(activity)
            self.db.commit()
            
            # Update real-time metrics
            self._update_user_activity_metrics(user_id, activity_type)
            
            logger.info(f"Tracked user activity: {activity_type} for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error tracking user activity: {e}")
            self.db.rollback()
    
    def track_system_performance(self, metric_name: str, value: float, dimensions: Dict[str, Any] = None):
        """Track system performance metrics"""
        try:
            # Create a performance metric
            metric = PerformanceMetric(
                metric_type=metric_name,
                value=value,
                threshold=self._get_metric_threshold(metric_name),
                description=f"System performance metric: {metric_name}",
                timestamp=datetime.now(),
                metadata=dimensions or {}
            )
            
            self.db.add(metric)
            self.db.commit()
            
            # Check for alerts
            self._check_performance_thresholds(metric)
            
            logger.debug(f"Tracked performance metric: {metric_name} = {value}")
            
        except Exception as e:
            logger.error(f"Error tracking system performance: {e}")
            self.db.rollback()
    
    def track_business_metric(self, metric_name: str, value: float, dimensions: Dict[str, Any] = None):
        """Track business metrics"""
        try:
            # Store in a business metrics table (would need to be created)
            # For now, store in performance metrics with special prefix
            self.track_system_performance(f"business_{metric_name}", value, dimensions)
            
        except Exception as e:
            logger.error(f"Error tracking business metric: {e}")
    
    def get_user_analytics(self, time_range: TimeRange = TimeRange.DAY, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        try:
            end_date = datetime.now()
            start_date = self._get_start_date(end_date, time_range)
            
            # Base query
            query = self.db.query(UserActivity)
            
            if user_id:
                query = query.filter(UserActivity.user_id == user_id)
            
            query = query.filter(
                and_(
                    UserActivity.created_at >= start_date,
                    UserActivity.created_at <= end_date
                )
            )
            
            activities = query.all()
            
            # Calculate metrics
            total_activities = len(activities)
            unique_users = len(set(a.user_id for a in activities))
            
            # Activity type breakdown
            activity_types = {}
            for activity in activities:
                activity_type = activity.activity_type
                activity_types[activity_type] = activity_types.get(activity_type, 0) + 1
            
            # Hourly distribution
            hourly_distribution = {}
            for activity in activities:
                hour = activity.created_at.hour
                hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
            
            # Most active users
            user_activity_counts = {}
            for activity in activities:
                user_id = activity.user_id
                user_activity_counts[user_id] = user_activity_counts.get(user_id, 0) + 1
            
            most_active_users = sorted(
                user_activity_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
            
            return {
                "time_range": time_range.value,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_activities": total_activities,
                "unique_users": unique_users,
                "activity_types": activity_types,
                "hourly_distribution": hourly_distribution,
                "most_active_users": most_active_users,
                "average_activities_per_user": total_activities / unique_users if unique_users > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting user analytics: {e}")
            return {}
    
    def get_system_performance_analytics(self, time_range: TimeRange = TimeRange.DAY) -> Dict[str, Any]:
        """Get system performance analytics"""
        try:
            end_date = datetime.now()
            start_date = self._get_start_date(end_date, time_range)
            
            # Get performance metrics
            query = self.db.query(PerformanceMetric).filter(
                and_(
                    PerformanceMetric.timestamp >= start_date,
                    PerformanceMetric.timestamp <= end_date
                )
            )
            
            metrics = query.all()
            
            # Group by metric type
            metrics_by_type = {}
            for metric in metrics:
                metric_type = metric.metric_type
                if metric_type not in metrics_by_type:
                    metrics_by_type[metric_type] = []
                metrics_by_type[metric_type].append(metric.value)
            
            # Calculate statistics for each metric type
            performance_stats = {}
            for metric_type, values in metrics_by_type.items():
                if values:
                    performance_stats[metric_type] = {
                        "count": len(values),
                        "average": np.mean(values),
                        "median": np.median(values),
                        "min": np.min(values),
                        "max": np.max(values),
                        "std": np.std(values),
                        "p95": np.percentile(values, 95),
                        "p99": np.percentile(values, 99)
                    }
            
            # Identify performance issues
            performance_issues = []
            for metric_type, stats in performance_stats.items():
                threshold = self._get_metric_threshold(metric_type)
                if stats["average"] > threshold:
                    performance_issues.append({
                        "metric_type": metric_type,
                        "current_average": stats["average"],
                        "threshold": threshold,
                        "severity": "high" if stats["average"] > threshold * 1.5 else "medium"
                    })
            
            return {
                "time_range": time_range.value,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_metrics": len(metrics),
                "metrics_by_type": performance_stats,
                "performance_issues": performance_issues,
                "overall_health_score": self._calculate_health_score(performance_stats)
            }
            
        except Exception as e:
            logger.error(f"Error getting system performance analytics: {e}")
            return {}
    
    def get_business_analytics(self, time_range: TimeRange = TimeRange.DAY) -> Dict[str, Any]:
        """Get business analytics and KPIs"""
        try:
            end_date = datetime.now()
            start_date = self._get_start_date(end_date, time_range)
            
            # Get user registrations
            from models.user import User
            new_users = self.db.query(User).filter(
                and_(
                    User.created_at >= start_date,
                    User.created_at <= end_date
                )
            ).count()
            
            # Get total users
            total_users = self.db.query(User).count()
            
            # Get case analytics (if cases table exists)
            case_metrics = self._get_case_metrics(start_date, end_date)
            
            # Get document analytics
            document_metrics = self._get_document_metrics(start_date, end_date)
            
            # Get AI usage analytics
            ai_metrics = self._get_ai_usage_metrics(start_date, end_date)
            
            # Calculate growth rates
            previous_start = start_date - (end_date - start_date)
            previous_new_users = self.db.query(User).filter(
                and_(
                    User.created_at >= previous_start,
                    User.created_at < start_date
                )
            ).count()
            
            user_growth_rate = ((new_users - previous_new_users) / previous_new_users * 100) if previous_new_users > 0 else 0
            
            return {
                "time_range": time_range.value,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "new_users": new_users,
                "total_users": total_users,
                "user_growth_rate": user_growth_rate,
                "case_metrics": case_metrics,
                "document_metrics": document_metrics,
                "ai_metrics": ai_metrics,
                "revenue_metrics": self._get_revenue_metrics(start_date, end_date),
                "conversion_metrics": self._get_conversion_metrics(start_date, end_date)
            }
            
        except Exception as e:
            logger.error(f"Error getting business analytics: {e}")
            return {}
    
    def get_security_analytics(self, time_range: TimeRange = TimeRange.DAY) -> Dict[str, Any]:
        """Get security analytics"""
        try:
            end_date = datetime.now()
            start_date = self._get_start_date(end_date, time_range)
            
            # Get security events
            from models.audit import SecurityEvent
            security_events = self.db.query(SecurityEvent).filter(
                and_(
                    SecurityEvent.timestamp >= start_date,
                    SecurityEvent.timestamp <= end_date
                )
            ).all()
            
            # Group by severity
            events_by_severity = {}
            for event in security_events:
                severity = event.severity
                events_by_severity[severity] = events_by_severity.get(severity, 0) + 1
            
            # Group by event type
            events_by_type = {}
            for event in security_events:
                event_type = event.event_type
                events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
            
            # Get top IP addresses
            ip_addresses = {}
            for event in security_events:
                if event.ip_address:
                    ip_addresses[event.ip_address] = ip_addresses.get(event.ip_address, 0) + 1
            
            top_ips = sorted(ip_addresses.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Calculate security score
            security_score = self._calculate_security_score(events_by_severity)
            
            return {
                "time_range": time_range.value,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_events": len(security_events),
                "events_by_severity": events_by_severity,
                "events_by_type": events_by_type,
                "top_ip_addresses": top_ips,
                "security_score": security_score,
                "critical_events": events_by_severity.get("critical", 0),
                "high_events": events_by_severity.get("high", 0),
                "medium_events": events_by_severity.get("medium", 0),
                "low_events": events_by_severity.get("low", 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting security analytics: {e}")
            return {}
    
    def generate_comprehensive_report(self, time_range: TimeRange = TimeRange.DAY) -> AnalyticsReport:
        """Generate a comprehensive analytics report"""
        try:
            report_id = f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Gather all analytics
            user_analytics = self.get_user_analytics(time_range)
            performance_analytics = self.get_system_performance_analytics(time_range)
            business_analytics = self.get_business_analytics(time_range)
            security_analytics = self.get_security_analytics(time_range)
            
            # Create comprehensive report
            report_data = {
                "user_analytics": user_analytics,
                "performance_analytics": performance_analytics,
                "business_analytics": business_analytics,
                "security_analytics": security_analytics,
                "summary": self._generate_report_summary(
                    user_analytics, 
                    performance_analytics, 
                    business_analytics, 
                    security_analytics
                )
            }
            
            report = AnalyticsReport(
                report_id=report_id,
                report_type="comprehensive",
                title=f"SmartProBono Analytics Report - {time_range.value.title()}",
                description=f"Comprehensive analytics report for {time_range.value} period",
                data=report_data,
                generated_at=datetime.now(),
                time_range=time_range,
                filters={}
            )
            
            # Cache the report
            self.reports_cache[report_id] = report
            
            logger.info(f"Generated comprehensive analytics report: {report_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return None
    
    def _get_start_date(self, end_date: datetime, time_range: TimeRange) -> datetime:
        """Calculate start date based on time range"""
        if time_range == TimeRange.HOUR:
            return end_date - timedelta(hours=1)
        elif time_range == TimeRange.DAY:
            return end_date - timedelta(days=1)
        elif time_range == TimeRange.WEEK:
            return end_date - timedelta(weeks=1)
        elif time_range == TimeRange.MONTH:
            return end_date - timedelta(days=30)
        elif time_range == TimeRange.QUARTER:
            return end_date - timedelta(days=90)
        elif time_range == TimeRange.YEAR:
            return end_date - timedelta(days=365)
        else:
            return end_date - timedelta(days=1)
    
    def _get_metric_threshold(self, metric_name: str) -> float:
        """Get threshold for a performance metric"""
        thresholds = {
            "response_time": 1000,  # 1 second
            "cpu_usage": 80,  # 80%
            "memory_usage": 85,  # 85%
            "disk_usage": 90,  # 90%
            "error_rate": 5,  # 5%
            "concurrent_users": 1000,  # 1000 users
            "api_calls_per_minute": 10000,  # 10k calls
            "database_connections": 100,  # 100 connections
        }
        return thresholds.get(metric_name, 100)
    
    def _check_performance_thresholds(self, metric: PerformanceMetric):
        """Check if performance metric exceeds thresholds"""
        if metric.value > metric.threshold:
            # This would trigger the performance alert system
            logger.warning(f"Performance threshold exceeded: {metric.metric_type} = {metric.value} > {metric.threshold}")
    
    def _update_user_activity_metrics(self, user_id: int, activity_type: str):
        """Update real-time user activity metrics"""
        # This would update real-time metrics cache
        pass
    
    def _get_case_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get case-related metrics"""
        # This would query case data if available
        return {
            "total_cases": 0,
            "new_cases": 0,
            "closed_cases": 0,
            "active_cases": 0
        }
    
    def _get_document_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get document-related metrics"""
        # This would query document data if available
        return {
            "total_documents": 0,
            "documents_uploaded": 0,
            "documents_generated": 0,
            "documents_processed": 0
        }
    
    def _get_ai_usage_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get AI usage metrics"""
        # This would query AI usage data if available
        return {
            "ai_queries": 0,
            "ai_responses": 0,
            "ai_success_rate": 0,
            "ai_response_time": 0
        }
    
    def _get_revenue_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get revenue metrics"""
        # This would query payment/revenue data if available
        return {
            "total_revenue": 0,
            "revenue_growth": 0,
            "average_revenue_per_user": 0,
            "subscription_metrics": {}
        }
    
    def _get_conversion_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get conversion metrics"""
        # This would calculate conversion rates
        return {
            "visitor_to_user_conversion": 0,
            "user_to_customer_conversion": 0,
            "trial_to_paid_conversion": 0,
            "funnel_metrics": {}
        }
    
    def _calculate_health_score(self, performance_stats: Dict[str, Any]) -> float:
        """Calculate overall system health score"""
        if not performance_stats:
            return 100.0
        
        total_score = 0
        count = 0
        
        for metric_type, stats in performance_stats.items():
            threshold = self._get_metric_threshold(metric_type)
            current_value = stats["average"]
            
            # Calculate score (100 = perfect, 0 = terrible)
            if current_value <= threshold:
                score = 100
            elif current_value <= threshold * 1.5:
                score = 80
            elif current_value <= threshold * 2:
                score = 60
            else:
                score = 40
            
            total_score += score
            count += 1
        
        return total_score / count if count > 0 else 100.0
    
    def _calculate_security_score(self, events_by_severity: Dict[str, int]) -> float:
        """Calculate security score based on events"""
        if not events_by_severity:
            return 100.0
        
        # Weight events by severity
        weights = {
            "critical": -20,
            "high": -10,
            "medium": -5,
            "low": -1
        }
        
        score = 100
        for severity, count in events_by_severity.items():
            weight = weights.get(severity, 0)
            score += weight * count
        
        return max(0, min(100, score))
    
    def _generate_report_summary(self, user_analytics: Dict, performance_analytics: Dict, 
                                business_analytics: Dict, security_analytics: Dict) -> Dict[str, Any]:
        """Generate executive summary of analytics"""
        return {
            "key_insights": [
                f"Total users: {business_analytics.get('total_users', 0)}",
                f"New users this period: {business_analytics.get('new_users', 0)}",
                f"System health score: {performance_analytics.get('overall_health_score', 0):.1f}%",
                f"Security score: {security_analytics.get('security_score', 0):.1f}%",
                f"Total activities: {user_analytics.get('total_activities', 0)}"
            ],
            "recommendations": [
                "Monitor system performance closely",
                "Focus on user engagement improvements",
                "Maintain security vigilance",
                "Consider scaling infrastructure"
            ],
            "alerts": [
                "Performance issues detected" if performance_analytics.get('performance_issues') else None,
                "Security events require attention" if security_analytics.get('critical_events', 0) > 0 else None
            ]
        }

# Global analytics service instance
def create_analytics_service(db_session):
    """Create analytics service instance"""
    return AdvancedAnalyticsService(db_session)
