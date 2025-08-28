"""Database package initialization"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import urlparse
from .mongo import mongo

# Load environment variables
load_dotenv()

# Create database objects
db = SQLAlchemy()
migrate = Migrate()
mongo = PyMongo()

def init_db(app):
    """Initialize both PostgreSQL and MongoDB databases"""
    # Set PostgreSQL as default database
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            # Fallback to SQLite for development only
            app.logger.warning("No DATABASE_URL found. Using SQLite for development.")
            db_path = os.path.join(app.instance_path, 'smartprobono.db')
            db_url = f'sqlite:///{db_path}'
            os.makedirs(app.instance_path, exist_ok=True)
        
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    # Disable modification tracking for better performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    return db 