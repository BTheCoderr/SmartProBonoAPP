"""
User activity tracking service for comprehensive user behavior analytics.
"""
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from flask import request, g, current_app
from database import db
from models.audit import UserActivity
from services.audit_service import audit_service
from models.audit import AuditEventType

logger = logging.getLogger(__name__)

class UserActivityService:
    """Service for tracking and analyzing user activities."""
    
    def __init__(self):
        self.session_activities = {}
        self.activity_patterns = {}
    
    def track_page_view(
        self,
        user_id: int,
        page_url: str,
        page_title: str = None,
        referrer: str = None,
        duration_seconds: int = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track a page view event."""
        try:
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="page_view",
                page_url=page_url,
                page_title=page_title,
                referrer=referrer,
                duration_seconds=duration_seconds,
                metadata=metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "page_view", page_url)
            
            # Analyze activity patterns
            self._analyze_activity_pattern(user_id, "page_view", page_url)
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking page view: {str(e)}")
            raise
    
    def track_user_click(
        self,
        user_id: int,
        element_id: str = None,
        element_class: str = None,
        page_url: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track a user click event."""
        try:
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="click",
                page_url=page_url,
                element_id=element_id,
                element_class=element_class,
                metadata=metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "click", element_id or element_class)
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking user click: {str(e)}")
            raise
    
    def track_form_submission(
        self,
        user_id: int,
        form_type: str,
        page_url: str = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track a form submission event."""
        try:
            activity_metadata = {
                "form_type": form_type,
                "success": success,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="form_submission",
                page_url=page_url,
                metadata=activity_metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "form_submission", form_type)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.USER_ACTIVITY,
                action="FORM_SUBMIT",
                user_id=user_id,
                description=f"Form submitted: {form_type}",
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking form submission: {str(e)}")
            raise
    
    def track_file_download(
        self,
        user_id: int,
        file_name: str,
        file_size: int = None,
        file_type: str = None,
        page_url: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track a file download event."""
        try:
            activity_metadata = {
                "file_name": file_name,
                "file_size": file_size,
                "file_type": file_type,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="file_download",
                page_url=page_url,
                metadata=activity_metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "file_download", file_name)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.USER_ACTIVITY,
                action="FILE_DOWNLOAD",
                user_id=user_id,
                description=f"File downloaded: {file_name}",
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking file download: {str(e)}")
            raise
    
    def track_search_query(
        self,
        user_id: int,
        query: str,
        results_count: int = None,
        page_url: str = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track a search query event."""
        try:
            activity_metadata = {
                "query": query,
                "results_count": results_count,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="search_query",
                page_url=page_url,
                metadata=activity_metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "search_query", query)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.USER_ACTIVITY,
                action="SEARCH",
                user_id=user_id,
                description=f"Search performed: {query}",
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking search query: {str(e)}")
            raise
    
    def track_user_session(
        self,
        user_id: int,
        session_start: datetime = None,
        session_end: datetime = None,
        pages_visited: int = None,
        actions_performed: int = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track user session information."""
        try:
            session_duration = None
            if session_start and session_end:
                session_duration = int((session_end - session_start).total_seconds())
            
            activity_metadata = {
                "session_start": session_start.isoformat() if session_start else None,
                "session_end": session_end.isoformat() if session_end else None,
                "pages_visited": pages_visited,
                "actions_performed": actions_performed,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="session",
                duration_seconds=session_duration,
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking user session: {str(e)}")
            raise
    
    def track_user_login(
        self,
        user_id: int,
        login_method: str = "password",
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track user login events."""
        try:
            activity_metadata = {
                "login_method": login_method,
                "success": success,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="login",
                metadata=activity_metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "login", login_method)
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.USER_ACTIVITY,
                action="LOGIN",
                user_id=user_id,
                description=f"User login: {login_method}",
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking user login: {str(e)}")
            raise
    
    def track_user_logout(
        self,
        user_id: int,
        session_duration: int = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track user logout events."""
        try:
            activity_metadata = {
                "session_duration": session_duration,
                **(metadata or {})
            }
            
            activity = audit_service.log_user_activity(
                user_id=user_id,
                activity_type="logout",
                duration_seconds=session_duration,
                metadata=activity_metadata
            )
            
            # Update session tracking
            self._update_session_activity(user_id, "logout", "session_end")
            
            # Log as audit event
            audit_service.log_audit_event(
                event_type=AuditEventType.USER_ACTIVITY,
                action="LOGOUT",
                user_id=user_id,
                description="User logout",
                metadata=activity_metadata
            )
            
            return activity
            
        except Exception as e:
            logger.error(f"Error tracking user logout: {str(e)}")
            raise
    
    def get_user_activity_summary(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get a summary of user activity for the specified period."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get activities from database
            activities = audit_service.get_user_activities(
                user_id=user_id,
                start_date=start_date,
                limit=1000
            )
            
            # Analyze activities
            summary = {
                "user_id": user_id,
                "period_days": days,
                "total_activities": len(activities),
                "activity_types": {},
                "page_views": 0,
                "clicks": 0,
                "form_submissions": 0,
                "file_downloads": 0,
                "search_queries": 0,
                "sessions": 0,
                "most_visited_pages": {},
                "most_clicked_elements": {},
                "search_terms": {},
                "device_types": {},
                "browsers": {},
                "operating_systems": {},
                "average_session_duration": 0,
                "total_session_time": 0
            }
            
            session_durations = []
            
            for activity in activities:
                # Count activity types
                activity_type = activity.activity_type
                summary["activity_types"][activity_type] = summary["activity_types"].get(activity_type, 0) + 1
                
                # Count specific activities
                if activity_type == "page_view":
                    summary["page_views"] += 1
                    page_url = activity.page_url
                    if page_url:
                        summary["most_visited_pages"][page_url] = summary["most_visited_pages"].get(page_url, 0) + 1
                
                elif activity_type == "click":
                    summary["clicks"] += 1
                    element_id = activity.element_id or activity.element_class
                    if element_id:
                        summary["most_clicked_elements"][element_id] = summary["most_clicked_elements"].get(element_id, 0) + 1
                
                elif activity_type == "form_submission":
                    summary["form_submissions"] += 1
                
                elif activity_type == "file_download":
                    summary["file_downloads"] += 1
                
                elif activity_type == "search_query":
                    summary["search_queries"] += 1
                    metadata = activity.metadata_dict
                    if metadata and "query" in metadata:
                        query = metadata["query"]
                        summary["search_terms"][query] = summary["search_terms"].get(query, 0) + 1
                
                elif activity_type == "session":
                    summary["sessions"] += 1
                    if activity.duration_seconds:
                        session_durations.append(activity.duration_seconds)
                        summary["total_session_time"] += activity.duration_seconds
                
                # Track device information
                if activity.device_type:
                    summary["device_types"][activity.device_type] = summary["device_types"].get(activity.device_type, 0) + 1
                
                if activity.browser:
                    summary["browsers"][activity.browser] = summary["browsers"].get(activity.browser, 0) + 1
                
                if activity.os:
                    summary["operating_systems"][activity.os] = summary["operating_systems"].get(activity.os, 0) + 1
            
            # Calculate average session duration
            if session_durations:
                summary["average_session_duration"] = sum(session_durations) / len(session_durations)
            
            # Sort dictionaries by count
            summary["most_visited_pages"] = dict(sorted(summary["most_visited_pages"].items(), key=lambda x: x[1], reverse=True)[:10])
            summary["most_clicked_elements"] = dict(sorted(summary["most_clicked_elements"].items(), key=lambda x: x[1], reverse=True)[:10])
            summary["search_terms"] = dict(sorted(summary["search_terms"].items(), key=lambda x: x[1], reverse=True)[:10])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting user activity summary: {str(e)}")
            return {"error": str(e)}
    
    def get_user_activity_patterns(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Analyze user activity patterns."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get activities
            activities = audit_service.get_user_activities(
                user_id=user_id,
                start_date=start_date,
                limit=1000
            )
            
            patterns = {
                "user_id": user_id,
                "period_days": days,
                "hourly_activity": {},
                "daily_activity": {},
                "weekly_activity": {},
                "activity_flow": [],
                "peak_hours": [],
                "peak_days": [],
                "user_journey": []
            }
            
            for activity in activities:
                created_at = activity.created_at
                hour = created_at.hour
                day_of_week = created_at.strftime('%A')
                date = created_at.strftime('%Y-%m-%d')
                
                # Hourly activity
                patterns["hourly_activity"][hour] = patterns["hourly_activity"].get(hour, 0) + 1
                
                # Daily activity
                patterns["daily_activity"][day_of_week] = patterns["daily_activity"].get(day_of_week, 0) + 1
                
                # Date activity
                patterns["weekly_activity"][date] = patterns["weekly_activity"].get(date, 0) + 1
                
                # Activity flow
                patterns["activity_flow"].append({
                    "timestamp": created_at.isoformat(),
                    "activity_type": activity.activity_type,
                    "page_url": activity.page_url,
                    "action": activity.action
                })
                
                # User journey
                if activity.page_url:
                    patterns["user_journey"].append({
                        "timestamp": created_at.isoformat(),
                        "page_url": activity.page_url,
                        "page_title": activity.page_title,
                        "action": activity.action
                    })
            
            # Find peak hours and days
            if patterns["hourly_activity"]:
                peak_hour = max(patterns["hourly_activity"], key=patterns["hourly_activity"].get)
                patterns["peak_hours"] = [hour for hour, count in patterns["hourly_activity"].items() if count >= patterns["hourly_activity"][peak_hour] * 0.8]
            
            if patterns["daily_activity"]:
                peak_day = max(patterns["daily_activity"], key=patterns["daily_activity"].get)
                patterns["peak_days"] = [day for day, count in patterns["daily_activity"].items() if count >= patterns["daily_activity"][peak_day] * 0.8]
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing user activity patterns: {str(e)}")
            return {"error": str(e)}
    
    def _update_session_activity(self, user_id: int, activity_type: str, activity_data: str):
        """Update session activity tracking."""
        try:
            session_key = f"{user_id}_{getattr(g, 'session_id', 'default')}"
            
            if session_key not in self.session_activities:
                self.session_activities[session_key] = {
                    "user_id": user_id,
                    "start_time": datetime.utcnow(),
                    "activities": [],
                    "page_views": 0,
                    "clicks": 0,
                    "form_submissions": 0
                }
            
            session = self.session_activities[session_key]
            session["activities"].append({
                "type": activity_type,
                "data": activity_data,
                "timestamp": datetime.utcnow()
            })
            
            # Update counters
            if activity_type == "page_view":
                session["page_views"] += 1
            elif activity_type == "click":
                session["clicks"] += 1
            elif activity_type == "form_submission":
                session["form_submissions"] += 1
            
        except Exception as e:
            logger.error(f"Error updating session activity: {str(e)}")
    
    def _analyze_activity_pattern(self, user_id: int, activity_type: str, activity_data: str):
        """Analyze user activity patterns for insights."""
        try:
            if user_id not in self.activity_patterns:
                self.activity_patterns[user_id] = {
                    "frequent_actions": {},
                    "common_pages": {},
                    "behavior_patterns": []
                }
            
            pattern = self.activity_patterns[user_id]
            
            # Track frequent actions
            action_key = f"{activity_type}:{activity_data}"
            pattern["frequent_actions"][action_key] = pattern["frequent_actions"].get(action_key, 0) + 1
            
            # Track common pages
            if activity_type == "page_view":
                pattern["common_pages"][activity_data] = pattern["common_pages"].get(activity_data, 0) + 1
            
            # Store behavior pattern
            pattern["behavior_patterns"].append({
                "timestamp": datetime.utcnow(),
                "activity_type": activity_type,
                "activity_data": activity_data
            })
            
            # Keep only recent patterns (last 100)
            if len(pattern["behavior_patterns"]) > 100:
                pattern["behavior_patterns"] = pattern["behavior_patterns"][-100:]
            
        except Exception as e:
            logger.error(f"Error analyzing activity pattern: {str(e)}")

# Global user activity service instance
user_activity_service = UserActivityService()
