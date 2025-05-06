"""
WSGI entry point for gunicorn to use
"""
from app import app

if __name__ == "__main__":
    app.run() 