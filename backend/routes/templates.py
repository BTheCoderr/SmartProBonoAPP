"""
Routes for handling document templates and PDF generation
"""
from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.template import Template
from extensions import db
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
from datetime import datetime
from services.pdf_service import get_pdf_service

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
    """List all templates"""
    try:
        templates = Template.query.all()
        return jsonify([t.to_dict() for t in templates])
    except Exception as e:
        logger.error(f'Error listing templates: {str(e)}')
        return jsonify({'error': 'Failed to list templates'}), 500

@bp.route('/api/templates/<string:template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    """Get a template by ID"""
    try:
        template = Template.query.filter_by(template_id=template_id).first()
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify(template.to_dict())
    except Exception as e:
        logger.error(f'Error getting template: {str(e)}')
        return jsonify({'error': 'Failed to get template'}), 500

@bp.route('/api/templates/preview', methods=['POST'])
def preview_template():
    """Generate a document preview from template"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        template_id = data.get('template_id')
        if not template_id:
            return jsonify({'error': 'No template_id provided'}), 400
            
        template_data = data.get('data', {})
        
        # Validate required fields based on template type
        # This is a simple validation, more complex validation should be implemented
        if not template_data.get('court_county') and template_id == 'small_claims_complaint':
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate PDF preview
        pdf_service = get_pdf_service()
        output_format = data.get('output_format', 'pdf')
        
        # Check if watermark is requested
        watermark_text = data.get('watermark_text', 'PREVIEW')
        
        # Generate document with preview watermark
        file_path = pdf_service.generate_legal_document(
            template_id=template_id,
            data=template_data,
            output_format=output_format,
            watermark_text=watermark_text
        )
        
        # Return the file
        return send_file(
            file_path,
            mimetype='application/pdf' if output_format == 'pdf' else 'text/html',
            as_attachment=True,
            download_name=f"{template_id}_preview.{output_format}"
        )
        
    except ValueError as e:
        logger.error(f'Validation error in template preview: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error generating template preview: {str(e)}')
        return jsonify({'error': 'Failed to generate preview'}), 500
        
@bp.route('/api/templates/generate', methods=['POST'])
@jwt_required()
def generate_document():
    """Generate a document from template and save it to the user's documents"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        template_id = data.get('template_id')
        if not template_id:
            return jsonify({'error': 'No template_id provided'}), 400
            
        template_data = data.get('data', {})
        
        # Generate document
        pdf_service = get_pdf_service()
        file_path = pdf_service.generate_legal_document(
            template_id=template_id,
            data=template_data
        )
        
        # Save document to user's documents
        from models.document import Document
        
        document = Document(
            user_id=user_id,
            title=f"{template_id.replace('_', ' ').title()} - {datetime.now().strftime('%Y-%m-%d')}",
            file_path=file_path,
            file_type='application/pdf',
            source='generated',
            metadata={
                'template_id': template_id,
                'template_data': template_data
            }
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document generated successfully',
            'document_id': document.id
        }), 201
        
    except ValueError as e:
        logger.error(f'Validation error in document generation: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error generating document: {str(e)}')
        return jsonify({'error': 'Failed to generate document'}), 500

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