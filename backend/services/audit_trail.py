from datetime import datetime
import os
import json
from typing import Dict, List, Optional
import hashlib

class AuditTrailService:
    def __init__(self):
        self.audit_path = os.path.join('data', 'audit_trails')
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.audit_path, exist_ok=True)

    def _generate_event_id(self) -> str:
        """Generate a unique event ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"event_{timestamp}_{os.urandom(4).hex()}"

    def _get_audit_file_path(self, entity_id: str) -> str:
        """Get the path to an entity's audit trail file"""
        return os.path.join(self.audit_path, f"{entity_id}_audit.json")

    def _load_audit_trail(self, entity_id: str) -> List[Dict]:
        """Load an entity's audit trail"""
        try:
            with open(self._get_audit_file_path(entity_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_audit_trail(self, entity_id: str, trail: List[Dict]):
        """Save an entity's audit trail"""
        with open(self._get_audit_file_path(entity_id), 'w') as f:
            json.dump(trail, f, indent=2)

    def _calculate_hash(self, event: Dict) -> str:
        """Calculate a hash of the event data"""
        event_str = json.dumps(event, sort_keys=True)
        return hashlib.sha256(event_str.encode()).hexdigest()

    def log_event(self, entity_id: str, event_type: str, user_id: str, details: Dict) -> str:
        """
        Log an audit event
        Returns the event ID
        """
        try:
            event_id = self._generate_event_id()
            
            # Create event record
            event = {
                'event_id': event_id,
                'entity_id': entity_id,
                'event_type': event_type,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'details': details
            }
            
            # Calculate event hash (for integrity)
            event['hash'] = self._calculate_hash(event)
            
            # Load existing trail
            trail = self._load_audit_trail(entity_id)
            
            # Add new event
            trail.append(event)
            
            # Save updated trail
            self._save_audit_trail(entity_id, trail)
            
            return event_id
        except Exception as e:
            raise ValueError(f"Failed to log audit event: {str(e)}")

    def get_audit_trail(self, entity_id: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Get an entity's audit trail with optional filters"""
        try:
            trail = self._load_audit_trail(entity_id)
            
            if filters:
                filtered_trail = []
                for event in trail:
                    match = all(
                        event.get(key) == value 
                        for key, value in filters.items()
                    )
                    if match:
                        filtered_trail.append(event)
                return filtered_trail
            
            return trail
        except Exception:
            return []

    def verify_trail_integrity(self, entity_id: str) -> bool:
        """Verify the integrity of an audit trail"""
        try:
            trail = self._load_audit_trail(entity_id)
            
            for event in trail:
                # Store original hash
                original_hash = event['hash']
                
                # Remove hash for recalculation
                event_copy = event.copy()
                event_copy.pop('hash')
                
                # Recalculate hash
                calculated_hash = self._calculate_hash(event_copy)
                
                # Compare hashes
                if calculated_hash != original_hash:
                    return False
            
            return True
        except Exception:
            return False

    def get_entity_events_by_type(self, entity_id: str, event_type: str) -> List[Dict]:
        """Get all events of a specific type for an entity"""
        return self.get_audit_trail(entity_id, {'event_type': event_type})

    def get_user_events(self, user_id: str) -> List[Dict]:
        """Get all events performed by a user across all entities"""
        all_events = []
        try:
            for filename in os.listdir(self.audit_path):
                if filename.endswith('_audit.json'):
                    entity_id = filename.replace('_audit.json', '')
                    entity_events = self.get_audit_trail(entity_id, {'user_id': user_id})
                    all_events.extend(entity_events)
            
            return sorted(all_events, key=lambda x: x['timestamp'], reverse=True)
        except Exception:
            return []

    def get_recent_events(self, limit: int = 100) -> List[Dict]:
        """Get recent events across all entities"""
        all_events = []
        try:
            for filename in os.listdir(self.audit_path):
                if filename.endswith('_audit.json'):
                    entity_id = filename.replace('_audit.json', '')
                    entity_events = self.get_audit_trail(entity_id)
                    all_events.extend(entity_events)
            
            return sorted(
                all_events, 
                key=lambda x: x['timestamp'], 
                reverse=True
            )[:limit]
        except Exception:
            return []

# Create a global instance
audit_trail_service = AuditTrailService() 