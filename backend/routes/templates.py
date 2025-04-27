"""
Routes for handling document templates and PDF generation
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.models.template import Template
from backend.extensions import db
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
from datetime import datetime

logger = logging.getLogger(__name__)
bp = Blueprint('templates', __name__)

def create_pdf_template(template: Template, data: dict) -> BytesIO:
    """Create a PDF from template"""
    if not template:
        raise ValueError("Template not found")
        
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, template.title)
    
    # Add date
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    # Add form fields
    y_position = 680
    p.setFont("Helvetica", 12)
    for field in template.fields:
        field_value = data.get(field, '')
        p.drawString(50, y_position, f"{field.replace('_', ' ').title()}: {field_value}")
        y_position -= 30
    
    p.save()
    buffer.seek(0)
    return buffer

@bp.route('/api/templates', methods=['GET'])
@jwt_required()
def list_templates():
    """List available templates"""
    templates = Template.query.filter_by(is_active=True).all()
    return jsonify({
        'templates': [template.to_dict() for template in templates]
    }), 200

@bp.route('/api/templates', methods=['POST'])
@jwt_required()
def create_template():
    """Create a new template"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['template_id', 'name', 'title', 'fields']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    try:
        template = Template.from_dict(data)
        db.session.add(template)
        db.session.commit()
        return jsonify(template.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating template: {str(e)}')
        return jsonify({'error': 'Error creating template'}), 500

@bp.route('/api/templates/<template_id>', methods=['POST'])
@jwt_required()
def generate_pdf(template_id):
    """Generate PDF from template"""
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'User not authenticated'}), 401

    template = Template.query.filter_by(template_id=template_id, is_active=True).first()
    if not template:
        return jsonify({'error': f'Template {template_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        pdf_buffer = create_pdf_template(template, data)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{template_id}_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Error generating PDF: {str(e)}')
        return jsonify({'error': f'Error generating PDF: {str(e)}'}), 500

@bp.route('/api/templates/<template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    """Update an existing template"""
    template = Template.query.filter_by(template_id=template_id).first()
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Create new version
        new_template = Template.from_dict({
            **data,
            'template_id': template_id,
            'version': template.version + 1
        })
        
        # Deactivate old version
        template.is_active = False
        
        db.session.add(new_template)
        db.session.commit()
        
        return jsonify(new_template.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating template: {str(e)}')
        return jsonify({'error': 'Error updating template'}), 500

@bp.route('/api/templates/guide/<guide_id>', methods=['GET'])
def get_guide(guide_id):
    """Get a legal guide PDF"""
    try:
        guide_path = os.path.join('resources', 'guides', f'{guide_id}.pdf')
        if not os.path.exists(guide_path):
            return jsonify({'error': 'Guide not found'}), 404

        return send_file(
            guide_path,
            mimetype='application/pdf',
            as_attachment=True
        )

    except Exception as e:
        logger.error(f'Error retrieving guide: {str(e)}')
        return jsonify({'error': 'Error retrieving guide'}), 500 