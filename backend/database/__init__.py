"""Database package initialization."""
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