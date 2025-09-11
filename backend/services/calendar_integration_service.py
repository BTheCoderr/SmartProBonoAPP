"""
Calendar Integration Service for SmartProBono
Handles Google Calendar integration for court dates and appointments.
"""
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app, session, redirect, request
from backend.database import db
from backend.models import CourtDate, User, Case
import logging
import json

logger = logging.getLogger(__name__)

class CalendarIntegrationService:
    """Service for integrating with Google Calendar."""
    
    def __init__(self):
        self.client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        self.client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = current_app.config.get('GOOGLE_REDIRECT_URI')
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        
        # Google Calendar API service
        self.service = None
    
    def get_authorization_url(self, user_id: int):
        """Get Google Calendar authorization URL."""
        try:
            if not self.client_id or not self.client_secret:
                raise ValueError("Google Calendar not configured")
            
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=str(user_id)
            )
            
            return authorization_url
            
        except Exception as e:
            logger.error(f"Error getting authorization URL: {e}")
            return None
    
    def handle_authorization_callback(self, authorization_response: str, state: str):
        """Handle Google Calendar authorization callback."""
        try:
            if not self.client_id or not self.client_secret:
                raise ValueError("Google Calendar not configured")
            
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Exchange authorization code for credentials
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            
            # Store credentials for user
            user_id = int(state)
            self._store_user_credentials(user_id, credentials)
            
            # Initialize service
            self.service = build('calendar', 'v3', credentials=credentials)
            
            return True
            
        except Exception as e:
            logger.error(f"Error handling authorization callback: {e}")
            return False
    
    def _store_user_credentials(self, user_id: int, credentials: Credentials):
        """Store user's Google Calendar credentials."""
        try:
            user = User.query.get(user_id)
            if not user:
                return False
            
            # Store credentials in user metadata
            user_metadata = user.metadata or {}
            user_metadata['google_calendar_credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            user.metadata = user_metadata
            db.session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing user credentials: {e}")
            return False
    
    def _get_user_credentials(self, user_id: int):
        """Get user's Google Calendar credentials."""
        try:
            user = User.query.get(user_id)
            if not user or not user.metadata:
                return None
            
            creds_data = user.metadata.get('google_calendar_credentials')
            if not creds_data:
                return None
            
            credentials = Credentials(
                token=creds_data['token'],
                refresh_token=creds_data['refresh_token'],
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error getting user credentials: {e}")
            return None
    
    def _get_service(self, user_id: int):
        """Get Google Calendar service for user."""
        try:
            credentials = self._get_user_credentials(user_id)
            if not credentials:
                return None
            
            service = build('calendar', 'v3', credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Error getting Google Calendar service: {e}")
            return None
    
    def create_calendar_event(self, court_date_id: int, user_id: int):
        """Create a Google Calendar event for a court date."""
        try:
            service = self._get_service(user_id)
            if not service:
                return {'success': False, 'error': 'Google Calendar not connected'}
            
            court_date = CourtDate.query.get(court_date_id)
            if not court_date:
                return {'success': False, 'error': 'Court date not found'}
            
            # Create event
            event = {
                'summary': court_date.title,
                'description': court_date.description or f"Court date for case {court_date.case_id}",
                'location': court_date.court_location,
                'start': {
                    'dateTime': court_date.scheduled_date.isoformat(),
                    'timeZone': 'America/New_York',  # Default timezone
                },
                'end': {
                    'dateTime': (court_date.scheduled_date + timedelta(minutes=court_date.duration_minutes)).isoformat(),
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
                'extendedProperties': {
                    'private': {
                        'court_date_id': str(court_date_id),
                        'case_id': str(court_date.case_id) if court_date.case_id else '',
                        'bond_id': str(court_date.bond_id) if court_date.bond_id else '',
                    }
                }
            }
            
            # Add court room if available
            if court_date.court_room:
                event['location'] += f", Room {court_date.court_room}"
            
            # Create the event
            created_event = service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            # Store Google Calendar event ID
            court_date.metadata = court_date.metadata or {}
            court_date.metadata['google_calendar_event_id'] = created_event['id']
            db.session.commit()
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_url': created_event.get('htmlLink')
            }
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return {'success': False, 'error': f'Google Calendar API error: {e}'}
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_calendar_event(self, court_date_id: int, user_id: int):
        """Update a Google Calendar event for a court date."""
        try:
            service = self._get_service(user_id)
            if not service:
                return {'success': False, 'error': 'Google Calendar not connected'}
            
            court_date = CourtDate.query.get(court_date_id)
            if not court_date:
                return {'success': False, 'error': 'Court date not found'}
            
            event_id = court_date.metadata.get('google_calendar_event_id') if court_date.metadata else None
            if not event_id:
                return {'success': False, 'error': 'Event not found in Google Calendar'}
            
            # Update event
            event = {
                'summary': court_date.title,
                'description': court_date.description or f"Court date for case {court_date.case_id}",
                'location': court_date.court_location,
                'start': {
                    'dateTime': court_date.scheduled_date.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': (court_date.scheduled_date + timedelta(minutes=court_date.duration_minutes)).isoformat(),
                    'timeZone': 'America/New_York',
                },
            }
            
            # Add court room if available
            if court_date.court_room:
                event['location'] += f", Room {court_date.court_room}"
            
            # Update the event
            updated_event = service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()
            
            return {
                'success': True,
                'event_id': updated_event['id'],
                'event_url': updated_event.get('htmlLink')
            }
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return {'success': False, 'error': f'Google Calendar API error: {e}'}
        except Exception as e:
            logger.error(f"Error updating calendar event: {e}")
            return {'success': False, 'error': str(e)}
    
    def delete_calendar_event(self, court_date_id: int, user_id: int):
        """Delete a Google Calendar event for a court date."""
        try:
            service = self._get_service(user_id)
            if not service:
                return {'success': False, 'error': 'Google Calendar not connected'}
            
            court_date = CourtDate.query.get(court_date_id)
            if not court_date:
                return {'success': False, 'error': 'Court date not found'}
            
            event_id = court_date.metadata.get('google_calendar_event_id') if court_date.metadata else None
            if not event_id:
                return {'success': False, 'error': 'Event not found in Google Calendar'}
            
            # Delete the event
            service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            
            # Remove Google Calendar event ID from metadata
            if court_date.metadata:
                court_date.metadata.pop('google_calendar_event_id', None)
                db.session.commit()
            
            return {'success': True}
            
        except HttpError as e:
            if e.resp.status == 410:  # Event already deleted
                return {'success': True}
            logger.error(f"Google Calendar API error: {e}")
            return {'success': False, 'error': f'Google Calendar API error: {e}'}
        except Exception as e:
            logger.error(f"Error deleting calendar event: {e}")
            return {'success': False, 'error': str(e)}
    
    def sync_court_dates_to_calendar(self, user_id: int, case_id: int = None):
        """Sync all court dates to Google Calendar."""
        try:
            service = self._get_service(user_id)
            if not service:
                return {'success': False, 'error': 'Google Calendar not connected'}
            
            # Get court dates
            query = CourtDate.query.filter_by(client_id=user_id)
            if case_id:
                query = query.filter_by(case_id=case_id)
            
            court_dates = query.all()
            
            synced_count = 0
            errors = []
            
            for court_date in court_dates:
                result = self.create_calendar_event(court_date.id, user_id)
                if result['success']:
                    synced_count += 1
                else:
                    errors.append(f"Court date {court_date.id}: {result['error']}")
            
            return {
                'success': True,
                'synced_count': synced_count,
                'total_count': len(court_dates),
                'errors': errors
            }
            
        except Exception as e:
            logger.error(f"Error syncing court dates to calendar: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_calendar_events(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        """Get Google Calendar events for a user."""
        try:
            service = self._get_service(user_id)
            if not service:
                return {'success': False, 'error': 'Google Calendar not connected'}
            
            # Set default date range
            if not start_date:
                start_date = datetime.utcnow()
            if not end_date:
                end_date = start_date + timedelta(days=30)
            
            # Get events
            events_result = service.events().list(
                calendarId='primary',
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            return {
                'success': True,
                'events': events
            }
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            return {'success': False, 'error': f'Google Calendar API error: {e}'}
        except Exception as e:
            logger.error(f"Error getting calendar events: {e}")
            return {'success': False, 'error': str(e)}
    
    def is_connected(self, user_id: int):
        """Check if user has Google Calendar connected."""
        try:
            credentials = self._get_user_credentials(user_id)
            if not credentials:
                return False
            
            # Test the credentials
            service = build('calendar', 'v3', credentials=credentials)
            service.calendarList().list().execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking Google Calendar connection: {e}")
            return False
    
    def disconnect(self, user_id: int):
        """Disconnect user's Google Calendar."""
        try:
            user = User.query.get(user_id)
            if not user or not user.metadata:
                return {'success': False, 'error': 'No connection found'}
            
            # Remove credentials
            user.metadata.pop('google_calendar_credentials', None)
            db.session.commit()
            
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Error disconnecting Google Calendar: {e}")
            return {'success': False, 'error': str(e)}

# Create singleton instance
calendar_integration_service = CalendarIntegrationService()
