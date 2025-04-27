"""
Migration to add email verification and session management fields to users table.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)

# Setup SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///smartprobono.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def upgrade():
    """
    Add email_verified and last_login columns to users table
    """
    with app.app_context():
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user ADD COLUMN email_verified BOOLEAN DEFAULT 0"))
            conn.execute(text("ALTER TABLE user ADD COLUMN last_login TIMESTAMP"))
            conn.commit()
        
        print("Migration completed: Added email_verified and last_login columns to users table.")

def downgrade():
    """
    Remove email_verified and last_login columns from users table
    """
    with app.app_context():
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE user DROP COLUMN email_verified"))
            conn.execute(text("ALTER TABLE user DROP COLUMN last_login"))
            conn.commit()
        
        print("Downgrade completed: Removed email_verified and last_login columns from users table.")

if __name__ == '__main__':
    upgrade() 