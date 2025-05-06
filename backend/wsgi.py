"""
WSGI entry point for gunicorn to use
"""
import os
# Import app from the app module in the current directory
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002))) 