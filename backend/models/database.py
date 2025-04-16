from typing import Optional, TypeVar, Type, Any, cast
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, Session, declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String, Integer, DateTime, Text, Boolean
import os

T = TypeVar('T')

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Add type hints for common column types
Column = db.Column
String = db.String
Integer = db.Integer
DateTime = db.DateTime
Text = db.Text
Boolean = db.Boolean
ForeignKey = db.ForeignKey
relationship = db.relationship
backref = db.backref

class DatabaseConfig:
    """Database configuration and session management."""
    
    @staticmethod
    def init_app(app: Flask) -> None:
        """Initialize database with Flask application."""
        # Configure SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize SQLAlchemy with app
        db.init_app(app)
        
        # Create all tables
        with app.app_context():
            # Import models here to ensure they are registered with SQLAlchemy
            from models.user import User
            from models.case import Case
            from models.document import Document
            from models.notification import Notification
            from models.rights import Rights
            from models.user_notification_preferences import UserNotificationPreferences
            from models.attorney_request import AttorneyRequest
            from models.case_timeline import CaseTimelineEvent
            from models.case_next_step import CaseNextStep
            from models.case_document import CaseDocument
            from models.queue_models import QueueCase, QueueHistory
            
            db.create_all()
            print("Database initialized successfully")

    @staticmethod
    def get_session() -> Session:
        """Get the current database session."""
        return cast(Session, db.session)

    @staticmethod
    def commit_session() -> None:
        """Commit the current session."""
        session = cast(Session, db.session)
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def close_session() -> None:
        """Close the current session."""
        session = cast(Session, db.session)
        session.close()

class BaseModel(db.Model):  # type: ignore
    """Abstract base model with common functionality."""
    __abstract__ = True

    @classmethod
    def get_by_id(cls: Type[T], id: str) -> Optional[T]:
        """Get a record by ID."""
        return cls.query.get(id)  # type: ignore

    @classmethod
    def create(cls: Type[T], **kwargs: Any) -> T:
        """Create a new record."""
        instance = cls(**kwargs)
        session = cast(Session, db.session)
        session.add(instance)
        session.commit()
        return instance

    def update(self, **kwargs: Any) -> None:
        """Update the current record."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session = cast(Session, db.session)
        session.commit()

    def delete(self) -> None:
        """Delete the current record."""
        session = cast(Session, db.session)
        session.delete(self)
        session.commit()

    def save(self) -> None:
        """Save the current record."""
        session = cast(Session, db.session)
        session.add(self)
        session.commit() 