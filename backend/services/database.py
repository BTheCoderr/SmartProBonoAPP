"""Database service for managing database operations"""
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from extensions import db

class Database:
    """Database service class"""
    
    @staticmethod
    def init_app(app):
        """Initialize database with app context"""
        db.init_app(app)
    
    @staticmethod
    def create_all():
        """Create all database tables"""
        db.create_all()
    
    @staticmethod
    def drop_all():
        """Drop all database tables"""
        db.drop_all()
    
    @staticmethod
    def session_commit():
        """Commit the current session"""
        try:
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database commit error: {str(e)}")
            return False
    
    @staticmethod
    def session_rollback():
        """Rollback the current session"""
        db.session.rollback()
    
    @staticmethod
    def session_remove():
        """Remove the current session"""
        db.session.remove()
    
    @staticmethod
    def session_add(obj):
        """Add an object to the current session"""
        db.session.add(obj)
    
    @staticmethod
    def session_delete(obj):
        """Delete an object from the current session"""
        db.session.delete(obj)
    
    @staticmethod
    def session_add_all(objects):
        """Add multiple objects to the current session"""
        db.session.add_all(objects)
    
    @staticmethod
    def session_execute(query):
        """Execute a raw SQL query"""
        try:
            return db.session.execute(query)
        except SQLAlchemyError as e:
            current_app.logger.error(f"Query execution error: {str(e)}")
            return None 