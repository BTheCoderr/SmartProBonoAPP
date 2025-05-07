"""Initialize the database"""
from app import db, app

def init_db():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!") 