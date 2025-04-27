"""Form templates routes"""
from flask import Blueprint, jsonify, request
from backend.extensions import db
from backend.models.template import Template
from backend.auth.decorators import admin_required
from backend.utils.validation import validate_json, TEMPLATE_SCHEMA, FORM_DATA_SCHEMA
import logging

logger = logging.getLogger(__name__)
form_templates_bp = Blueprint('form_templates', __name__)

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