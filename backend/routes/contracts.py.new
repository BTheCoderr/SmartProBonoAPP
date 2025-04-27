# Import needed modules
from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from datetime import datetime
import os
import tempfile
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Try to import pdfkit, but gracefully handle if it's not available
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    print("Warning: pdfkit module not available. PDF generation will use reportlab only.")
    PDFKIT_AVAILABLE = False

# Check if PDF generation is explicitly disabled via environment variable
import os
PDF_ENABLED = os.environ.get('PDF_ENABLED', 'true').lower() not in ('false', '0', 'no')

# Create the blueprint
contracts = Blueprint('contracts', __name__, url_prefix='/api/contracts')

@contracts.route('/generate', methods=['POST'])
def generate_contract():
    if not PDF_ENABLED:
        return jsonify({
            'error': 'PDF generation is disabled on this server',
            'message': 'The administrator has disabled PDF generation. Please contact support.'
        }), 501  # 501 Not Implemented
    
    try:
        data = request.get_json()
        template_name = data.get('template')
        form_data = data.get('data')
        
        if not template_name or not form_data:
            return jsonify({'error': 'Missing required fields'}), 400

        # Create PDF using reportlab (always available)
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12
        )
        normal_style = styles['Normal']

        # Create the document content
        elements = []
        
        # Add title
        elements.append(Paragraph(template_name.replace('_', ' ').title(), title_style))
        elements.append(Spacer(1, 12))

        # Add form data
        for field, value in form_data.items():
            elements.append(Paragraph(field + ':', heading_style))
            elements.append(Paragraph(str(value), normal_style))
            elements.append(Spacer(1, 12))

        # Add footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))

        # Build the PDF
        doc.build(elements)
        buffer.seek(0)

        # Send the PDF file
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{template_name.lower().replace(" ", "-")}-{datetime.now().strftime("%Y%m%d")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contracts.route('/templates', methods=['GET'])
def get_templates():
    try:
        templates = [
            {
                'id': 'employment',
                'name': 'Employment Contract',
                'description': 'Standard employment agreement template',
                'fields': [
                    {'name': 'title', 'type': 'text', 'required': True},
                    {'name': 'employer', 'type': 'object', 'required': True, 'fields': [
                        {'name': 'name', 'type': 'text', 'required': True},
                        {'name': 'address', 'type': 'text', 'required': True}
                    ]},
                    {'name': 'employee', 'type': 'object', 'required': True, 'fields': [
                        {'name': 'name', 'type': 'text', 'required': True},
                        {'name': 'address', 'type': 'text', 'required': True}
                    ]},
                    {'name': 'startDate', 'type': 'date', 'required': True},
                    {'name': 'compensation', 'type': 'object', 'required': True, 'fields': [
                        {'name': 'salary', 'type': 'number', 'required': True},
                        {'name': 'benefits', 'type': 'text', 'required': False}
                    ]}
                ]
            },
            {
                'id': 'nda',
                'name': 'Non-Disclosure Agreement',
                'description': 'Confidentiality agreement template',
                'fields': [
                    {'name': 'title', 'type': 'text', 'required': True},
                    {'name': 'partyA', 'type': 'text', 'required': True},
                    {'name': 'partyB', 'type': 'text', 'required': True},
                    {'name': 'effectiveDate', 'type': 'date', 'required': True},
                    {'name': 'confidentialInformation', 'type': 'text', 'required': True},
                    {'name': 'duration', 'type': 'text', 'required': True}
                ]
            },
            {
                'id': 'rental',
                'name': 'Rental Agreement',
                'description': 'Property rental/lease agreement',
                'fields': [
                    {'name': 'title', 'type': 'text', 'required': True},
                    {'name': 'landlord', 'type': 'text', 'required': True},
                    {'name': 'tenant', 'type': 'text', 'required': True},
                    {'name': 'property', 'type': 'object', 'required': True, 'fields': [
                        {'name': 'address', 'type': 'text', 'required': True},
                        {'name': 'type', 'type': 'text', 'required': True}
                    ]},
                    {'name': 'rent', 'type': 'number', 'required': True},
                    {'name': 'startDate', 'type': 'date', 'required': True},
                    {'name': 'endDate', 'type': 'date', 'required': True}
                ]
            }
        ]
        return jsonify(templates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 