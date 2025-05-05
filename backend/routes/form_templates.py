"""Form templates routes"""
from flask import Blueprint, jsonify, request, current_app
from extensions import db
from models.template import Template
from auth.decorators import admin_required
from utils.validation import validate_json, TEMPLATE_SCHEMA, FORM_DATA_SCHEMA
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..models.form import Form, FormDraft
from ..models.document import Document
from ..services.pdf_service import generate_pdf
from ..services.form_service import validate_form_data
from ..utils.error_handlers import handle_api_error
import logging

logger = logging.getLogger(__name__)
form_templates_bp = Blueprint('form_templates', __name__)
forms_bp = Blueprint('forms', __name__)

@form_templates_bp.route('/api/templates', methods=['GET'])
@admin_required()
def list_templates():
    """List all templates"""
    try:
        templates = Template.query.all()
        return jsonify([t.to_dict() for t in templates])
    except Exception as e:
        logger.error(f'Error listing templates: {str(e)}')
        return jsonify({'error': 'Failed to list templates'}), 500

@form_templates_bp.route('/api/templates', methods=['POST'])
@admin_required()
@validate_json(TEMPLATE_SCHEMA)
def create_template():
    """Create a new template"""
    try:
        template = Template.from_dict(request.json)
        db.session.add(template)
        db.session.commit()
        return jsonify(template.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating template: {str(e)}')
        return jsonify({'error': 'Failed to create template'}), 500

@form_templates_bp.route('/api/templates/<template_id>', methods=['GET'])
@admin_required()
def get_template(template_id):
    """Get a specific template"""
    try:
        template = Template.query.filter_by(template_id=template_id).first()
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify(template.to_dict())
    except Exception as e:
        logger.error(f'Error getting template {template_id}: {str(e)}')
        return jsonify({'error': 'Failed to get template'}), 500

@form_templates_bp.route('/api/templates/<template_id>', methods=['PUT'])
@admin_required()
@validate_json(TEMPLATE_SCHEMA)
def update_template(template_id):
    """Update a template"""
    try:
        template = Template.query.filter_by(template_id=template_id).first()
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'No update data provided or invalid format'}), 400
        
        # Update fields
        for key, value in dict(data).items():
            setattr(template, key, value)
        
        db.session.commit()
        return jsonify(template.to_dict())
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating template {template_id}: {str(e)}')
        return jsonify({'error': 'Failed to update template'}), 500

@form_templates_bp.route('/api/templates/<template_id>', methods=['DELETE'])
@admin_required()
def delete_template(template_id):
    """Delete a template"""
    try:
        template = Template.query.filter_by(template_id=template_id).first()
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        db.session.delete(template)
        db.session.commit()
        return jsonify({'message': 'Template deleted'})
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting template {template_id}: {str(e)}')
        return jsonify({'error': 'Failed to delete template'}), 500

@form_templates_bp.route('/api/templates/<template_id>/generate', methods=['POST'])
@admin_required()
@validate_json(FORM_DATA_SCHEMA)
def generate_form(template_id):
    """Generate a form from a template"""
    try:
        template = Template.query.filter_by(template_id=template_id).first()
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        # Here you would implement the actual form generation logic
        # For now, we'll just return a success message
        return jsonify({'message': 'Form generated successfully'})
    except Exception as e:
        logger.error(f'Error generating form from template {template_id}: {str(e)}')
        return jsonify({'error': 'Failed to generate form'}), 500

@forms_bp.route('/<form_type>/submit', methods=['POST'])
@jwt_required()
@handle_api_error
def submit_form(form_type):
    """Submit a form and generate the corresponding document."""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Validate form data
    validation_errors = validate_form_data(form_type, data)
    if validation_errors:
        return jsonify({'errors': validation_errors}), 400

    try:
        # Create form record
        form = Form(
            user_id=user_id,
            form_type=form_type,
            data=data,
            status='submitted',
            submitted_at=datetime.utcnow()
        )
        db.session.add(form)
        
        # Generate PDF document
        pdf_data = generate_pdf(form_type, data)
        
        # Create document record
        document = Document(
            user_id=user_id,
            form_id=form.id,
            document_type=f"{form_type}_form",
            file_data=pdf_data,
            status='generated',
            generated_at=datetime.utcnow()
        )
        db.session.add(document)
        
        # Delete any existing drafts
        FormDraft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).delete()
        
        db.session.commit()

        return jsonify({
            'message': 'Form submitted successfully',
            'form_id': form.id,
            'document_id': document.id
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting form: {str(e)}")
        return jsonify({'error': 'Failed to submit form'}), 500

@forms_bp.route('/<form_type>/draft', methods=['POST'])
@jwt_required()
@handle_api_error
def save_draft(form_type):
    """Save form draft."""
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        # Update existing draft or create new one
        draft = FormDraft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).first()

        if draft:
            draft.data = data
            draft.updated_at = datetime.utcnow()
        else:
            draft = FormDraft(
                user_id=user_id,
                form_type=form_type,
                data=data
            )
            db.session.add(draft)

        db.session.commit()

        return jsonify({
            'message': 'Draft saved successfully',
            'draft_id': draft.id
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving draft: {str(e)}")
        return jsonify({'error': 'Failed to save draft'}), 500

@forms_bp.route('/<form_type>/draft', methods=['GET'])
@jwt_required()
@handle_api_error
def get_draft(form_type):
    """Get the latest draft for a form type."""
    user_id = get_jwt_identity()

    try:
        draft = FormDraft.query.filter_by(
            user_id=user_id,
            form_type=form_type
        ).first()

        if not draft:
            return jsonify({'message': 'No draft found'}), 404

        return jsonify({
            'draft_id': draft.id,
            'data': draft.data,
            'created_at': draft.created_at,
            'updated_at': draft.updated_at
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving draft: {str(e)}")
        return jsonify({'error': 'Failed to retrieve draft'}), 500

@forms_bp.route('/<form_type>/generate', methods=['POST'])
@jwt_required()
@handle_api_error
def generate_document(form_type):
    """Generate a document from form data without submitting the form."""
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        # Generate PDF document
        pdf_data = generate_pdf(form_type, data)
        
        # Create temporary document record
        document = Document(
            user_id=user_id,
            document_type=f"{form_type}_preview",
            file_data=pdf_data,
            status='preview',
            generated_at=datetime.utcnow()
        )
        db.session.add(document)
        db.session.commit()

        return jsonify({
            'message': 'Document generated successfully',
            'document_id': document.id
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error generating document: {str(e)}")
        return jsonify({'error': 'Failed to generate document'}), 500 