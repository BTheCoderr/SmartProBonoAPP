from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.database import db
from routes.auth import token_required
from datetime import datetime, timedelta
from sqlalchemy import func
import json
import os
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = args[0]
        if not hasattr(current_user, 'role') or current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@admin_required
def get_dashboard(current_user):
    """Get admin dashboard statistics"""
    try:
        # Get user statistics
        total_users = User.query.count()
        total_attorneys = User.query.filter_by(role='attorney').count()
        total_clients = User.query.filter_by(role='client').count()
        verified_users = User.query.filter_by(is_verified=True).count()
        
        # Get recent users
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        
        # Get system statistics
        system_stats = {
            'cpu_usage': os.getloadavg()[0],  # 1-minute load average
            'memory_usage': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'),
            'disk_usage': os.statvfs('/').f_blocks * os.statvfs('/').f_frsize,
            'disk_free': os.statvfs('/').f_bfree * os.statvfs('/').f_frsize
        }
        
        return jsonify({
            'user_stats': {
                'total_users': total_users,
                'total_attorneys': total_attorneys,
                'total_clients': total_clients,
                'verified_users': verified_users,
                'verification_rate': (verified_users / total_users * 100) if total_users > 0 else 0
            },
            'recent_users': [user.to_dict() for user in recent_users],
            'system_stats': system_stats
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting dashboard data: {str(e)}")
        return jsonify({'error': 'Could not fetch dashboard data'}), 500

@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users(current_user):
    """Get all users with filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role')
        verified = request.args.get('verified', type=bool)
        search = request.args.get('search')
        
        # Build query
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
        if verified is not None:
            query = query.filter_by(is_verified=verified)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (User.email.like(search_term)) |
                (User.first_name.like(search_term)) |
                (User.last_name.like(search_term))
            )
        
        # Execute query with pagination
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting users: {str(e)}")
        return jsonify({'error': 'Could not fetch users'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
@admin_required
def get_user(current_user, user_id):
    """Get detailed user information"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify(user.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Error getting user {user_id}: {str(e)}")
        return jsonify({'error': 'Could not fetch user'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(current_user, user_id):
    """Update user information"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Don't allow updating certain fields
        forbidden_fields = ['id', 'password_hash', 'created_at']
        for field in forbidden_fields:
            data.pop(field, None)
            
        # Update user fields
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
                
        db.session.commit()
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating user {user_id}: {str(e)}")
        return jsonify({'error': 'Could not update user'}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, user_id):
    """Delete a user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({'error': 'Could not delete user'}), 500

@admin_bp.route('/logs', methods=['GET'])
@token_required
@admin_required
def get_logs(current_user):
    """Get system logs"""
    try:
        log_type = request.args.get('type', 'error')  # error, access, or all
        days = request.args.get('days', 7, type=int)
        
        # For MVP, return dummy logs
        dummy_logs = [
            {
                'timestamp': (datetime.utcnow() - timedelta(hours=i)).isoformat(),
                'level': 'ERROR' if i % 3 == 0 else 'INFO',
                'message': f'Sample log message {i}',
                'source': 'system'
            }
            for i in range(50)
        ]
        
        return jsonify({
            'logs': dummy_logs
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting logs: {str(e)}")
        return jsonify({'error': 'Could not fetch logs'}), 500

@admin_bp.route('/system/health', methods=['GET'])
@token_required
@admin_required
def get_system_health(current_user):
    """Get system health information"""
    try:
        # Get basic system information
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': os.popen('uptime').read().strip(),
            'system': {
                'cpu_usage': os.getloadavg(),
                'memory_total': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'),
                'memory_available': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES'),
                'disk_usage': {
                    'total': os.statvfs('/').f_blocks * os.statvfs('/').f_frsize,
                    'free': os.statvfs('/').f_bfree * os.statvfs('/').f_frsize
                }
            },
            'database': {
                'status': 'connected',
                'total_users': User.query.count(),
                'total_attorneys': User.query.filter_by(role='attorney').count(),
                'total_clients': User.query.filter_by(role='client').count()
            }
        }
        
        return jsonify(health_data)
        
    except Exception as e:
        current_app.logger.error(f"Error getting system health: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500 