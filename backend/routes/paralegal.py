from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

# Import your database models here
from models.case import CaseStore
from models.document_template import DocumentTemplate
from models.screening_question import ScreeningQuestion

paralegal_bp = Blueprint('paralegal', __name__, url_prefix='/api/paralegal')

@paralegal_bp.route('/', methods=['GET'])
def get_routes():
    """Get documentation for all paralegal API routes"""
    routes = [
        {
            'endpoint': '/api/paralegal/',
            'method': 'GET',
            'description': 'Get documentation for all paralegal API routes',
            'auth_required': False
        },
        {
            'endpoint': '/api/paralegal/case',
            'method': 'POST',
            'description': 'Create a new case with client information',
            'auth_required': True,
            'required_fields': ['clientName', 'clientEmail', 'caseType']
        },
        {
            'endpoint': '/api/paralegal/cases',
            'method': 'GET',
            'description': 'Get all cases for the current user',
            'auth_required': True,
            'query_params': ['status', 'case_type']
        },
        {
            'endpoint': '/api/paralegal/case/<case_id>',
            'method': 'GET',
            'description': 'Get a specific case by ID',
            'auth_required': True
        },
        {
            'endpoint': '/api/paralegal/case/<case_id>',
            'method': 'PUT',
            'description': 'Update a specific case',
            'auth_required': True
        },
        {
            'endpoint': '/api/paralegal/templates',
            'method': 'GET',
            'description': 'Get all document templates',
            'auth_required': True,
            'query_params': ['type']
        },
        {
            'endpoint': '/api/paralegal/screening-questions',
            'method': 'GET',
            'description': 'Get screening questions',
            'auth_required': True,
            'query_params': ['category']
        },
        {
            'endpoint': '/api/paralegal/generate-document/<template_id>',
            'method': 'POST',
            'description': 'Generate a document from a template with case data',
            'auth_required': True
        }
    ]
    
    return jsonify({
        'name': 'Paralegal API',
        'version': '1.0.0',
        'description': 'API for the Virtual Paralegal Assistant',
        'routes': routes
    })

@paralegal_bp.route('/case', methods=['POST'])
@jwt_required()
def create_case():
    """Create a new case with client information"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['clientName', 'clientEmail', 'caseType']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create new case object
    new_case = {
        'client_name': data['clientName'],
        'client_email': data['clientEmail'],
        'client_phone': data.get('clientPhone', ''),
        'case_type': data['caseType'],
        'description': data.get('description', ''),
        'urgency': data.get('urgency', 'medium'),
        'initial_consult_date': data.get('initialConsultDate', ''),
        'status': 'new',
        'assigned_to': current_user,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    # Save to database
    case_id = CaseStore.create(new_case)
    
    return jsonify({
        'success': True,
        'message': 'Case created successfully',
        'case_id': str(case_id)
    }), 201


@paralegal_bp.route('/cases', methods=['GET'])
@jwt_required()
def get_cases():
    """Get all cases for the current user"""
    current_user = get_jwt_identity()
    
    # Get query parameters for filtering
    status = request.args.get('status')
    case_type = request.args.get('case_type')
    
    # Build query
    query = {'assigned_to': current_user}
    if status:
        query['status'] = status
    if case_type:
        query['case_type'] = case_type
    
    # Get cases from database
    cases = CaseStore.find(query)
    
    return jsonify({
        'success': True,
        'cases': cases
    })


@paralegal_bp.route('/case/<case_id>', methods=['GET'])
@jwt_required()
def get_case(case_id):
    """Get a specific case by ID"""
    current_user = get_jwt_identity()
    
    # Find case in database
    case = CaseStore.find_one({
        '_id': ObjectId(case_id),
        'assigned_to': current_user
    })
    
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    return jsonify({
        'success': True,
        'case': case
    })


@paralegal_bp.route('/case/<case_id>', methods=['PUT'])
@jwt_required()
def update_case(case_id):
    """Update a specific case"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Find case in database
    case = CaseStore.find_one({
        '_id': ObjectId(case_id),
        'assigned_to': current_user
    })
    
    if not case:
        return jsonify({'error': 'Case not found'}), 404
    
    # Update fields
    update_data = {
        'client_name': data.get('clientName', case['client_name']),
        'client_email': data.get('clientEmail', case['client_email']),
        'client_phone': data.get('clientPhone', case['client_phone']),
        'case_type': data.get('caseType', case['case_type']),
        'description': data.get('description', case['description']),
        'urgency': data.get('urgency', case['urgency']),
        'initial_consult_date': data.get('initialConsultDate', case['initial_consult_date']),
        'status': data.get('status', case['status']),
        'updated_at': datetime.utcnow()
    }
    
    # Update in database
    CaseStore.update_one({'_id': ObjectId(case_id)}, {'$set': update_data})
    
    return jsonify({
        'success': True,
        'message': 'Case updated successfully'
    })


@paralegal_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_document_templates():
    """Get all document templates"""
    template_type = request.args.get('type')
    
    # Build query
    query = {}
    if template_type:
        query['type'] = template_type
    
    # Get templates from database
    templates = DocumentTemplate.find(query)
    
    return jsonify({
        'success': True,
        'templates': templates
    })


@paralegal_bp.route('/screening-questions', methods=['GET'])
@jwt_required()
def get_screening_questions():
    """Get screening questions"""
    category = request.args.get('category')
    
    # Build query
    query = {}
    if category:
        query['category'] = category
    
    # Get questions from database
    questions = ScreeningQuestion.find(query)
    
    return jsonify({
        'success': True,
        'questions': questions
    })


@paralegal_bp.route('/generate-document/<template_id>', methods=['POST'])
@jwt_required()
def generate_document(template_id):
    """Generate a document from a template with case data"""
    current_user = get_jwt_identity()
    data = request.get_json()
    
    # Get template from database
    template = DocumentTemplate.find_one({'_id': ObjectId(template_id)})
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    # In a real application, this would process the template with the data
    # and generate a document (PDF, DOCX, etc.)
    # For demonstration, we'll just return a success message
    
    return jsonify({
        'success': True,
        'message': 'Document generated successfully',
        'document_url': f'/documents/generated/{template_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pdf'
    }) 