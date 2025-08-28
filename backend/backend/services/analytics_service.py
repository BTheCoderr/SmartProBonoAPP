from typing import Dict, Any, Optional, List
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
from services.database import Database
from services.cache import Cache
from models.analytics import (
    FormView,
    FormStart,
    FormCompletion,
    FormAbandonment,
    FieldInteraction,
    FieldTiming,
    FormError
)
import os
import json
import asyncio

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for handling form analytics, Google Analytics, and custom performance metrics."""
    
    def __init__(self, property_id: str):
        """Initialize analytics service.
        
        Args:
            property_id: Google Analytics 4 property ID
        """
        self.property_id = property_id
        self._client = None
        self.db = Database()
        self.cache = Cache()
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
                         user_id: Optional[str] = None) -> bool:
        """Track an event in both GA4 and custom monitoring.
        
        Args:
            event_name: Name of the event
            event_params: Event parameters
            user_id: Optional user ID for user-specific tracking
            
        Returns:
            True if the event was successfully tracked, False otherwise
        """
        try:
            # Track in custom performance monitor
            performance_monitor.track_custom_event(event_name, event_params)
            
            # Track in Google Analytics (if available)
            if self._client:
                # Implementation depends on your GA4 configuration
                pass
                
            return True
        except Exception as e:
            logger.error(f"Failed to track event {event_name}: {e}")
            return False
    
    async def track_form_view(self, form_view: FormView) -> None:
        """Track a form view event.
        
        Args:
            form_view: Form view event data
        """
        try:
            # Store in database
            await self.db.form_views.insert_one(form_view.dict())
            
            # Update cache for real-time analytics
            cache_key = f"form_views:{form_view.form_type}:{datetime.now().date()}"
            await self.cache.incr(cache_key)
            
            # Track in GA4
            await self.track_event("form_view", form_view.dict())
            
        except Exception as e:
            logger.error(f"Failed to track form view: {e}")
    
    async def track_form_start(self, form_start: FormStart) -> None:
        """Track a form start event.
        
        Args:
            form_start: Form start event data
        """
        try:
            await self.db.form_starts.insert_one(form_start.dict())
            await self.track_event("form_start", form_start.dict())
            
            # Update active sessions
            session_key = f"active_sessions:{form_start.form_type}"
            await self.cache.sadd(session_key, form_start.session_id)
            await self.cache.expire(session_key, 3600)  # 1 hour TTL
            
        except Exception as e:
            logger.error(f"Failed to track form start: {e}")
    
    async def track_form_completion(self, form_completion: FormCompletion) -> None:
        """Track a form completion event.
        
        Args:
            form_completion: Form completion event data
        """
        try:
            await self.db.form_completions.insert_one(form_completion.dict())
            await self.track_event("form_completion", form_completion.dict())
            
            # Update completion metrics
            await self._update_completion_metrics(form_completion)
            
            # Remove from active sessions
            session_key = f"active_sessions:{form_completion.form_type}"
            await self.cache.srem(session_key, form_completion.session_id)
            
        except Exception as e:
            logger.error(f"Failed to track form completion: {e}")
    
    async def track_form_abandonment(self, abandonment: FormAbandonment) -> None:
        """Track a form abandonment event.
        
        Args:
            abandonment: Form abandonment event data
        """
        try:
            await self.db.form_abandonments.insert_one(abandonment.dict())
            await self.track_event("form_abandonment", abandonment.dict())
            
            # Update abandonment metrics
            await self._update_abandonment_metrics(abandonment)
            
            # Remove from active sessions
            session_key = f"active_sessions:{abandonment.form_type}"
            await self.cache.srem(session_key, abandonment.session_id)
            
        except Exception as e:
            logger.error(f"Failed to track form abandonment: {e}")
    
    async def track_field_interaction(self, interaction: FieldInteraction) -> None:
        """Track a field interaction event.
        
        Args:
            interaction: Field interaction event data
        """
        try:
            await self.db.field_interactions.insert_one(interaction.dict())
            
            # Update field metrics
            metrics_key = f"field_metrics:{interaction.form_type}:{interaction.field_name}"
            field_metrics = {
                'total_interactions': await self.cache.incr(f"{metrics_key}:interactions"),
                'validation_errors': await self.cache.incr(f"{metrics_key}:errors") if not interaction.is_valid else 0
            }
            
            await self.cache.hmset(metrics_key, field_metrics)
            
        except Exception as e:
            logger.error(f"Failed to track field interaction: {e}")
    
    async def track_field_timing(self, timing: FieldTiming) -> None:
        """Track field timing data.
        
        Args:
            timing: Field timing event data
        """
        try:
            await self.db.field_timings.insert_one(timing.dict())
            
            # Update average time spent on field
            key = f"field_timing:{timing.form_type}:{timing.field_name}"
            await self._update_average_timing(key, timing.duration)
            
        except Exception as e:
            logger.error(f"Failed to track field timing: {e}")
    
    async def track_form_error(self, error: FormError) -> None:
        """Track a form error event.
        
        Args:
            error: Form error event data
        """
        try:
            await self.db.form_errors.insert_one(error.dict())
            await self.track_event("form_error", error.dict())
            
            # Update error metrics
            error_key = f"form_errors:{error.form_type}:{error.error_type}"
            await self.cache.incr(error_key)
            
        except Exception as e:
            logger.error(f"Failed to track form error: {e}")
    
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
    
    async def get_form_analytics(self, form_type: str, date_range: str = '7d') -> Dict[str, Any]:
        """Get comprehensive analytics for a specific form type.
        
        Args:
            form_type: Type of form
            date_range: Date range for analytics (e.g., '7d', '30d')
            
        Returns:
            Dictionary containing form analytics
        """
        try:
            days = int(date_range[:-1])
            start_date = datetime.now() - timedelta(days=days)
            
            pipeline = [
                {
                    '$match': {
                        'form_type': form_type,
                        'timestamp': {'$gte': start_date}
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'total_views': {'$sum': 1},
                        'total_starts': {'$sum': {'$cond': ['$session_id', 1, 0]}},
                        'total_completions': {'$sum': {'$cond': ['$completed', 1, 0]}},
                        'total_abandonments': {'$sum': {'$cond': ['$abandoned', 1, 0]}},
                        'avg_completion_time': {'$avg': '$completion_time'},
                        'field_completion_rates': {'$push': '$field_completion_rates'}
                    }
                }
            ]
            
            results = await self.db.form_analytics.aggregate(pipeline)
            
            # Enhance with cached real-time data
            real_time_data = await self._get_real_time_metrics(form_type)
            
            return {**results, **real_time_data}
            
        except Exception as e:
            logger.error(f"Failed to get form analytics: {e}")
            return {}
    
    async def get_field_analytics(self, form_type: str, field_name: str) -> Dict[str, Any]:
        """Get analytics for a specific form field.
        
        Args:
            form_type: Type of form
            field_name: Name of the field
            
        Returns:
            Dictionary containing field analytics
        """
        try:
            # Get field metrics from cache
            metrics_key = f"field_metrics:{form_type}:{field_name}"
            cached_metrics = await self.cache.hgetall(metrics_key)
            
            # Get field timing data
            timing_key = f"field_timing:{form_type}:{field_name}"
            avg_time = await self.cache.get(timing_key)
            
            # Get historical data from database
            pipeline = [
                {
                    '$match': {
                        'form_type': form_type,
                        'field_name': field_name
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'validation_success_rate': {
                            '$avg': {'$cond': ['$is_valid', 1, 0]}
                        },
                        'avg_attempts': {'$avg': '$validation_attempts'},
                        'common_errors': {
                            '$push': '$validation_errors'
                        }
                    }
                }
            ]
            
            historical_data = await self.db.field_interactions.aggregate(pipeline)
            
            return {
                **cached_metrics,
                'average_time_spent': float(avg_time) if avg_time else 0,
                **historical_data
            }
            
        except Exception as e:
            logger.error(f"Failed to get field analytics: {e}")
            return {}
    
    async def get_abandonment_analysis(self, form_type: str) -> Dict[str, Any]:
        """Get detailed analysis of form abandonments.
        
        Args:
            form_type: Type of form
            
        Returns:
            Dictionary containing abandonment analysis
        """
        try:
            pipeline = [
                {
                    '$match': {
                        'form_type': form_type,
                        'abandoned': True
                    }
                },
                {
                    '$group': {
                        '_id': '$abandonment_reason.type',
                        'count': {'$sum': 1},
                        'avg_completion_percentage': {'$avg': '$completion_percentage'},
                        'common_last_fields': {'$push': '$last_interaction.field_name'},
                        'avg_time_spent': {'$avg': '$time_spent'}
                    }
                }
            ]
            
            results = await self.db.form_abandonments.aggregate(pipeline)
            
            # Enhance with real-time data
            active_sessions = await self.cache.scard(f"active_sessions:{form_type}")
            
            return {
                'abandonment_analysis': results,
                'active_sessions': active_sessions
            }
            
        except Exception as e:
            logger.error(f"Failed to get abandonment analysis: {e}")
            return {}
    
    async def get_form_success_rate(self, form_type: str, date_range: str = '30d') -> Dict[str, Any]:
        """Get form success rate metrics.
        
        Args:
            form_type: Type of form
            date_range: Date range for analysis
            
        Returns:
            Dictionary containing success rate metrics
        """
        try:
            days = int(date_range[:-1])
            start_date = datetime.now() - timedelta(days=days)
            
            pipeline = [
                {
                    '$match': {
                        'form_type': form_type,
                        'timestamp': {'$gte': start_date}
                    }
                },
                {
                    '$group': {
                        '_id': None,
                        'total_attempts': {'$sum': 1},
                        'successful_submissions': {
                            '$sum': {'$cond': ['$completed', 1, 0]}
                        },
                        'avg_attempts_before_success': {
                            '$avg': '$previous_attempts'
                        },
                        'completion_time_distribution': {
                            '$push': '$completion_time'
                        }
                    }
                }
            ]
            
            results = await self.db.form_completions.aggregate(pipeline)
            
            return {
                **results,
                'real_time_success_rate': await self._get_real_time_success_rate(form_type)
            }
            
        except Exception as e:
            logger.error(f"Failed to get form success rate: {e}")
            return {}
    
    # Helper methods
    async def _update_completion_metrics(self, completion: FormCompletion) -> None:
        """Update completion metrics in cache."""
        try:
            base_key = f"completion_metrics:{completion.form_type}"
            
            # Update completion count
            await self.cache.incr(f"{base_key}:total")
            
            # Update average completion time
            await self._update_average_timing(f"{base_key}:avg_time", completion.completion_time)
            
            # Store completion path for analysis
            await self.cache.rpush(
                f"{base_key}:paths",
                ','.join(step['field_name'] for step in completion.completion_path)
            )
            
        except Exception as e:
            logger.error(f"Failed to update completion metrics: {e}")
    
    async def _update_abandonment_metrics(self, abandonment: FormAbandonment) -> None:
        """Update abandonment metrics in cache."""
        try:
            base_key = f"abandonment_metrics:{abandonment.form_type}"
            
            # Update abandonment count
            await self.cache.incr(f"{base_key}:total")
            
            # Track abandonment reasons
            reason_key = f"{base_key}:reasons:{abandonment.abandonment_reason['type']}"
            await self.cache.incr(reason_key)
            
            # Track incomplete fields
            for field in abandonment.incomplete_fields:
                await self.cache.incr(f"{base_key}:incomplete:{field}")
            
        except Exception as e:
            logger.error(f"Failed to update abandonment metrics: {e}")
    
    async def _update_average_timing(self, key: str, new_value: float) -> None:
        """Update running average in cache."""
        try:
            current = await self.cache.get(key)
            count_key = f"{key}:count"
            count = await self.cache.incr(count_key)
            
            if current:
                current = float(current)
                new_avg = ((current * (count - 1)) + new_value) / count
            else:
                new_avg = new_value
            
            await self.cache.set(key, str(new_avg))
            
        except Exception as e:
            logger.error(f"Failed to update average timing: {e}")
    
    async def _get_real_time_metrics(self, form_type: str) -> Dict[str, Any]:
        """Get real-time metrics from cache."""
        try:
            base_key = f"completion_metrics:{form_type}"
            
            return {
                'active_sessions': await self.cache.scard(f"active_sessions:{form_type}"),
                'recent_completions': await self.cache.get(f"{base_key}:total") or 0,
                'avg_completion_time': float(await self.cache.get(f"{base_key}:avg_time") or 0),
                'recent_paths': await self.cache.lrange(f"{base_key}:paths", -5, -1)
            }
            
        except Exception as e:
            logger.error(f"Failed to get real-time metrics: {e}")
            return {}
    
    async def _get_real_time_success_rate(self, form_type: str) -> float:
        """Calculate real-time success rate."""
        try:
            completions = int(await self.cache.get(f"completion_metrics:{form_type}:total") or 0)
            abandonments = int(await self.cache.get(f"abandonment_metrics:{form_type}:total") or 0)
            
            total = completions + abandonments
            return (completions / total * 100) if total > 0 else 0
            
        except Exception as e:
            logger.error(f"Failed to calculate real-time success rate: {e}")
            return 0.0

# Create singleton instance
analytics_service = AnalyticsService("YOUR_GA4_PROPERTY_ID")

async def track_event(event_name, properties=None):
    """Track an event using the analytics service"""
    if properties is None:
        properties = {}
    
    try:
        # Log the event
        logger.info(f"EVENT: {event_name} - {json.dumps(properties)}")
        
        # In production, you'd send this to your analytics service
        # For now, we'll just log it
        
        # Example of how you might send to an analytics service:
        # await analytics_client.track(event_name, properties)
        
        return True
    except Exception as e:
        logger.error(f"Error tracking event {event_name}: {str(e)}")
        return False

def track_event_flask(event_name, properties=None):
    """Synchronous version of track_event for Flask"""
    if properties is None:
        properties = {}
    
    try:
        # Log the event
        logger.info(f"EVENT: {event_name} - {json.dumps(properties)}")
        
        # In production, you'd send this to your analytics service
        # For now, we'll just log it
        
        return True
    except Exception as e:
        logger.error(f"Error tracking event {event_name}: {str(e)}")
        return False 