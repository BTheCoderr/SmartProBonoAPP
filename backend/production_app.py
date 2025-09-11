"""Production Flask application for Render deployment."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)
CORS(app, origins=['*'])  # Allow all origins for production

# Set production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///production.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and register routes
try:
    from backend.routes.unified_api import bp as unified_api_bp
    app.register_blueprint(unified_api_bp)
    logger.info("✅ Unified API routes registered")
except ImportError as e:
    logger.warning(f"⚠️ Unified API routes not available: {e}")

try:
    from backend.routes.legal_ai import bp as legal_ai_bp
    app.register_blueprint(legal_ai_bp, url_prefix='/api/legal')
    logger.info("✅ Legal AI routes registered")
except ImportError as e:
    logger.warning(f"⚠️ Legal AI routes not available: {e}")

try:
    from backend.routes.virtual_paralegal_crm import bp as virtual_paralegal_crm_bp
    app.register_blueprint(virtual_paralegal_crm_bp)
    logger.info("✅ Virtual Paralegal CRM routes registered")
except ImportError as e:
    logger.warning(f"⚠️ Virtual Paralegal CRM routes not available: {e}")

try:
    from backend.routes.ai_virtual_paralegal import bp as ai_virtual_paralegal_bp
    app.register_blueprint(ai_virtual_paralegal_bp)
    logger.info("✅ AI Virtual Paralegal routes registered")
except ImportError as e:
    logger.warning(f"⚠️ AI Virtual Paralegal routes not available: {e}")

try:
    from backend.routes.crm_api import bp as crm_api_bp
    app.register_blueprint(crm_api_bp)
    logger.info("✅ CRM API routes registered")
except ImportError as e:
    logger.warning(f"⚠️ CRM API routes not available: {e}")

# Health check endpoint
@app.route('/api/v1/health')
def health():
    return {
        "status": "healthy",
        "service": "SmartProBono Backend",
        "version": "2.0.0"
    }

# Root endpoint
@app.route('/')
def root():
    return {
        "message": "SmartProBono Backend API",
        "version": "2.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "legal_analysis": "/api/v1/legal/analyze",
            "ai_virtual_paralegal": "/api/v1/ai-virtual-paralegal/dashboard"
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
