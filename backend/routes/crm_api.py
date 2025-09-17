"""
Comprehensive CRM API Routes
Provides complete API endpoints for Client Portal, Lawyer Dashboard, and Bondsman Dashboard.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging
from services.crm_service import crm_service
from services.auth_service import require_auth, get_current_user

bp = Blueprint('crm_api', __name__, url_prefix='/api/v1/crm')
logger = logging.getLogger(__name__)

# ==================== HEALTH CHECK ====================

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for CRM system"""
    try:
        return jsonify({
            'success': True,
            'message': 'CRM system is healthy',
            'status': 'operational',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'success': False,
            'message': 'CRM system health check failed',
            'error': str(e)
        }), 500

# ==================== CLIENT PORTAL API ====================

@bp.route('/client/intake', methods=['POST'])
def create_client_intake():
    """Create a new client intake."""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'legal_issue_type', 'case_description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        intake = crm_service.create_client_intake(data)
        
        return jsonify({
            'success': True,
            'intake': intake,
            'message': 'Intake submitted successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating client intake: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/client/<int:client_id>/cases', methods=['GET'])
@require_auth
def get_client_cases(client_id):
    """Get all cases for a specific client."""
    try:
        current_user = get_current_user()
        if current_user['id'] != client_id and current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        cases = crm_service.get_client_cases(client_id)
        
        return jsonify({
            'success': True,
            'cases': cases
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting client cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/client/<int:client_id>/documents', methods=['GET'])
@require_auth
def get_client_documents(client_id):
    """Get all documents for a specific client."""
    try:
        current_user = get_current_user()
        if current_user['id'] != client_id and current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        documents = crm_service.get_client_documents(client_id)
        
        return jsonify({
            'success': True,
            'documents': documents
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting client documents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/client/<int:client_id>/court-dates', methods=['GET'])
@require_auth
def get_client_court_dates(client_id):
    """Get all court dates for a specific client."""
    try:
        current_user = get_current_user()
        if current_user['id'] != client_id and current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        court_dates = crm_service.get_client_court_dates(client_id)
        
        return jsonify({
            'success': True,
            'court_dates': court_dates
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting client court dates: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/client/<int:client_id>/notifications', methods=['GET'])
@require_auth
def get_client_notifications(client_id):
    """Get all notifications for a specific client."""
    try:
        current_user = get_current_user()
        if current_user['id'] != client_id and current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        notifications = crm_service.get_client_notifications(client_id)
        
        return jsonify({
            'success': True,
            'notifications': notifications
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting client notifications: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== LAWYER DASHBOARD API ====================

@bp.route('/lawyer/clients', methods=['GET'])
@require_auth
def get_lawyer_clients():
    """Get all clients for a lawyer."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        clients = crm_service.get_all_clients(current_user['id'])
        
        return jsonify({
            'success': True,
            'clients': clients
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting lawyer clients: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/lawyer/cases', methods=['GET'])
@require_auth
def get_lawyer_cases():
    """Get all cases for a lawyer."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        cases = crm_service.get_lawyer_cases(current_user['id'])
        
        return jsonify({
            'success': True,
            'cases': cases
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting lawyer cases: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/lawyer/cases', methods=['POST'])
@require_auth
def create_lawyer_case():
    """Create a new case."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add lawyer ID to case data
        data['attorney_id'] = current_user['id']
        
        case = crm_service.create_case(data)
        
        return jsonify({
            'success': True,
            'case': case,
            'message': 'Case created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating case: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/lawyer/tasks', methods=['GET'])
@require_auth
def get_lawyer_tasks():
    """Get all tasks for a lawyer."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        tasks = crm_service.get_lawyer_tasks(current_user['id'])
        
        return jsonify({
            'success': True,
            'tasks': tasks
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting lawyer tasks: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/lawyer/tasks', methods=['POST'])
@require_auth
def create_lawyer_task():
    """Create a new task."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add assigned by to task data
        data['assigned_by'] = current_user['id']
        
        task = crm_service.create_task(data)
        
        return jsonify({
            'success': True,
            'task': task,
            'message': 'Task created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== BONDSMAN DASHBOARD API ====================

@bp.route('/bondsman/bonds', methods=['GET'])
@require_auth
def get_bondsman_bonds():
    """Get all bail bonds for a bondsman."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        bonds = crm_service.get_bondsman_bonds(current_user['id'])
        
        return jsonify({
            'success': True,
            'bonds': bonds
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting bondsman bonds: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/bondsman/bonds', methods=['POST'])
@require_auth
def create_bondsman_bond():
    """Create a new bail bond."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add bondsman ID to bond data
        data['bondsman_id'] = current_user['id']
        
        bond = crm_service.create_bail_bond(data)
        
        return jsonify({
            'success': True,
            'bond': bond,
            'message': 'Bail bond created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating bail bond: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/bondsman/payments', methods=['GET'])
@require_auth
def get_bondsman_payments():
    """Get all payments for a bondsman."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        payments = crm_service.get_bondsman_payments(current_user['id'])
        
        return jsonify({
            'success': True,
            'payments': payments
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting bondsman payments: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/bondsman/payments', methods=['POST'])
@require_auth
def create_bondsman_payment():
    """Create a new payment record."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        payment = crm_service.create_payment(data)
        
        return jsonify({
            'success': True,
            'payment': payment,
            'message': 'Payment recorded successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SHARED API ====================

@bp.route('/court-dates', methods=['POST'])
@require_auth
def create_court_date():
    """Create a new court date."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        court_date = crm_service.create_court_date(data)
        
        return jsonify({
            'success': True,
            'court_date': court_date,
            'message': 'Court date created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating court date: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/court-dates/upcoming', methods=['GET'])
@require_auth
def get_upcoming_court_dates():
    """Get upcoming court dates."""
    try:
        current_user = get_current_user()
        days_ahead = request.args.get('days', 30, type=int)
        
        court_dates = crm_service.get_upcoming_court_dates(days_ahead)
        
        return jsonify({
            'success': True,
            'court_dates': court_dates
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting upcoming court dates: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/notifications', methods=['POST'])
@require_auth
def create_notification():
    """Create a new notification."""
    try:
        current_user = get_current_user()
        if current_user['role'] not in ['lawyer', 'bondsman', 'admin']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        notification = crm_service.create_notification(data)
        
        return jsonify({
            'success': True,
            'notification': notification,
            'message': 'Notification created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@require_auth
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    try:
        current_user = get_current_user()
        
        success = crm_service.mark_notification_read(notification_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Notification marked as read'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Notification not found'
            }), 404
        
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/dashboard/analytics', methods=['GET'])
@require_auth
def get_dashboard_analytics():
    """Get dashboard analytics for the current user."""
    try:
        current_user = get_current_user()
        
        analytics = crm_service.get_dashboard_analytics(current_user['role'], current_user['id'])
        
        return jsonify({
            'success': True,
            'analytics': analytics
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
