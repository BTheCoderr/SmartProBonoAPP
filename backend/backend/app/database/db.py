from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from utils.logging_setup import get_logger

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize logger
logger = get_logger('database')

def init_db(app):
    """
    Initialize the database connection and migrations
    
    Args:
        app: Flask application instance
    """
    # Set default SQLite database if not provided
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        db_path = os.path.join(app.instance_path, 'smartprobono.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        
        # Ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)
    
    # Disable modification tracking for better performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy app
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Create the tables if they don't exist in development
    if app.config.get('ENV') == 'development':
        with app.app_context():
            # Import models to ensure they're registered with SQLAlchemy
            from models.user import User
            from models.notification import Notification, NotificationSettings
            
            try:
                db.create_all()
                logger.info("Database tables created successfully")
            except Exception as e:
                logger.error(f"Error creating database tables: {str(e)}")
    
    return db 