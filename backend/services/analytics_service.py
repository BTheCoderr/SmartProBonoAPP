from typing import Dict, Any, Optional
import logging
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)
from datetime import datetime, timedelta
from services.performance_monitor import performance_monitor

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for handling both Google Analytics and custom performance metrics."""
    
    def __init__(self, property_id: str):
        """Initialize analytics service.
        
        Args:
            property_id: Google Analytics 4 property ID
        """
        self.property_id = property_id
        self._client = None
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize Google Analytics client."""
        try:
            self._client = BetaAnalyticsDataClient()
        except Exception as e:
            logger.error(f"Failed to initialize Google Analytics client: {e}")
            self._client = None
    
    async def track_event(self, 
                         event_name: str, 
                         event_params: Dict[str, Any],
                         user_id: Optional[str] = None) -> None:
        """Track an event in both GA4 and custom monitoring.
        
        Args:
            event_name: Name of the event
            event_params: Event parameters
            user_id: Optional user ID for user-specific tracking
        """
        try:
            # Track in custom performance monitor
            performance_monitor.track_custom_event(event_name, event_params)
            
            # Track in Google Analytics (if available)
            if self._client:
                # Implementation depends on your GA4 configuration
                pass
                
        except Exception as e:
            logger.error(f"Failed to track event {event_name}: {e}")
    
    async def get_user_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Get user-related metrics from both GA and custom monitoring.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Combined metrics from both systems
        """
        try:
            # Get custom metrics
            custom_metrics = {
                'concurrent_users': performance_monitor.get_peak_concurrent_users(),
                'average_response_time': performance_monitor.get_average_response_time('/api/*'),
                'error_rate': performance_monitor.generate_report()['error_rate']
            }
            
            # Get GA4 metrics if available
            if self._client:
                request = RunReportRequest(
                    property=f"properties/{self.property_id}",
                    date_ranges=[DateRange(
                        start_date=f"{days}daysAgo",
                        end_date="today"
                    )],
                    metrics=[
                        Metric(name="activeUsers"),
                        Metric(name="newUsers"),
                        Metric(name="userEngagementDuration")
                    ],
                    dimensions=[Dimension(name="date")]
                )
                
                response = self._client.run_report(request)
                
                ga_metrics = {
                    'active_users': sum(row.metric_values[0].value for row in response.rows),
                    'new_users': sum(row.metric_values[1].value for row in response.rows),
                    'avg_engagement_time': sum(float(row.metric_values[2].value) for row in response.rows) / len(response.rows)
                }
                
                return {**custom_metrics, **ga_metrics}
            
            return custom_metrics
            
        except Exception as e:
            logger.error(f"Failed to get user metrics: {e}")
            return {}
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get combined performance metrics."""
        try:
            # Get detailed performance metrics from our custom monitor
            custom_metrics = performance_monitor.generate_report()
            
            # Get GA4 performance metrics if available
            if self._client:
                request = RunReportRequest(
                    property=f"properties/{self.property_id}",
                    date_ranges=[DateRange(
                        start_date="7daysAgo",
                        end_date="today"
                    )],
                    metrics=[
                        Metric(name="averagePageLoadTime"),
                        Metric(name="bounceRate"),
                        Metric(name="pageViews")
                    ]
                )
                
                response = self._client.run_report(request)
                
                ga_metrics = {
                    'avg_page_load': float(response.rows[0].metric_values[0].value),
                    'bounce_rate': float(response.rows[0].metric_values[1].value),
                    'page_views': int(response.rows[0].metric_values[2].value)
                }
                
                return {**custom_metrics, **ga_metrics}
            
            return custom_metrics
            
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}
    
    async def get_error_analytics(self) -> Dict[str, Any]:
        """Get error analytics from both systems."""
        try:
            # Get error metrics from custom monitor
            custom_errors = {
                'api_errors': performance_monitor.get_error_count('*', '/api/*'),
                'slow_queries': performance_monitor.get_slow_queries()
            }
            
            # Get GA4 error metrics if available
            if self._client:
                request = RunReportRequest(
                    property=f"properties/{self.property_id}",
                    date_ranges=[DateRange(
                        start_date="7daysAgo",
                        end_date="today"
                    )],
                    metrics=[
                        Metric(name="exceptions"),
                        Metric(name="fatalExceptions")
                    ]
                )
                
                response = self._client.run_report(request)
                
                ga_errors = {
                    'js_exceptions': int(response.rows[0].metric_values[0].value),
                    'fatal_exceptions': int(response.rows[0].metric_values[1].value)
                }
                
                return {**custom_errors, **ga_errors}
            
            return custom_errors
            
        except Exception as e:
            logger.error(f"Failed to get error analytics: {e}")
            return {}

# Create singleton instance
analytics_service = AnalyticsService("YOUR_GA4_PROPERTY_ID") 