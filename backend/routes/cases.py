from flask import Blueprint, request, jsonify, g
from typing import Dict, Any, List, Optional, Union, Tuple, cast
from services.case_service import CaseService, CaseStatus
from models.case import Case
from utils.auth import require_auth
from config.database import DatabaseConfig
from sqlalchemy.exc import SQLAlchemyError

cases_bp = Blueprint('cases', __name__)
case_service = CaseService()

@cases_bp.route('/api/cases', methods=['GET'])
@require_auth
def get_cases():
    """Get all cases with optional filters."""
    filters = {
        'status': request.args.get('status'),
        'priority': request.args.get('priority'),
        'lawyer_id': request.args.get('assigned_to'),
        'client_id': request.args.get('client_id')
    }
    
    # Remove None values from filters
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        cases = case_service.get_cases(filters)
        return jsonify([case.to_dict() for case in cases])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>', methods=['GET'])
@require_auth
def get_case(case_id: str):
    """Get a specific case by ID."""
    try:
        case = case_service.get_case(case_id)
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases', methods=['POST'])
@require_auth
def create_case():
    """Create a new case."""
    data = request.get_json()
    
    required_fields = ['title', 'case_type']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    try:
        case = case_service.create_case(data, str(g.user.id))
        return jsonify(case.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>', methods=['PUT'])
@require_auth
def update_case(case_id: str):
    """Update an existing case."""
    data = request.get_json()
    
    # Validate status if it's being updated
    if 'status' in data and data['status'] not in CaseStatus.get_valid_statuses():
        return jsonify({
            'error': 'Invalid status',
            'valid_statuses': CaseStatus.get_valid_statuses()
        }), 400
    
    try:
        case = case_service.update_case(case_id, data, str(g.user.id))
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/assign', methods=['POST'])
@require_auth
def assign_case(case_id: str):
    """Assign a case to a user."""
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        case = Case.get_by_id(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        case.update(lawyer_id=data['user_id'])
        return jsonify(case.to_dict())
    except Exception as e:
        session = DatabaseConfig.get_session()
        session.rollback()
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/priority', methods=['PUT'])
@require_auth
def update_case_priority(case_id: str):
    """Update case priority."""
    data = request.get_json()
    if 'priority' not in data:
        return jsonify({'error': 'Missing priority field'}), 400
        
    try:
        case = case_service.get_case(case_id)
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        case = case_service.update_case(case_id, {'priority': data['priority']}, g.user.id)
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/history', methods=['GET'])
@require_auth
def get_case_history(case_id: str):
    """Get case history."""
    try:
        history = case_service.get_case_timeline(case_id)  # Using timeline instead of history
        return jsonify([event.to_dict() for event in history])
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/timeline', methods=['POST'])
@require_auth
def add_timeline_event(case_id: str):
    """Add a timeline event to a case."""
    data = request.get_json()
    
    required_fields = ['event_type', 'title']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    try:
        event = case_service.add_timeline_event(case_id, str(g.user.id), data)
        return jsonify(event.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/documents', methods=['POST'])
@require_auth
def add_document(case_id: str):
    """Add a document to a case."""
    data = request.get_json()
    
    required_fields = ['name', 'type', 'url']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400
    
    try:
        document = case_service.add_document(case_id, str(g.user.id), data)
        return jsonify(document.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/documents', methods=['GET'])
@require_auth
def get_case_documents(case_id: str):
    """Get all documents for a case."""
    try:
        documents = case_service.get_case_documents(case_id)
        return jsonify([doc.to_dict() for doc in documents])
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cases_bp.route('/api/cases/<case_id>/timeline', methods=['GET'])
@require_auth
def get_case_timeline(case_id: str):
    """Get all timeline events for a case."""
    try:
        events = case_service.get_case_timeline(case_id)
        return jsonify([event.to_dict() for event in events])
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 