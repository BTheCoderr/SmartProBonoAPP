"""
Admin routes for user management in SmartProBono - Simplified version
"""
from flask import Blueprint, jsonify

# Create blueprint
bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint that doesn't rely on any dependencies"""
    return jsonify({
        'status': 'ok',
        'message': 'Admin API is running',
        'version': '1.0.0'
    }), 200 