"""Simplified Flask extensions initialization"""
from flask_cors import CORS

# Initialize only essential extensions
cors = CORS()

def init_extensions(app):
    """Initialize only essential Flask extensions"""
    cors.init_app(app)
