"""
Human-in-the-loop functionality for LangGraph
Allows human review and intervention at key points in the workflow
"""

import os
import json
from typing import Dict, Any, Optional, Literal
from datetime import datetime, timedelta
from enum import Enum
from .supabase_client import sb

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class HumanReviewRequest:
    """Represents a request for human review"""
    
    def __init__(self, request_id: str, thread_id: str, node_name: str, 
                 state: Dict[str, Any], review_type: str, timeout_minutes: int = 60):
        self.request_id = request_id
        self.thread_id = thread_id
        self.node_name = node_name
        self.state = state
        self.review_type = review_type
        self.timeout_minutes = timeout_minutes
        self.created_at = datetime.now()
        self.status = ReviewStatus.PENDING
        self.human_feedback = None
        self.modified_state = None

class HumanInTheLoopManager:
    """Manages human-in-the-loop interactions"""
    
    def __init__(self):
        self.table_name = "human_reviews"
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the human reviews table exists"""
        pass
    
    def create_review_request(self, thread_id: str, node_name: str, 
                            state: Dict[str, Any], review_type: str,
                            timeout_minutes: int = 60) -> str:
        """Create a new human review request"""
        request_id = f"{thread_id}_{node_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        review_request = {
            "id": request_id,
            "thread_id": thread_id,
            "node_name": node_name,
            "state": json.dumps(state),
            "review_type": review_type,
            "status": ReviewStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "timeout_at": (datetime.now() + timedelta(minutes=timeout_minutes)).isoformat(),
            "human_feedback": None,
            "modified_state": None
        }
        
        try:
            sb().table(self.table_name).insert(review_request).execute()
            return request_id
        except Exception as e:
            print(f"Error creating review request: {e}")
            return None
    
    def get_review_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get a review request by ID"""
        try:
            result = sb().table(self.table_name).select("*").eq("id", request_id).execute()
            if result.data:
                review = result.data[0]
                return {
                    "id": review["id"],
                    "thread_id": review["thread_id"],
                    "node_name": review["node_name"],
                    "state": json.loads(review["state"]),
                    "review_type": review["review_type"],
                    "status": review["status"],
                    "created_at": review["created_at"],
                    "timeout_at": review["timeout_at"],
                    "human_feedback": review["human_feedback"],
                    "modified_state": json.loads(review["modified_state"]) if review["modified_state"] else None
                }
            return None
        except Exception as e:
            print(f"Error getting review request: {e}")
            return None
    
    def submit_review(self, request_id: str, status: ReviewStatus, 
                     feedback: str = None, modified_state: Dict[str, Any] = None):
        """Submit human review"""
        try:
            update_data = {
                "status": status.value,
                "human_feedback": feedback,
                "modified_state": json.dumps(modified_state) if modified_state else None,
                "reviewed_at": datetime.now().isoformat()
            }
            
            sb().table(self.table_name).update(update_data).eq("id", request_id).execute()
            return True
        except Exception as e:
            print(f"Error submitting review: {e}")
            return False
    
    def wait_for_review(self, request_id: str, timeout_seconds: int = 300) -> Optional[Dict[str, Any]]:
        """Wait for human review (polling)"""
        import time
        
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            review = self.get_review_request(request_id)
            if review and review["status"] != ReviewStatus.PENDING.value:
                return review
            
            time.sleep(5)  # Poll every 5 seconds
        
        return None
    
    def list_pending_reviews(self, limit: int = 10) -> list:
        """List pending review requests"""
        try:
            result = (sb().table(self.table_name)
                     .select("*")
                     .eq("status", ReviewStatus.PENDING.value)
                     .order("created_at", desc=True)
                     .limit(limit)
                     .execute())
            
            return result.data
        except Exception as e:
            print(f"Error listing pending reviews: {e}")
            return []

# Global human-in-the-loop manager
human_manager = HumanInTheLoopManager()

def require_human_review(node_name: str, review_type: str = "quality_check", 
                        timeout_minutes: int = 60):
    """Decorator to require human review at a specific node"""
    def decorator(func):
        def wrapper(ctx, *args, **kwargs):
            # Check if human review is enabled
            if os.environ.get("ENABLE_HUMAN_REVIEW", "false").lower() != "true":
                return func(ctx, *args, **kwargs)
            
            # Create review request
            thread_id = ctx.state.get("intake_id", "default")
            request_id = human_manager.create_review_request(
                thread_id, node_name, ctx.state, review_type, timeout_minutes
            )
            
            if request_id:
                print(f"Human review required at {node_name}. Request ID: {request_id}")
                print(f"State: {json.dumps(ctx.state, indent=2)}")
                
                # Wait for review
                review = human_manager.wait_for_review(request_id, timeout_seconds=300)
                
                if review:
                    if review["status"] == ReviewStatus.APPROVED.value:
                        # Continue with original function
                        return func(ctx, *args, **kwargs)
                    elif review["status"] == ReviewStatus.MODIFIED.value:
                        # Use modified state
                        if review["modified_state"]:
                            ctx.state.update(review["modified_state"])
                        return func(ctx, *args, **kwargs)
                    else:
                        # Rejected or timeout
                        ctx.state["status"] = "rejected"
                        ctx.state["human_feedback"] = review.get("human_feedback", "Review rejected")
                        return ctx.state
                else:
                    # Timeout
                    ctx.state["status"] = "timeout"
                    ctx.state["human_feedback"] = "Human review timeout"
                    return ctx.state
            else:
                # Fallback to original function if review creation fails
                return func(ctx, *args, **kwargs)
        
        return wrapper
    return decorator

def create_review_endpoint(app):
    """Create FastAPI endpoints for human review"""
    
    @app.get("/human-reviews/pending")
    def get_pending_reviews():
        """Get pending human review requests"""
        reviews = human_manager.list_pending_reviews()
        return {"reviews": reviews}
    
    @app.get("/human-reviews/{request_id}")
    def get_review_request(request_id: str):
        """Get a specific review request"""
        review = human_manager.get_review_request(request_id)
        if review:
            return {"review": review}
        else:
            return {"error": "Review request not found"}
    
    @app.post("/human-reviews/{request_id}/submit")
    def submit_review(request_id: str, status: str, feedback: str = None, 
                     modified_state: Dict[str, Any] = None):
        """Submit human review"""
        try:
            review_status = ReviewStatus(status)
            success = human_manager.submit_review(request_id, review_status, feedback, modified_state)
            if success:
                return {"success": True, "message": "Review submitted successfully"}
            else:
                return {"success": False, "message": "Failed to submit review"}
        except ValueError:
            return {"success": False, "message": "Invalid status"}
        except Exception as e:
            return {"success": False, "message": str(e)}
