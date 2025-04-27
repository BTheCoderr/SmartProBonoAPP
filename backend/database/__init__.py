"""Database package initialization"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from .mongo import mongo

# Load environment variables
load_dotenv()

# Create database objects
db = SQLAlchemy()
migrate = Migrate()

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
    
    # Initialize MongoDB (optional)
    with app.app_context():
        try:
            mongo.init_client()
            app.logger.info("MongoDB initialized successfully")
        except Exception as e:
            app.logger.warning(f"Failed to initialize MongoDB: {str(e)}")
            app.logger.warning("Continuing without MongoDB support")

    return db 