"""
Database package initialization.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_migrate import Migrate

# Initialize database objects
db = SQLAlchemy()
mongo = PyMongo()
migrate = Migrate()

def init_db(app):
    """Initialize database connections."""
    db.init_app(app)
    mongo.init_app(app)
    migrate.init_app(app, db)

# Import models at the bottom to avoid circular imports
# This is commented out to avoid errors during development
# from ..models import User, Document, Notification, Case, Form, Template
