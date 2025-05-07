"""Health check endpoints for the application."""
from flask import Blueprint, jsonify, current_app
from database.mongo import MongoManager
from extensions import db
import logging

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Comprehensive health check endpoint that checks all critical services
    """
    health_status = {
        'status': 'healthy',
        'services': {
            'api': 'healthy',
            'postgresql': 'unknown',
            'mongodb': 'unknown'
        },
        'details': {}
    }

    # Check PostgreSQL connection
    try:
        db.session.execute('SELECT 1')
        health_status['services']['postgresql'] = 'healthy'
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {str(e)}")
        health_status['services']['postgresql'] = 'unhealthy'
        health_status['details']['postgresql_error'] = str(e)
        health_status['status'] = 'degraded'

    # Check MongoDB connection
    mongo_manager = MongoManager()
    try:
        if mongo_manager.is_connected():
            health_status['services']['mongodb'] = 'healthy'
        else:
            health_status['services']['mongodb'] = 'unhealthy'
            health_status['details']['mongodb_error'] = 'Connection test failed'
            health_status['status'] = 'degraded'
    except Exception as e:
        logger.error(f"MongoDB health check failed: {str(e)}")
        health_status['services']['mongodb'] = 'unhealthy'
        health_status['details']['mongodb_error'] = str(e)
        health_status['status'] = 'degraded'

    # Set response status code based on health status
    status_code = 200 if health_status['status'] == 'healthy' else 503

    return jsonify(health_status), status_code

@health_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for basic connectivity check"""
    return jsonify({
        'status': 'ok',
        'message': 'pong'
    }) 