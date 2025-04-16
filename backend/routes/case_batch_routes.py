from flask import Blueprint, jsonify, request
from models.database import DatabaseConfig
from services.case_service import CaseService
from services.case_timeline_service import CaseTimelineService
from utils.auth import require_auth, require_role
from typing import Dict, List, Any, Optional, Union, Tuple

case_batch_bp = Blueprint('case_batch_routes', __name__)
case_service = CaseService()
timeline_service = CaseTimelineService()

@case_batch_bp.route('/api/cases/batch', methods=['PUT'])
@require_auth
def update_cases_batch():
    """Update multiple cases at once"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'case_ids' not in data or not data['case_ids']:
        return jsonify({'error': 'No case IDs provided'}), 400
    
    case_ids = data.pop('case_ids')
    
    # Extract user ID from request context or JWT
    user_id = data.pop('user_id', None) or request.user_id
    
    try:
        results = []
        for case_id in case_ids:
            try:
                case = case_service.update_case(case_id, data, user_id)
                if case:
                    results.append({
                        'case_id': case_id,
                        'status': 'success',
                        'data': case.to_dict()
                    })
                else:
                    results.append({
                        'case_id': case_id,
                        'status': 'error',
                        'message': 'Case not found'
                    })
            except Exception as e:
                results.append({
                    'case_id': case_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        return jsonify({
            'results': results,
            'summary': {
                'total': len(results),
                'success': success_count,
                'error': error_count
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_batch_bp.route('/api/cases/batch', methods=['DELETE'])
@require_auth
def delete_cases_batch():
    """Delete multiple cases at once"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'case_ids' not in data or not data['case_ids']:
        return jsonify({'error': 'No case IDs provided'}), 400
    
    case_ids = data['case_ids']
    
    try:
        results = []
        for case_id in case_ids:
            try:
                success = case_service.delete_case(case_id)
                if success:
                    results.append({
                        'case_id': case_id,
                        'status': 'success'
                    })
                else:
                    results.append({
                        'case_id': case_id,
                        'status': 'error',
                        'message': 'Case not found'
                    })
            except Exception as e:
                results.append({
                    'case_id': case_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        return jsonify({
            'results': results,
            'summary': {
                'total': len(results),
                'success': success_count,
                'error': error_count
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_batch_bp.route('/api/cases/batch/assign', methods=['POST'])
@require_auth
def assign_cases_batch():
    """Assign multiple cases to a user"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'case_ids' not in data or not data['case_ids']:
        return jsonify({'error': 'No case IDs provided'}), 400
    
    if 'user_id' not in data:
        return jsonify({'error': 'No user ID provided'}), 400
    
    case_ids = data['case_ids']
    user_id = data['user_id']
    
    try:
        results = []
        for case_id in case_ids:
            try:
                case = case_service.update_case(case_id, {'lawyer_id': user_id}, request.user_id)
                if case:
                    # Add a timeline event for the assignment
                    timeline_service.add_timeline_event(
                        case_id=case_id,
                        user_id=request.user_id,
                        event_type='assignment',
                        title=f'Case assigned to user {user_id}',
                        description=f'Case was assigned to a new user'
                    )
                    
                    results.append({
                        'case_id': case_id,
                        'status': 'success',
                        'data': case.to_dict()
                    })
                else:
                    results.append({
                        'case_id': case_id,
                        'status': 'error',
                        'message': 'Case not found'
                    })
            except Exception as e:
                results.append({
                    'case_id': case_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        return jsonify({
            'results': results,
            'summary': {
                'total': len(results),
                'success': success_count,
                'error': error_count
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_batch_bp.route('/api/cases/batch/priority', methods=['PUT'])
@require_auth
def update_priority_batch():
    """Update priority for multiple cases"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'case_ids' not in data or not data['case_ids']:
        return jsonify({'error': 'No case IDs provided'}), 400
    
    if 'priority' not in data:
        return jsonify({'error': 'No priority provided'}), 400
    
    case_ids = data['case_ids']
    priority = data['priority']
    
    try:
        results = []
        for case_id in case_ids:
            try:
                case = case_service.update_case(case_id, {'priority': priority}, request.user_id)
                if case:
                    # Add a timeline event for the priority change
                    timeline_service.add_timeline_event(
                        case_id=case_id,
                        user_id=request.user_id,
                        event_type='priority_change',
                        title=f'Priority changed to {priority}',
                        description=f'Case priority was updated'
                    )
                    
                    results.append({
                        'case_id': case_id,
                        'status': 'success',
                        'data': case.to_dict()
                    })
                else:
                    results.append({
                        'case_id': case_id,
                        'status': 'error',
                        'message': 'Case not found'
                    })
            except Exception as e:
                results.append({
                    'case_id': case_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        return jsonify({
            'results': results,
            'summary': {
                'total': len(results),
                'success': success_count,
                'error': error_count
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_batch_bp.route('/api/cases/batch/status', methods=['PUT'])
@require_auth
def update_status_batch():
    """Update status for multiple cases"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'case_ids' not in data or not data['case_ids']:
        return jsonify({'error': 'No case IDs provided'}), 400
    
    if 'status' not in data:
        return jsonify({'error': 'No status provided'}), 400
    
    case_ids = data['case_ids']
    status = data['status']
    
    try:
        results = []
        for case_id in case_ids:
            try:
                case = case_service.update_case(case_id, {'status': status}, request.user_id)
                if case:
                    # Add a timeline event for the status change
                    timeline_service.add_timeline_event(
                        case_id=case_id,
                        user_id=request.user_id,
                        event_type='status_change',
                        title=f'Status changed to {status}',
                        description=f'Case status was updated'
                    )
                    
                    results.append({
                        'case_id': case_id,
                        'status': 'success',
                        'data': case.to_dict()
                    })
                else:
                    results.append({
                        'case_id': case_id,
                        'status': 'error',
                        'message': 'Case not found'
                    })
            except Exception as e:
                results.append({
                    'case_id': case_id,
                    'status': 'error',
                    'message': str(e)
                })
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        return jsonify({
            'results': results,
            'summary': {
                'total': len(results),
                'success': success_count,
                'error': error_count
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 