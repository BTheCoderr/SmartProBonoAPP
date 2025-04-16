from flask import Blueprint, jsonify, request
from services.availability_service import availability_service
from utils.auth import require_auth

availability_routes = Blueprint('availability_routes', __name__)

@availability_routes.route('/api/availability/status', methods=['GET'])
@require_auth
def get_user_status():
    """Get current user's availability status"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        status = availability_service.get_status(user_id)
        if not status:
            return jsonify({'error': 'Status not found'}), 404
            
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@availability_routes.route('/api/availability/status', methods=['PUT'])
@require_auth
def update_user_status():
    """Update user's availability status"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        status = data.get('status')
        expires_in = data.get('expires_in')
        
        if not user_id or not status:
            return jsonify({'error': 'User ID and status are required'}), 400
            
        updated_status = availability_service.update_status(user_id, status, expires_in)
        return jsonify(updated_status), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@availability_routes.route('/api/availability/schedule', methods=['GET'])
@require_auth
def get_user_schedule():
    """Get user's availability schedule"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        schedule = availability_service.get_schedule(user_id)
        if not schedule:
            return jsonify({'error': 'Schedule not found'}), 404
            
        return jsonify(schedule), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@availability_routes.route('/api/availability/schedule', methods=['PUT'])
@require_auth
def update_user_schedule():
    """Update user's availability schedule"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        schedule = data.get('schedule')
        
        if not user_id or not schedule:
            return jsonify({'error': 'User ID and schedule are required'}), 400
            
        updated_schedule = availability_service.update_schedule(user_id, schedule)
        return jsonify(updated_schedule), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@availability_routes.route('/api/availability/lawyers', methods=['GET'])
@require_auth
def get_available_lawyers():
    """Get list of available lawyers"""
    try:
        specialty = request.args.get('specialty')
        lawyers = availability_service.get_available_lawyers(specialty)
        return jsonify(lawyers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@availability_routes.route('/api/availability/next-slot', methods=['GET'])
@require_auth
def get_next_available_slot():
    """Get next available time slot for a lawyer"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        next_slot = availability_service.get_next_available_slot(user_id)
        if not next_slot:
            return jsonify({'error': 'No available slots found'}), 404
            
        return jsonify({'next_available_slot': next_slot.isoformat()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 