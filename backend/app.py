"""Flask application entry point"""
import os
import sys
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from extensions import init_extensions, db, socketio
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
import redis
from datetime import datetime

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize Redis with proper error handling
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    try:
        redis_client = redis.from_url(redis_url)
        redis_client.ping()  # Test connection
        app.redis = redis_client
        logger.info("Redis connection established successfully")
    except redis.ConnectionError as e:
        logger.warning(f"Redis connection failed: {str(e)}. Using in-memory storage for rate limiting.")
        redis_client = None
    
    # Initialize rate limiter with Redis storage if available
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=redis_url if redis_client else None
    )
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)
    
    # Initialize middleware
    from middleware import init_middleware
    init_middleware(app)
    
    # Add health check endpoints
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Check Redis connection
            redis_status = "healthy" if redis_client and redis_client.ping() else "unhealthy"
            
            # Check database connection
            db_status = "healthy"
            try:
                db.session.execute("SELECT 1")
            except Exception as e:
                logger.error(f"Database health check failed: {str(e)}")
                db_status = "unhealthy"
            
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "services": {
                    "redis": redis_status,
                    "database": db_status
                }
            })
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500
    
    # Add rate limiting monitoring endpoint
    @app.route('/rate-limit-status')
    def rate_limit_status():
        """Rate limiting status endpoint"""
        try:
            if redis_client:
                return jsonify({
                    "status": "healthy",
                    "storage": "redis",
                    "limits": limiter.limits
                })
            return jsonify({
                "status": "healthy",
                "storage": "memory",
                "limits": limiter.limits
            })
        except Exception as e:
            logger.error(f"Rate limit status check failed: {str(e)}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500
    
    return app

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app('development')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    logger.info(f"Starting application on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True)


