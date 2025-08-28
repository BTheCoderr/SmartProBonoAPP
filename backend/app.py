"""Main Flask application."""
from backend import create_app
from database import init_db
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
    app.run(host='0.0.0.0', port=5000, debug=True) 