from flask import Blueprint, jsonify, request, g
from services.priority_queue_service import priority_queue_service, QueuedCase
from utils.auth import require_permission, require_role
from services.audit_trail import audit_trail_service
import time
from typing import Dict, Any, Optional

# Rate limiting settings
REQUEST_LIMIT = 60  # Number of requests
RATE_LIMIT_WINDOW = 60  # Seconds
request_counter = {}

def rate_limit(user_id: str) -> bool:
    """Basic rate limiting implementation"""
    current_time = time.time()
    
    # Initialize or clean up expired entries
    if user_id not in request_counter:
        request_counter[user_id] = {'count': 0, 'start_time': current_time}
    elif current_time - request_counter[user_id]['start_time'] > RATE_LIMIT_WINDOW:
        request_counter[user_id] = {'count': 0, 'start_time': current_time}
        
    # Increment request count
    request_counter[user_id]['count'] += 1
    
    # Check if rate limit exceeded
    if request_counter[user_id]['count'] > REQUEST_LIMIT:
        return True
        
    return False

priority_queue_bp = Blueprint('priority_queue', __name__)

def serialize_case(case: QueuedCase) -> Dict[str, Any]:
    """Serialize a QueuedCase instance to a dictionary."""
    return {
        'case_id': case.case_id,
        'priority': case.priority.name if hasattr(case.priority, 'name') else str(case.priority),
        'user_id': case.user_id,
        'situation_type': case.situation_type,
        'timestamp': case.timestamp.isoformat() if hasattr(case, 'timestamp') else None,
        'assigned_lawyer_id': case.assigned_lawyer_id if hasattr(case, 'assigned_lawyer_id') else None
    }

@priority_queue_bp.route('/api/priority-queue/case', methods=['POST'])
@require_permission('manage_queue')
def add_case():
    """Add a new case to the priority queue"""
    try:
        # Apply rate limiting
        user_id = g.user.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID not found'}), 401
            
        if rate_limit(user_id):
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        required_fields = ['case_id', 'priority', 'user_id', 'situation_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
            
        case = priority_queue_service.add_case(
            case_id=str(data['case_id']),
            priority=str(data['priority']),
            user_id=str(data['user_id']),
            situation_type=str(data['situation_type']),
            metadata=data.get('metadata', {})
        )
        
        # Get estimated wait time
        wait_time = priority_queue_service.get_estimated_wait_time(case.case_id)
        position = priority_queue_service.get_queue_position(case.case_id)
        
        # Log audit event
        audit_trail_service.log_event(
            entity_id=case.case_id,
            event_type='case_added_to_queue',
            user_id=user_id,
            details={
                'priority': data['priority'],
                'situation_type': data['situation_type']
            }
        )
        
        return jsonify({
            'case': serialize_case(case),
            'estimated_wait': wait_time,
            'queue_position': position
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@priority_queue_bp.route('/api/priority-queue/case/<case_id>', methods=['PUT'])
@require_permission('manage_queue')
def update_case_priority(case_id: str):
    """Update case priority in queue"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        if 'priority' not in data:
            return jsonify({'error': 'New priority level is required'}), 400
            
        # Get old priority for audit
        case_info = priority_queue_service.get_case(case_id)
        if not case_info:
            return jsonify({'error': 'Case not found'}), 404
            
        old_priority = case_info.priority.name if case_info.priority else 'unknown'
            
        case = priority_queue_service.update_priority(case_id, str(data['priority']))
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Log audit event
        audit_trail_service.log_event(
            entity_id=case_id,
            event_type='case_priority_updated',
            user_id=g.user.get('user_id', ''),
            details={
                'old_priority': old_priority,
                'new_priority': data['priority']
            }
        )
        
        return jsonify(serialize_case(case)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@priority_queue_bp.route('/api/priority-queue/case/<case_id>/assign', methods=['POST'])
@require_role('lawyer', 'admin', 'superadmin')
def assign_case(case_id: str):
    """Assign a case to a lawyer"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        if 'lawyer_id' not in data:
            return jsonify({'error': 'Lawyer ID is required'}), 400
            
        case = priority_queue_service.assign_case(case_id, str(data['lawyer_id']))
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        # Log audit event
        audit_trail_service.log_event(
            entity_id=case_id,
            event_type='case_assigned',
            user_id=g.user.get('user_id', ''),
            details={
                'lawyer_id': data['lawyer_id']
            }
        )
        
        return jsonify(serialize_case(case)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@priority_queue_bp.route('/api/priority-queue/case/<case_id>/status', methods=['GET'])
@require_permission('view_queue')
def get_case_status(case_id):
    """Get the current status of a case in the queue"""
    try:
        # Apply rate limiting
        if rate_limit(g.user.get('user_id')):
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        position = priority_queue_service.get_queue_position(case_id)
        if position is None:
            return jsonify({'error': 'Case not found'}), 404
            
        wait_time = priority_queue_service.get_estimated_wait_time(case_id)
        
        # Log view event (lower detail level for read operations)
        audit_trail_service.log_event(
            entity_id=case_id,
            event_type='case_status_viewed',
            user_id=g.user.get('user_id'),
            details={}
        )
        
        return jsonify({
            'case_id': case_id,
            'queue_position': position,
            'estimated_wait_time': str(wait_time) if wait_time else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@priority_queue_bp.route('/api/priority-queue/status', methods=['GET'])
@require_permission('view_queue')
def get_queue_status():
    """Get the current status of the entire queue"""
    try:
        # Apply rate limiting
        if rate_limit(g.user.get('user_id')):
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        status = priority_queue_service.get_queue_status()
        
        # Log view event
        audit_trail_service.log_event(
            entity_id='queue',
            event_type='queue_status_viewed',
            user_id=g.user.get('user_id'),
            details={}
        )
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New endpoint for queue analytics
@priority_queue_bp.route('/api/priority-queue/analytics', methods=['GET'])
@require_permission('admin_actions')
def get_queue_analytics():
    """Get queue performance analytics"""
    try:
        # Apply rate limiting
        if rate_limit(g.user.get('user_id')):
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        analytics = priority_queue_service.get_queue_analytics()
        
        # Log analytics access
        audit_trail_service.log_event(
            entity_id='queue',
            event_type='queue_analytics_accessed',
            user_id=g.user.get('user_id'),
            details={}
        )
        
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New endpoint for queue history and audit logs
@priority_queue_bp.route('/api/priority-queue/audit', methods=['GET'])
@require_permission('admin_actions')
def get_queue_audit_log():
    """Get queue audit logs"""
    try:
        # Apply rate limiting
        if rate_limit(g.user.get('user_id')):
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        # Get audit logs for the queue
        audit_logs = audit_trail_service.get_audit_trail('queue')
        
        # Log audit trail access
        audit_trail_service.log_event(
            entity_id='queue',
            event_type='queue_audit_logs_accessed',
            user_id=g.user.get('user_id'),
            details={}
        )
        
        return jsonify(audit_logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 