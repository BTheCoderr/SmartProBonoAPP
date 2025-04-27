#!/usr/bin/env python
"""
Simple script to initialize the database migrations.
This avoids issues with loading the full app during initial setup.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

# Always use SQLite for migrations setup
DB_URI = 'sqlite:///smartprobono.db'

# Create a minimal app just for migrations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models to ensure they're registered with SQLAlchemy
from models.user import User
from models.case import Case
from models.document import Document
from backend.models.rights import Rights

if __name__ == '__main__':
    print("Migration environment initialized.")
    print(f"Using database: {DB_URI}")
    print("Run these commands:")
    print("  flask db init    - Initialize migrations folder")
    print("  flask db migrate - Create migration based on models")
    print("  flask db upgrade - Apply migrations to database") 