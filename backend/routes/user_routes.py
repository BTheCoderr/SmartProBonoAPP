from flask import Blueprint, jsonify, request
from services.user_service import UserService
from utils.auth import require_auth

user_bp = Blueprint('user_routes', __name__)
user_service = UserService()

@user_bp.route('/api/users/attorneys/available', methods=['GET'])
@require_auth
def get_available_attorneys():
    """Get list of available attorneys for case assignment"""
    try:
        filters = {
            'role': 'volunteer_attorney',
            'availability': request.args.get('availability'),
            'specialties': request.args.getlist('specialties')
        }
        attorneys = user_service.get_available_attorneys(filters)
        return jsonify(attorneys), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>/availability', methods=['PUT'])
@require_auth
def update_user_availability(user_id):
    """Update user availability settings"""
    try:
        data = request.get_json()
        updated_user = user_service.update_availability(user_id, data)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>/profile', methods=['GET'])
@require_auth
def get_user_profile(user_id):
    """Get user profile details"""
    try:
        user = user_service.get_user_by_id(user_id)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>/profile', methods=['PUT'])
@require_auth
def update_user_profile(user_id):
    """Update user profile details"""
    try:
        data = request.get_json()
        updated_user = user_service.update_profile(user_id, data)
        return jsonify(updated_user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500