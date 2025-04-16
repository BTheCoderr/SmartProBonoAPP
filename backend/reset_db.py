import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_app import create_app, db

def reset_database():
    """
    Reset the database - drop all tables and recreate them.
    WARNING: This will delete all data!
    """
    app = create_app()
    
    with app.app_context():
        logger.info("Dropping all tables...")
        db.drop_all()
        
        logger.info("Creating all tables...")
        db.create_all()
        
        logger.info("Database reset complete!")

if __name__ == "__main__":
    reset_database() 