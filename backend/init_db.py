from app import create_app
from models.database import db, init_db
from seed_data import seed_demo_data

def init_database():
    app = create_app()
    # Initialize database with app parameter
    init_db(app)
    
    with app.app_context():
        # Seed demo data
        seed_demo_data()
        
        print("Database initialized and seeded with demo data!")

if __name__ == "__main__":
    init_database() 