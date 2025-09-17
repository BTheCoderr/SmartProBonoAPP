"""
Real-time Case Updates Agent
Monitors for new case law updates and provides real-time notifications
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
import json
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CaseUpdate:
    """Represents a real-time case update"""
    case_id: str
    case_name: str
    court: str
    jurisdiction: str
    update_type: str  # 'new_decision', 'status_change', 'deadline_reminder'
    description: str
    timestamp: datetime
    urgency: str  # 'low', 'medium', 'high', 'critical'
    relevant_queries: List[str]
    action_required: Optional[str] = None

class RealtimeAgent:
    """Agent for monitoring and providing real-time case updates"""
    
    def __init__(self):
        self.courtlistener_base_url = "https://www.courtlistener.com/api/rest/v3"
        self.last_check = datetime.now() - timedelta(hours=1)
        self.subscribed_queries = []
        self.update_cache = []
        
    def subscribe_to_updates(self, query: str, jurisdiction: str = "ri") -> bool:
        """Subscribe to real-time updates for a specific query"""
        try:
            subscription = {
                "query": query,
                "jurisdiction": jurisdiction,
                "subscribed_at": datetime.now(),
                "last_update": None
            }
            self.subscribed_queries.append(subscription)
            logger.info(f"Subscribed to updates for query: {query}")
            return True
        except Exception as e:
            logger.error(f"Error subscribing to updates: {e}")
            return False
    
    def check_for_updates(self) -> List[CaseUpdate]:
        """Check for new case law updates since last check"""
        updates = []
        
        try:
            # Check CourtListener for recent cases
            recent_cases = self._fetch_recent_cases()
            
            for case in recent_cases:
                # Check if case matches any subscribed queries
                for subscription in self.subscribed_queries:
                    if self._is_case_relevant(case, subscription["query"]):
                        update = self._create_case_update(case, subscription)
                        updates.append(update)
            
            # Update last check time
            self.last_check = datetime.now()
            
            # Cache updates
            self.update_cache.extend(updates)
            
            logger.info(f"Found {len(updates)} new case updates")
            return updates
            
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return []
    
    def _fetch_recent_cases(self) -> List[Dict[str, Any]]:
        """Fetch recent cases from CourtListener API"""
        try:
            # Calculate date range for recent cases
            start_date = self.last_check.strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
            
            params = {
                "filed_after": start_date,
                "filed_before": end_date,
                "order_by": "filed_date desc",
                "stat_Precedential": "on",
                "format": "json"
            }
            
            response = requests.get(
                f"{self.courtlistener_base_url}/search/",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                logger.warning(f"CourtListener API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching recent cases: {e}")
            return []
    
    def _is_case_relevant(self, case: Dict[str, Any], query: str) -> bool:
        """Check if a case is relevant to a subscribed query"""
        try:
            # Simple keyword matching - in production, use more sophisticated NLP
            query_keywords = set(query.lower().split())
            
            # Check case name, text, and other fields
            case_text = " ".join([
                case.get("caseName", ""),
                case.get("snippet", ""),
                case.get("text", "")
            ]).lower()
            
            case_keywords = set(case_text.split())
            
            # Check for keyword overlap
            overlap = len(query_keywords.intersection(case_keywords))
            relevance_score = overlap / len(query_keywords) if query_keywords else 0
            
            return relevance_score > 0.3  # 30% keyword overlap threshold
            
        except Exception as e:
            logger.error(f"Error checking case relevance: {e}")
            return False
    
    def _create_case_update(self, case: Dict[str, Any], subscription: Dict[str, Any]) -> CaseUpdate:
        """Create a CaseUpdate object from case data"""
        try:
            # Determine update type and urgency
            update_type = "new_decision"
            urgency = "medium"
            
            # Check if case is very recent (within 24 hours)
            case_date = datetime.fromisoformat(case.get("dateFiled", "").replace("Z", "+00:00"))
            hours_old = (datetime.now() - case_date).total_seconds() / 3600
            
            if hours_old < 24:
                urgency = "high"
            elif hours_old < 168:  # 1 week
                urgency = "medium"
            else:
                urgency = "low"
            
            # Determine if action is required
            action_required = None
            if urgency == "high":
                action_required = "Review immediately - recent case law may affect your case"
            elif urgency == "medium":
                action_required = "Review when convenient - new relevant case law available"
            
            return CaseUpdate(
                case_id=case.get("id", ""),
                case_name=case.get("caseName", "Unknown Case"),
                court=case.get("court", "Unknown Court"),
                jurisdiction=case.get("jurisdiction", subscription.get("jurisdiction", "ri")),
                update_type=update_type,
                description=case.get("snippet", "New case law update"),
                timestamp=case_date,
                urgency=urgency,
                relevant_queries=[subscription["query"]],
                action_required=action_required
            )
            
        except Exception as e:
            logger.error(f"Error creating case update: {e}")
            # Return a basic update
            return CaseUpdate(
                case_id=case.get("id", "unknown"),
                case_name=case.get("caseName", "Unknown Case"),
                court=case.get("court", "Unknown Court"),
                jurisdiction="ri",
                update_type="new_decision",
                description="New case law update",
                timestamp=datetime.now(),
                urgency="medium",
                relevant_queries=[subscription["query"]]
            )
    
    def get_updates_for_query(self, query: str) -> List[CaseUpdate]:
        """Get all updates for a specific query"""
        return [update for update in self.update_cache if query in update.relevant_queries]
    
    def get_urgent_updates(self) -> List[CaseUpdate]:
        """Get all urgent updates (high or critical urgency)"""
        return [update for update in self.update_cache if update.urgency in ["high", "critical"]]
    
    def clear_old_updates(self, days: int = 7):
        """Clear updates older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        self.update_cache = [
            update for update in self.update_cache 
            if update.timestamp > cutoff_date
        ]
        logger.info(f"Cleared updates older than {days} days")

# Global instance
realtime_agent = RealtimeAgent()

def subscribe_to_updates(query: str, jurisdiction: str = "ri") -> bool:
    """Subscribe to real-time updates for a query"""
    return realtime_agent.subscribe_to_updates(query, jurisdiction)

def check_for_updates() -> List[CaseUpdate]:
    """Check for new case law updates"""
    return realtime_agent.check_for_updates()

def get_updates_for_query(query: str) -> List[CaseUpdate]:
    """Get updates for a specific query"""
    return realtime_agent.get_updates_for_query(query)

def get_urgent_updates() -> List[CaseUpdate]:
    """Get urgent updates"""
    return realtime_agent.get_urgent_updates()
