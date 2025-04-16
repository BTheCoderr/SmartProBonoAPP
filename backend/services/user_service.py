import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class UserService:
    def __init__(self):
        self.users_file = 'data/users.json'
        self._ensure_data_file()

    def _ensure_data_file(self) -> None:
        """Ensure the users data file exists"""
        try:
            with open(self.users_file, 'r') as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.users_file, 'w') as f:
                json.dump({'users': []}, f)

    def _load_users(self) -> List[Dict[str, Any]]:
        """Load users from the data file"""
        with open(self.users_file, 'r') as f:
            data = json.load(f)
            return data.get('users', [])

    def _save_users(self, users: List[Dict[str, Any]]) -> None:
        """Save users to the data file"""
        with open(self.users_file, 'w') as f:
            json.dump({'users': users}, f, indent=2)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by their ID"""
        users = self._load_users()
        return next((user for user in users if user['id'] == user_id), None)

    def get_available_attorneys(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available attorneys based on filters"""
        users = self._load_users()
        attorneys = [
            user for user in users 
            if user['role'] == 'volunteer_attorney'
        ]

        # Apply additional filters
        if filters.get('availability'):
            attorneys = [
                atty for atty in attorneys 
                if atty['profile'].get('availability') == filters['availability']
            ]

        if filters.get('specialties'):
            attorneys = [
                atty for atty in attorneys 
                if any(spec in atty['profile'].get('specialties', []) 
                      for spec in filters['specialties'])
            ]

        return attorneys

    def update_availability(self, user_id: str, availability_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a user's availability settings"""
        users = self._load_users()
        user_index = next((i for i, user in enumerate(users) if user['id'] == user_id), -1)
        
        if user_index == -1:
            return None

        users[user_index]['profile']['availability'] = availability_data
        users[user_index]['updated_at'] = datetime.utcnow().isoformat()
        
        self._save_users(users)
        return users[user_index]

    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a user's profile"""
        users = self._load_users()
        user_index = next((i for i, user in enumerate(users) if user['id'] == user_id), -1)
        
        if user_index == -1:
            return None

        # Update only allowed fields
        allowed_fields = {'full_name', 'phone', 'language', 'specialties', 'bar_number', 'location'}
        for field in allowed_fields:
            if field in profile_data:
                users[user_index]['profile'][field] = profile_data[field]

        users[user_index]['updated_at'] = datetime.utcnow().isoformat()
        
        self._save_users(users)
        return users[user_index] 