"""
Checkpointing system for durable execution in LangGraph
Based on official LangGraph checkpointing patterns
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from .supabase_client import sb

class SupabaseCheckpointSaver:
    """Checkpoint saver using Supabase for persistence"""
    
    def __init__(self):
        self.table_name = "langgraph_checkpoints"
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """Ensure the checkpoints table exists"""
        # This would typically be done via Supabase migrations
        # For now, we'll assume the table exists or create it manually
        pass
    
    def save_checkpoint(self, thread_id: str, checkpoint_data: Dict[str, Any]) -> str:
        """Save a checkpoint for a thread"""
        checkpoint_id = f"{thread_id}_{datetime.now().isoformat()}"
        
        checkpoint_record = {
            "id": checkpoint_id,
            "thread_id": thread_id,
            "checkpoint_data": json.dumps(checkpoint_record),
            "created_at": datetime.now().isoformat(),
            "metadata": checkpoint_data.get("metadata", {})
        }
        
        try:
            sb().table(self.table_name).insert(checkpoint_record).execute()
            return checkpoint_id
        except Exception as e:
            print(f"Error saving checkpoint: {e}")
            return None
    
    def get_latest_checkpoint(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest checkpoint for a thread"""
        try:
            result = (sb().table(self.table_name)
                     .select("*")
                     .eq("thread_id", thread_id)
                     .order("created_at", desc=True)
                     .limit(1)
                     .execute())
            
            if result.data:
                checkpoint = result.data[0]
                return {
                    "checkpoint_id": checkpoint["id"],
                    "thread_id": checkpoint["thread_id"],
                    "data": json.loads(checkpoint["checkpoint_data"]),
                    "created_at": checkpoint["created_at"]
                }
            return None
        except Exception as e:
            print(f"Error getting checkpoint: {e}")
            return None
    
    def list_checkpoints(self, thread_id: str, limit: int = 10) -> list:
        """List checkpoints for a thread"""
        try:
            result = (sb().table(self.table_name)
                     .select("*")
                     .eq("thread_id", thread_id)
                     .order("created_at", desc=True)
                     .limit(limit)
                     .execute())
            
            return result.data
        except Exception as e:
            print(f"Error listing checkpoints: {e}")
            return []

class MemoryCheckpointSaver:
    """In-memory checkpoint saver for development/testing"""
    
    def __init__(self):
        self.checkpoints: Dict[str, list] = {}
    
    def save_checkpoint(self, thread_id: str, checkpoint_data: Dict[str, Any]) -> str:
        """Save a checkpoint in memory"""
        checkpoint_id = f"{thread_id}_{datetime.now().isoformat()}"
        
        if thread_id not in self.checkpoints:
            self.checkpoints[thread_id] = []
        
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "thread_id": thread_id,
            "data": checkpoint_data,
            "created_at": datetime.now().isoformat()
        }
        
        self.checkpoints[thread_id].append(checkpoint)
        return checkpoint_id
    
    def get_latest_checkpoint(self, thread_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest checkpoint for a thread"""
        if thread_id in self.checkpoints and self.checkpoints[thread_id]:
            return self.checkpoints[thread_id][-1]
        return None
    
    def list_checkpoints(self, thread_id: str, limit: int = 10) -> list:
        """List checkpoints for a thread"""
        if thread_id in self.checkpoints:
            return self.checkpoints[thread_id][-limit:]
        return []

# Global checkpoint saver instance
def get_checkpoint_saver():
    """Get the appropriate checkpoint saver based on environment"""
    if os.environ.get("USE_SUPABASE_CHECKPOINTS", "false").lower() == "true":
        return SupabaseCheckpointSaver()
    else:
        return MemoryCheckpointSaver()

# Decorator for automatic checkpointing
def with_checkpointing(func):
    """Decorator to add checkpointing to graph functions"""
    def wrapper(*args, **kwargs):
        # Extract thread_id from args or kwargs
        thread_id = kwargs.get("thread_id", "default")
        
        # Get checkpoint saver
        saver = get_checkpoint_saver()
        
        # Try to resume from checkpoint
        checkpoint = saver.get_latest_checkpoint(thread_id)
        if checkpoint:
            print(f"Resuming from checkpoint: {checkpoint['checkpoint_id']}")
            # You would restore state here
        
        # Execute the function
        result = func(*args, **kwargs)
        
        # Save checkpoint
        checkpoint_data = {
            "function": func.__name__,
            "args": str(args),
            "kwargs": str(kwargs),
            "result": str(result),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "function_name": func.__name__
            }
        }
        
        saver.save_checkpoint(thread_id, checkpoint_data)
        
        return result
    
    return wrapper
