from flask import Blueprint, request, jsonify
from services.case_service import CaseService
from utils.auth import require_auth
from typing import Dict, Any

# Create a blueprint for case-related routes
case_routes = Blueprint('case_routes', __name__)
case_service = CaseService()

@case_routes.route('/api/cases', methods=['GET'])
@require_auth
def get_cases():
    """Get all cases with optional filters."""
    filters = request.args.to_dict()
    try:
        cases = case_service.get_cases(
            filters=filters,
            user_id=request.user_id  # type: ignore
        )
        return jsonify([case.to_dict() for case in cases])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>', methods=['GET'])
@require_auth
def get_case(case_id: str):
    """Get a specific case by ID."""
    try:
        case = case_service.get_case(
            case_id=case_id,
            user_id=request.user_id  # type: ignore
        )
        return jsonify(case.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases', methods=['POST'])
def create_case():
    """
    Create a new case.
    
    Request Body:
        JSON object with case data
    
    Returns:
        JSON: The created case with its assigned ID
    """
    case_data = request.json
    
    if not case_data:
        return jsonify({'error': 'Missing case data'}), 400
    
    # Validate required fields
    required_fields = ['title', 'type', 'status', 'priority']
    missing_fields = [field for field in required_fields if field not in case_data]
    
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    # Create the case
    created_case = case_service.create_case(case_data)
    
    return jsonify(created_case), 201

@case_routes.route('/api/cases/<case_id>', methods=['PUT'])
def update_case(case_id):
    """
    Update an existing case.
    
    Parameters:
        case_id (str): The ID of the case to update
    
    Request Body:
        JSON object with case data to update
    
    Returns:
        JSON: The updated case or 404 error if not found
    """
    update_data = request.json
    
    if not update_data:
        return jsonify({'error': 'Missing update data'}), 400
    
    updated_case = case_service.update_case(case_id, update_data)
    
    if not updated_case:
        return jsonify({'error': 'Case not found'}), 404
    
    return jsonify(updated_case)

@case_routes.route('/api/cases/<case_id>', methods=['DELETE'])
@require_auth
def delete_case(case_id: str):
    """Delete a case by ID."""
    try:
        case_service.delete_case(
            case_id=case_id,
            user_id=request.user_id  # type: ignore
        )
        return jsonify({'message': 'Case deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/timeline', methods=['POST'])
@require_auth
def add_timeline_event(case_id: str):
    """
    Add a timeline event to a case.
    
    Parameters:
        case_id (str): The ID of the case
    
    Request Body:
        JSON object with event data:
        - event_type (str): Type of event
        - title (str): Event title
        - description (str, optional): Event description
        - metadata (dict, optional): Additional event data
    
    Returns:
        JSON: The created timeline event or error response
    """
    event_data = request.get_json()
    
    if not event_data:
        return jsonify({'error': 'Missing event data'}), 400
    
    # Validate required fields
    required_fields = ['event_type', 'title']
    missing_fields = [field for field in required_fields if field not in event_data]
    
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    try:
        event = case_service.add_timeline_event(
            case_id=case_id,
            user_id=request.user_id,  # type: ignore
            event_data=event_data
        )
        return jsonify(event.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/documents', methods=['POST'])
@require_auth
def add_document(case_id: str):
    """
    Add a document to a case.
    
    Parameters:
        case_id (str): The ID of the case
    
    Request Body:
        JSON object with document data:
        - title (str): Document title
        - document_type (str): Type of document
        - file_path (str): Path to stored file
        - metadata (dict, optional): Additional document metadata
    
    Returns:
        JSON: The created document or error response
    """
    document_data = request.get_json()
    
    if not document_data:
        return jsonify({'error': 'Missing document data'}), 400
    
    # Validate required fields
    required_fields = ['title', 'document_type', 'file_path']
    missing_fields = [field for field in required_fields if field not in document_data]
    
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    try:
        document = case_service.add_document(
            case_id=case_id,
            user_id=request.user_id,  # type: ignore
            document_data=document_data
        )
        return jsonify(document.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/documents/<document_id>', methods=['PUT'])
@require_auth
def update_document(case_id: str, document_id: str):
    """
    Update a case document.
    
    Parameters:
        case_id (str): The ID of the case
        document_id (str): The ID of the document
    
    Request Body:
        JSON object with document update data:
        - title (str, optional): New document title
        - document_type (str, optional): New document type
        - metadata (dict, optional): Updated metadata
    
    Returns:
        JSON: The updated document or error response
    """
    update_data = request.get_json()
    
    if not update_data:
        return jsonify({'error': 'Missing update data'}), 400
    
    try:
        document = case_service.document_service.update_document(
            document_id=document_id,
            user_id=request.user_id,  # type: ignore
            update_data=update_data
        )
        return jsonify(document.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/documents/<document_id>', methods=['DELETE'])
@require_auth
def delete_document(case_id: str, document_id: str):
    """
    Delete a case document.
    
    Parameters:
        case_id (str): The ID of the case
        document_id (str): The ID of the document
    
    Returns:
        JSON: Success message or error response
    """
    try:
        case_service.document_service.delete_document(
            document_id=document_id,
            user_id=request.user_id  # type: ignore
        )
        return jsonify({'message': 'Document deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/next-steps', methods=['POST'])
@require_auth
def add_next_step(case_id: str):
    """Add a next step to a case."""
    step_data = request.get_json()
    
    if not step_data:
        return jsonify({'error': 'Missing step data'}), 400
    
    required_fields = ['title', 'description', 'due_date']
    missing_fields = [field for field in required_fields if field not in step_data]
    
    if missing_fields:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    try:
        step = case_service.add_next_step(
            case_id=case_id,
            user_id=request.user_id,  # type: ignore
            step_data=step_data
        )
        return jsonify(step.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@case_routes.route('/api/cases/<case_id>/next-steps/<step_id>', methods=['PUT'])
@require_auth
def update_next_step(case_id: str, step_id: str):
    """Update a next step in a case."""
    update_data = request.get_json()
    
    if not update_data:
        return jsonify({'error': 'Missing update data'}), 400
    
    try:
        step = case_service.modify_next_step(
            case_id=case_id,
            step_id=step_id,
            user_id=request.user_id,  # type: ignore
            update_data=update_data
        )
        return jsonify(step.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 