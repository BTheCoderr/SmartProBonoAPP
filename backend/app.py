"""Main Flask application."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend import create_app
from backend.database import init_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = create_app()

# Initialize database
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    logger.info("Starting application in development mode")
    app.run(host='0.0.0.0', port=3001, debug=True) 