"""Flask extensions module."""
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

# Initialize extensions
db = SQLAlchemy()
mongo = PyMongo()
mail = Mail()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")

def init_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    mongo.init_app(app) 