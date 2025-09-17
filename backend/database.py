import os
from dotenv import load_dotenv
from .extensions import db, migrate

# Load environment variables
load_dotenv()

def init_db(app):
    """Initialize database with the Flask app"""
    # Check if database is already initialized
    if hasattr(app, 'extensions') and 'sqlalchemy' in app.extensions:
        app.logger.info("Database already initialized, skipping...")
        return
    
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
    
    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db) 