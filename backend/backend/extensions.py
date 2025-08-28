"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions
db = SQLAlchemy()
mongo = PyMongo()
mail = Mail()
socketio = SocketIO()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def init_extensions(app):
    """Initialize all Flask extensions."""
    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app) 