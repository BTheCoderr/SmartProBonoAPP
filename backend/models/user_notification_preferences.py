from models.database import db
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import json
from services.cache_service import get_cache_service
import uuid

class UserNotificationPreferences(db.Model):
    """User notification preferences model"""
    __tablename__ = 'user_notification_preferences'
    
    # Primary key
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), unique=True, nullable=False)
    
    # Channel settings
    _email_enabled = Column('email_enabled', Boolean, default=True)
    _app_enabled = Column('app_enabled', Boolean, default=True)
    _browser_enabled = Column('browser_enabled', Boolean, default=False)
    
    # Email notification settings
    _email_case_updates = Column('email_case_updates', Boolean, default=True)
    _email_document_updates = Column('email_document_updates', Boolean, default=True)
    _email_appointment_reminders = Column('email_appointment_reminders', Boolean, default=True)
    _email_messages = Column('email_messages', Boolean, default=True)
    _email_legal_ai_responses = Column('email_legal_ai_responses', Boolean, default=True)
    _email_system_announcements = Column('email_system_announcements', Boolean, default=True)
    
    # In-app notification settings
    _app_case_updates = Column('app_case_updates', Boolean, default=True)
    _app_document_updates = Column('app_document_updates', Boolean, default=True)
    _app_appointment_reminders = Column('app_appointment_reminders', Boolean, default=True)
    _app_messages = Column('app_messages', Boolean, default=True)
    _app_legal_ai_responses = Column('app_legal_ai_responses', Boolean, default=True)
    _app_system_announcements = Column('app_system_announcements', Boolean, default=True)
    
    # Browser notification settings
    _browser_case_updates = Column('browser_case_updates', Boolean, default=False)
    _browser_document_updates = Column('browser_document_updates', Boolean, default=False)
    _browser_appointment_reminders = Column('browser_appointment_reminders', Boolean, default=False)
    _browser_messages = Column('browser_messages', Boolean, default=False)
    _browser_legal_ai_responses = Column('browser_legal_ai_responses', Boolean, default=False)
    _browser_system_announcements = Column('browser_system_announcements', Boolean, default=False)
    
    # Timestamps
    _created_at = Column('created_at', DateTime, default=datetime.utcnow)
    _updated_at = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def cache_key(self):
        """Get cache key for this user's preferences"""
        return f"notification_preferences:{self.user_id}"

    def __init__(self, user_id, **kwargs):
        """Initialize user notification preferences"""
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        
        # Set attributes from kwargs with defaults
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    # Channel settings properties
    @hybrid_property
    def email_enabled(self):
        return bool(self._email_enabled)
    
    @email_enabled.setter
    def email_enabled(self, value):
        self._email_enabled = bool(value)
    
    @hybrid_property
    def app_enabled(self):
        return bool(self._app_enabled)
    
    @app_enabled.setter
    def app_enabled(self, value):
        self._app_enabled = bool(value)
    
    @hybrid_property
    def browser_enabled(self):
        return bool(self._browser_enabled)
    
    @browser_enabled.setter
    def browser_enabled(self, value):
        self._browser_enabled = bool(value)
        if not value:
            self._browser_case_updates = False
            self._browser_document_updates = False
            self._browser_appointment_reminders = False
            self._browser_messages = False
            self._browser_legal_ai_responses = False
            self._browser_system_announcements = False
    
    # Email notification settings properties
    @hybrid_property
    def email_case_updates(self):
        return bool(self._email_case_updates)
    
    @email_case_updates.setter
    def email_case_updates(self, value):
        self._email_case_updates = bool(value)
    
    @hybrid_property
    def email_document_updates(self):
        return bool(self._email_document_updates)
    
    @email_document_updates.setter
    def email_document_updates(self, value):
        self._email_document_updates = bool(value)
    
    @hybrid_property
    def email_appointment_reminders(self):
        return bool(self._email_appointment_reminders)
    
    @email_appointment_reminders.setter
    def email_appointment_reminders(self, value):
        self._email_appointment_reminders = bool(value)
    
    @hybrid_property
    def email_messages(self):
        return bool(self._email_messages)
    
    @email_messages.setter
    def email_messages(self, value):
        self._email_messages = bool(value)
    
    @hybrid_property
    def email_legal_ai_responses(self):
        return bool(self._email_legal_ai_responses)
    
    @email_legal_ai_responses.setter
    def email_legal_ai_responses(self, value):
        self._email_legal_ai_responses = bool(value)
    
    @hybrid_property
    def email_system_announcements(self):
        return bool(self._email_system_announcements)
    
    @email_system_announcements.setter
    def email_system_announcements(self, value):
        self._email_system_announcements = bool(value)
    
    # In-app notification settings properties
    @hybrid_property
    def app_case_updates(self):
        return bool(self._app_case_updates)
    
    @app_case_updates.setter
    def app_case_updates(self, value):
        self._app_case_updates = bool(value)
    
    @hybrid_property
    def app_document_updates(self):
        return bool(self._app_document_updates)
    
    @app_document_updates.setter
    def app_document_updates(self, value):
        self._app_document_updates = bool(value)
    
    @hybrid_property
    def app_appointment_reminders(self):
        return bool(self._app_appointment_reminders)
    
    @app_appointment_reminders.setter
    def app_appointment_reminders(self, value):
        self._app_appointment_reminders = bool(value)
    
    @hybrid_property
    def app_messages(self):
        return bool(self._app_messages)
    
    @app_messages.setter
    def app_messages(self, value):
        self._app_messages = bool(value)
    
    @hybrid_property
    def app_legal_ai_responses(self):
        return bool(self._app_legal_ai_responses)
    
    @app_legal_ai_responses.setter
    def app_legal_ai_responses(self, value):
        self._app_legal_ai_responses = bool(value)
    
    @hybrid_property
    def app_system_announcements(self):
        return bool(self._app_system_announcements)
    
    @app_system_announcements.setter
    def app_system_announcements(self, value):
        self._app_system_announcements = bool(value)
    
    # Browser notification settings properties
    @hybrid_property
    def browser_case_updates(self):
        return bool(self._browser_case_updates)
    
    @browser_case_updates.setter
    def browser_case_updates(self, value):
        self._browser_case_updates = bool(value)
    
    @hybrid_property
    def browser_document_updates(self):
        return bool(self._browser_document_updates)
    
    @browser_document_updates.setter
    def browser_document_updates(self, value):
        self._browser_document_updates = bool(value)
    
    @hybrid_property
    def browser_appointment_reminders(self):
        return bool(self._browser_appointment_reminders)
    
    @browser_appointment_reminders.setter
    def browser_appointment_reminders(self, value):
        self._browser_appointment_reminders = bool(value)
    
    @hybrid_property
    def browser_messages(self):
        return bool(self._browser_messages)
    
    @browser_messages.setter
    def browser_messages(self, value):
        self._browser_messages = bool(value)
    
    @hybrid_property
    def browser_legal_ai_responses(self):
        return bool(self._browser_legal_ai_responses)
    
    @browser_legal_ai_responses.setter
    def browser_legal_ai_responses(self, value):
        self._browser_legal_ai_responses = bool(value)
    
    @hybrid_property
    def browser_system_announcements(self):
        return bool(self._browser_system_announcements)
    
    @browser_system_announcements.setter
    def browser_system_announcements(self, value):
        self._browser_system_announcements = bool(value)
    
    # Timestamp properties
    @hybrid_property
    def created_at(self):
        return self._created_at
    
    @hybrid_property
    def updated_at(self):
        return self._updated_at
    
    def to_dict(self):
        """Convert preferences to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_enabled': self.email_enabled,
            'app_enabled': self.app_enabled,
            'browser_enabled': self.browser_enabled,
            'email_case_updates': self.email_case_updates,
            'email_document_updates': self.email_document_updates,
            'email_appointment_reminders': self.email_appointment_reminders,
            'email_messages': self.email_messages,
            'email_legal_ai_responses': self.email_legal_ai_responses,
            'email_system_announcements': self.email_system_announcements,
            'app_case_updates': self.app_case_updates,
            'app_document_updates': self.app_document_updates,
            'app_appointment_reminders': self.app_appointment_reminders,
            'app_messages': self.app_messages,
            'app_legal_ai_responses': self.app_legal_ai_responses,
            'app_system_announcements': self.app_system_announcements,
            'browser_case_updates': self.browser_case_updates,
            'browser_document_updates': self.browser_document_updates,
            'browser_appointment_reminders': self.browser_appointment_reminders,
            'browser_messages': self.browser_messages,
            'browser_legal_ai_responses': self.browser_legal_ai_responses,
            'browser_system_announcements': self.browser_system_announcements,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at is not None else None
        }
    
    def update_from_dict(self, data):
        """Update preferences from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, bool(value) if isinstance(value, bool) else value)
        
        # If browser notifications are disabled, disable all browser notification types
        if hasattr(self, 'browser_enabled') and not self.browser_enabled:
            self.browser_case_updates = False
            self.browser_document_updates = False
            self.browser_appointment_reminders = False
            self.browser_messages = False
            self.browser_legal_ai_responses = False
            self.browser_system_announcements = False

    def save_to_cache(self):
        """Save preferences to cache"""
        cache = get_cache_service()
        return cache.set(self.cache_key, self.to_dict(), expire_seconds=3600)

    def invalidate_cache(self):
        """Remove preferences from cache"""
        cache = get_cache_service()
        return cache.delete(self.cache_key)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get preferences for a user ID"""
        # Try to get from cache first
        cache = get_cache_service()
        cache_key = f"notification_preferences:{user_id}"
        cached_prefs = cache.get(cache_key)
        
        if cached_prefs:
            # Create instance from cached data
            prefs = cls(user_id)
            for category, settings in cached_prefs.items():
                if isinstance(settings, dict):
                    for key, value in settings.items():
                        attr_name = f"{category.lower()}_{key.lower()}"
                        if hasattr(prefs, attr_name):
                            setattr(prefs, attr_name, value)
            return prefs
        
        # If not in cache, get from database
        prefs = cls.query.filter_by(user_id=user_id).first()
        if not prefs:
            # Create default preferences
            prefs = cls(user_id=user_id)
            db.session.add(prefs)
            db.session.commit()
        
        # Save to cache
        prefs.save_to_cache()
        return prefs
    
    @classmethod
    def update_preferences(cls, user_id, preferences_data):
        """Update preferences for a user"""
        prefs = cls.get_by_user_id(user_id)
        
        # Update email preferences
        if 'email' in preferences_data:
            email_prefs = preferences_data['email']
            if 'caseUpdates' in email_prefs:
                prefs.email_case_updates = email_prefs['caseUpdates']
            if 'documentUpdates' in email_prefs:
                prefs.email_document_updates = email_prefs['documentUpdates']
            if 'appointmentReminders' in email_prefs:
                prefs.email_appointment_reminders = email_prefs['appointmentReminders']
            if 'newMessages' in email_prefs:
                prefs.email_messages = email_prefs['newMessages']
            if 'legalAIResponses' in email_prefs:
                prefs.email_legal_ai_responses = email_prefs['legalAIResponses']
            if 'systemAnnouncements' in email_prefs:
                prefs.email_system_announcements = email_prefs['systemAnnouncements']
        
        # Update in-app preferences
        if 'inApp' in preferences_data:
            app_prefs = preferences_data['inApp']
            if 'caseUpdates' in app_prefs:
                prefs.app_case_updates = app_prefs['caseUpdates']
            if 'documentUpdates' in app_prefs:
                prefs.app_document_updates = app_prefs['documentUpdates']
            if 'appointmentReminders' in app_prefs:
                prefs.app_appointment_reminders = app_prefs['appointmentReminders']
            if 'newMessages' in app_prefs:
                prefs.app_messages = app_prefs['newMessages']
            if 'legalAIResponses' in app_prefs:
                prefs.app_legal_ai_responses = app_prefs['legalAIResponses']
            if 'systemAnnouncements' in app_prefs:
                prefs.app_system_announcements = app_prefs['systemAnnouncements']
        
        # Update browser preferences
        if 'browser' in preferences_data:
            browser_prefs = preferences_data['browser']
            if 'caseUpdates' in browser_prefs:
                prefs.browser_case_updates = browser_prefs['caseUpdates']
            if 'documentUpdates' in browser_prefs:
                prefs.browser_document_updates = browser_prefs['documentUpdates']
            if 'appointmentReminders' in browser_prefs:
                prefs.browser_appointment_reminders = browser_prefs['appointmentReminders']
            if 'newMessages' in browser_prefs:
                prefs.browser_messages = browser_prefs['newMessages']
            if 'legalAIResponses' in browser_prefs:
                prefs.browser_legal_ai_responses = browser_prefs['legalAIResponses']
            if 'systemAnnouncements' in browser_prefs:
                prefs.browser_system_announcements = browser_prefs['systemAnnouncements']
        
        # Save to database
        db.session.commit()
        
        # Update cache
        prefs.save_to_cache()
        
        return prefs 