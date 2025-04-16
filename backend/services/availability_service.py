from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

class AvailabilityStatus:
    ONLINE = "online"
    BUSY = "busy"
    AWAY = "away"
    OFFLINE = "offline"

class AvailabilityService:
    def __init__(self):
        self.data_path = os.path.join('data', 'availability')
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_path, exist_ok=True)
        
    def _get_status_file(self, user_id: str) -> str:
        """Get path to user's status file"""
        return os.path.join(self.data_path, f"{user_id}_status.json")
        
    def _get_schedule_file(self, user_id: str) -> str:
        """Get path to user's schedule file"""
        return os.path.join(self.data_path, f"{user_id}_schedule.json")

    def update_status(self, user_id: str, status: str, expires_in: Optional[int] = None) -> Dict:
        """Update a user's availability status"""
        try:
            if status not in vars(AvailabilityStatus).values():
                raise ValueError(f"Invalid status: {status}")
                
            status_data = {
                'status': status,
                'updated_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(minutes=expires_in)).isoformat() if expires_in else None
            }
            
            with open(self._get_status_file(user_id), 'w') as f:
                json.dump(status_data, f, indent=2)
                
            return status_data
        except Exception as e:
            raise Exception(f"Failed to update status: {str(e)}")

    def get_status(self, user_id: str) -> Optional[Dict]:
        """Get a user's current availability status"""
        try:
            with open(self._get_status_file(user_id), 'r') as f:
                status_data = json.load(f)
                
            # Check if status has expired
            if status_data.get('expires_at'):
                expires_at = datetime.fromisoformat(status_data['expires_at'])
                if datetime.now() > expires_at:
                    status_data['status'] = AvailabilityStatus.OFFLINE
                    self.update_status(user_id, AvailabilityStatus.OFFLINE)
                    
            return status_data
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Failed to get status: {str(e)}")

    def update_schedule(self, user_id: str, schedule: Dict) -> Dict:
        """Update a user's availability schedule"""
        try:
            with open(self._get_schedule_file(user_id), 'w') as f:
                json.dump({
                    'schedule': schedule,
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2)
                
            return schedule
        except Exception as e:
            raise Exception(f"Failed to update schedule: {str(e)}")

    def get_schedule(self, user_id: str) -> Optional[Dict]:
        """Get a user's availability schedule"""
        try:
            with open(self._get_schedule_file(user_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Failed to get schedule: {str(e)}")

    def get_available_lawyers(self, specialty: Optional[str] = None) -> List[Dict]:
        """Get list of currently available lawyers"""
        try:
            available_lawyers = []
            status_files = [f for f in os.listdir(self.data_path) if f.endswith('_status.json')]
            
            for status_file in status_files:
                user_id = status_file.replace('_status.json', '')
                status_data = self.get_status(user_id)
                
                if status_data and status_data['status'] in [AvailabilityStatus.ONLINE, AvailabilityStatus.AWAY]:
                    # Get user profile (assuming we have a user service)
                    # This should be replaced with actual user service call
                    lawyer_data = {
                        'user_id': user_id,
                        'status': status_data['status'],
                        'last_updated': status_data['updated_at']
                    }
                    
                    if specialty:
                        # Add logic to check lawyer's specialty
                        pass
                        
                    available_lawyers.append(lawyer_data)
                    
            return available_lawyers
        except Exception as e:
            raise Exception(f"Failed to get available lawyers: {str(e)}")

    def get_next_available_slot(self, user_id: str) -> Optional[datetime]:
        """Get the next available time slot for a lawyer"""
        try:
            schedule = self.get_schedule(user_id)
            if not schedule:
                return None
                
            now = datetime.now()
            # Add logic to find next available slot based on schedule
            # This is a placeholder implementation
            return now + timedelta(hours=1)
        except Exception as e:
            raise Exception(f"Failed to get next available slot: {str(e)}")

# Create global instance
availability_service = AvailabilityService() 