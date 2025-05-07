"""Flask extensions initialization"""
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

# Initialize extensions
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
socketio = SocketIO()
jwt = JWTManager()
mongo = PyMongo()

def init_extensions(app):
    """Initialize Flask extensions"""
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    jwt.init_app(app)
    mongo.init_app(app) 