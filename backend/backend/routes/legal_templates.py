"""
Routes for handling legal document templates and PDF generation
"""
from flask import Blueprint, request, jsonify, send_file, render_template, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import logging
from io import BytesIO
from weasyprint import HTML
import os
from werkzeug.exceptions import BadRequest
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
bp = Blueprint('legal_templates', __name__)

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
    return bool(phone_pattern.match(phone))

def validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))

def validate_date(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

TEMPLATE_TYPES = {
    'expungement': {
        'name': 'Expungement Letter',
        'template': 'legal/expungement_letter.html',
        'description': 'Letter requesting expungement of criminal records',
        'fields': [
            {'name': 'court_name', 'type': 'text', 'required': True, 'label': 'Court Name', 'max_length': 100},
            {'name': 'case_number', 'type': 'text', 'required': True, 'label': 'Case Number', 'pattern': r'^[A-Z0-9-]+$'},
            {'name': 'defendant_name', 'type': 'text', 'required': True, 'label': 'Defendant Name', 'max_length': 100},
            {'name': 'defendant_address', 'type': 'text', 'required': True, 'label': 'Defendant Address'},
            {'name': 'defendant_phone', 'type': 'text', 'required': True, 'label': 'Defendant Phone', 'validator': 'phone'},
            {'name': 'defendant_email', 'type': 'text', 'required': True, 'label': 'Defendant Email', 'validator': 'email'},
            {'name': 'offense_date', 'type': 'date', 'required': True, 'label': 'Date of Offense', 'validator': 'date'},
            {'name': 'offense_description', 'type': 'text', 'required': True, 'label': 'Offense Description', 'max_length': 500},
            {'name': 'arrest_date', 'type': 'date', 'required': False, 'label': 'Date of Arrest', 'validator': 'date'},
            {'name': 'conviction_date', 'type': 'date', 'required': True, 'label': 'Date of Conviction', 'validator': 'date'},
            {'name': 'sentence_description', 'type': 'text', 'required': True, 'label': 'Sentence Description'},
            {'name': 'completion_date', 'type': 'date', 'required': True, 'label': 'Sentence Completion Date', 'validator': 'date'},
            {'name': 'rehabilitation_evidence', 'type': 'array', 'required': False, 'label': 'Evidence of Rehabilitation'},
            {'name': 'attorney_name', 'type': 'text', 'required': True, 'label': 'Attorney Name', 'max_length': 100},
            {'name': 'attorney_bar_number', 'type': 'text', 'required': True, 'label': 'Attorney Bar Number', 'pattern': r'^[0-9A-Z]+$'},
            {'name': 'attorney_phone', 'type': 'text', 'required': True, 'label': 'Attorney Phone', 'validator': 'phone'},
            {'name': 'attorney_email', 'type': 'text', 'required': True, 'label': 'Attorney Email', 'validator': 'email'}
        ]
    },
    'eviction': {
        'name': 'Eviction Response',
        'template': 'legal/eviction_response.html',
        'description': 'Response to eviction notice/complaint',
        'fields': [
            {'name': 'court_name', 'type': 'text', 'required': True, 'label': 'Court Name', 'max_length': 100},
            {'name': 'case_number', 'type': 'text', 'required': True, 'label': 'Case Number', 'pattern': r'^[A-Z0-9-]+$'},
            {'name': 'tenant_name', 'type': 'text', 'required': True, 'label': 'Tenant Name', 'max_length': 100},
            {'name': 'tenant_phone', 'type': 'text', 'required': True, 'label': 'Tenant Phone', 'validator': 'phone'},
            {'name': 'tenant_email', 'type': 'text', 'required': True, 'label': 'Tenant Email', 'validator': 'email'},
            {'name': 'landlord_name', 'type': 'text', 'required': True, 'label': 'Landlord Name', 'max_length': 100},
            {'name': 'landlord_address', 'type': 'text', 'required': True, 'label': 'Landlord Address'},
            {'name': 'property_address', 'type': 'text', 'required': True, 'label': 'Property Address'},
            {'name': 'lease_start_date', 'type': 'date', 'required': True, 'label': 'Lease Start Date', 'validator': 'date'},
            {'name': 'lease_end_date', 'type': 'date', 'required': False, 'label': 'Lease End Date', 'validator': 'date'},
            {'name': 'monthly_rent', 'type': 'number', 'required': True, 'label': 'Monthly Rent Amount'},
            {'name': 'notice_date', 'type': 'date', 'required': True, 'label': 'Notice Date', 'validator': 'date'},
            {'name': 'notice_type', 'type': 'select', 'required': True, 'label': 'Type of Notice',
             'options': ['Non-Payment', 'Lease Violation', 'No Cause', 'Other']},
            {'name': 'response_reasons', 'type': 'array', 'required': True, 'label': 'Response Reasons',
             'description': 'List specific reasons for contesting the eviction'},
            {'name': 'evidence_list', 'type': 'array', 'required': False, 'label': 'Evidence List',
             'description': 'List of supporting documents'},
            {'name': 'relief_requested', 'type': 'text', 'required': True, 'label': 'Relief Requested',
             'description': 'Specific relief sought from the court'}
        ]
    },
    'small_claims': {
        'name': 'Small Claims Form',
        'template': 'legal/small_claims_form.html',
        'description': 'Small claims court complaint form',
        'fields': [
            {'name': 'court_name', 'type': 'text', 'required': True, 'label': 'Court Name', 'max_length': 100},
            {'name': 'plaintiff_name', 'type': 'text', 'required': True, 'label': 'Plaintiff Name', 'max_length': 100},
            {'name': 'plaintiff_address', 'type': 'text', 'required': True, 'label': 'Plaintiff Address'},
            {'name': 'plaintiff_phone', 'type': 'text', 'required': True, 'label': 'Plaintiff Phone', 'validator': 'phone'},
            {'name': 'plaintiff_email', 'type': 'text', 'required': True, 'label': 'Plaintiff Email', 'validator': 'email'},
            {'name': 'defendant_name', 'type': 'text', 'required': True, 'label': 'Defendant Name', 'max_length': 100},
            {'name': 'defendant_address', 'type': 'text', 'required': True, 'label': 'Defendant Address'},
            {'name': 'defendant_phone', 'type': 'text', 'required': False, 'label': 'Defendant Phone', 'validator': 'phone'},
            {'name': 'claim_amount', 'type': 'number', 'required': True, 'label': 'Claim Amount',
             'min': 0, 'max': 10000, 'description': 'Maximum amount varies by jurisdiction'},
            {'name': 'claim_type', 'type': 'select', 'required': True, 'label': 'Type of Claim',
             'options': ['Contract Dispute', 'Property Damage', 'Personal Injury', 'Unpaid Debt', 'Other']},
            {'name': 'claim_reason', 'type': 'text', 'required': True, 'label': 'Reason for Claim',
             'max_length': 1000, 'description': 'Detailed explanation of the claim'},
            {'name': 'incident_date', 'type': 'date', 'required': True, 'label': 'Date of Incident', 'validator': 'date'},
            {'name': 'demand_letter_date', 'type': 'date', 'required': False, 'label': 'Date Demand Letter Sent', 'validator': 'date'},
            {'name': 'evidence_list', 'type': 'array', 'required': True, 'label': 'Evidence List',
             'description': 'List all supporting documents and evidence'},
            {'name': 'witness_list', 'type': 'array', 'required': False, 'label': 'Witness List',
             'description': 'Names and contact information of witnesses'},
            {'name': 'filing_date', 'type': 'date', 'required': True, 'label': 'Filing Date', 'validator': 'date'},
            {'name': 'service_method', 'type': 'select', 'required': True, 'label': 'Method of Service',
             'options': ['Personal Service', 'Certified Mail', 'Sheriff Service', 'Process Server']}
        ]
    },
    'tenant_rights': {
        'name': 'Tenant Rights Guide',
        'template': 'legal/tenant_rights.html',
        'description': 'Comprehensive guide to tenant rights',
        'fields': [
            {'name': 'state_name', 'type': 'text', 'required': True, 'label': 'State Name'},
            {'name': 'jurisdiction', 'type': 'text', 'required': False, 'label': 'Local Jurisdiction',
             'description': 'City or county if local laws apply'},
            {'name': 'max_security_deposit', 'type': 'text', 'required': True, 'label': 'Maximum Security Deposit'},
            {'name': 'deposit_return_timeline', 'type': 'text', 'required': True, 'label': 'Deposit Return Timeline'},
            {'name': 'emergency_contact', 'type': 'text', 'required': True, 'label': 'Emergency Contact'},
            {'name': 'emergency_maintenance_procedures', 'type': 'text', 'required': True, 'label': 'Emergency Maintenance Procedures'},
            {'name': 'month_to_month_notice', 'type': 'text', 'required': True, 'label': 'Month-to-Month Notice Period'},
            {'name': 'fixed_term_notice', 'type': 'text', 'required': True, 'label': 'Fixed-Term Notice Period'},
            {'name': 'eviction_notice_period', 'type': 'text', 'required': True, 'label': 'Eviction Notice Period'},
            {'name': 'rent_increase_rules', 'type': 'text', 'required': True, 'label': 'Rent Increase Rules'},
            {'name': 'legal_aid_contact', 'type': 'text', 'required': True, 'label': 'Legal Aid Contact'},
            {'name': 'legal_aid_hours', 'type': 'text', 'required': True, 'label': 'Legal Aid Office Hours'},
            {'name': 'housing_authority_contact', 'type': 'text', 'required': True, 'label': 'Housing Authority Contact'},
            {'name': 'housing_authority_hours', 'type': 'text', 'required': True, 'label': 'Housing Authority Office Hours'},
            {'name': 'tenant_org_contact', 'type': 'text', 'required': True, 'label': 'Tenant Organization Contact'},
            {'name': 'tenant_org_services', 'type': 'array', 'required': True, 'label': 'Available Tenant Services'},
            {'name': 'fair_housing_contact', 'type': 'text', 'required': True, 'label': 'Fair Housing Office Contact'},
            {'name': 'current_date', 'type': 'date', 'required': True, 'label': 'Current Date', 'validator': 'date'}
        ]
    }
}

def validate_field_value(field: Dict[str, Any], value: Any) -> List[str]:
    """Validate a field value based on its rules."""
    errors = []
    
    if field['required'] and not value:
        errors.append(f"{field['label']} is required")
        return errors
        
    if not value:
        return errors
        
    if 'validator' in field:
        if field['validator'] == 'phone' and not validate_phone(str(value)):
            errors.append(f"{field['label']} must be a valid phone number")
        elif field['validator'] == 'email' and not validate_email(str(value)):
            errors.append(f"{field['label']} must be a valid email address")
        elif field['validator'] == 'date' and not validate_date(str(value)):
            errors.append(f"{field['label']} must be a valid date (YYYY-MM-DD)")
            
    if field['type'] == 'text' and 'max_length' in field:
        if len(str(value)) > field['max_length']:
            errors.append(f"{field['label']} must be at most {field['max_length']} characters")
            
    if 'pattern' in field and not re.match(field['pattern'], str(value)):
        errors.append(f"{field['label']} has an invalid format")
        
    if field['type'] == 'number':
        try:
            num_value = float(value)
            if 'min' in field and num_value < field['min']:
                errors.append(f"{field['label']} must be at least {field['min']}")
            if 'max' in field and num_value > field['max']:
                errors.append(f"{field['label']} must be at most {field['max']}")
        except ValueError:
            errors.append(f"{field['label']} must be a number")
            
    if field['type'] == 'select' and 'options' in field:
        if str(value) not in field['options']:
            errors.append(f"{field['label']} must be one of: {', '.join(field['options'])}")
            
    return errors

def generate_pdf_from_template(template_path: str, data: Dict[str, Any]) -> BytesIO:
    """Generate a PDF from an HTML template with enhanced styling."""
    try:
        # Add any computed or formatted values
        if 'current_date' in data:
            data['formatted_date'] = datetime.strptime(data['current_date'], '%Y-%m-%d').strftime('%B %d, %Y')
            
        # Format currency values
        if 'claim_amount' in data:
            data['formatted_claim_amount'] = "${:,.2f}".format(float(data['claim_amount']))
        if 'monthly_rent' in data:
            data['formatted_monthly_rent'] = "${:,.2f}".format(float(data['monthly_rent']))

        # Format dates consistently
        date_fields = ['offense_date', 'arrest_date', 'conviction_date', 'completion_date',
                      'lease_start_date', 'lease_end_date', 'notice_date', 'incident_date',
                      'demand_letter_date', 'filing_date']
        for field in date_fields:
            if field in data and data[field]:
                data[f'formatted_{field}'] = datetime.strptime(data[field], '%Y-%m-%d').strftime('%B %d, %Y')

        # Add document metadata
        data['generation_date'] = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        data['document_id'] = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{template_path.split('/')[-1]}"

        # Render the HTML template with the provided data
        html_content = render_template(template_path, **data)
        
        # Get the path to our CSS file
        css_path = os.path.join(current_app.root_path, 'static', 'css', 'pdf_styles.css')
        
        # Create a PDF from the HTML content with custom styling
        html = HTML(string=html_content)
        pdf_buffer = BytesIO()
        
        # Apply CSS styling and generate PDF with additional options
        html.write_pdf(
            pdf_buffer,
            stylesheets=[css_path],
            # Enable additional PDF features
            presentational_hints=True,
            optimize_size=('fonts', 'images'),
            pdf_version='1.7',
            pdf_forms=True,
            # Add document metadata
            attachments={
                'document.html': html_content.encode('utf-8'),
                'styles.css': open(css_path, 'rb').read()
            },
            # Set PDF metadata
            metadata={
                'title': f"Legal Document - {template_path.split('/')[-1].replace('.html', '')}",
                'author': 'SmartProBono Legal Services',
                'subject': 'Legal Document',
                'keywords': 'legal,document,template',
                'creator': 'SmartProBono Document Generator',
                'producer': 'WeasyPrint'
            }
        )
        
        pdf_buffer.seek(0)
        return pdf_buffer
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

@bp.route('/templates', methods=['GET'])
def get_templates():
    """Get all available legal document templates."""
    try:
        templates = [{
            'id': template_id,
            'name': template_info['name'],
            'description': template_info['description'],
            'fields': template_info['fields']
        } for template_id, template_info in TEMPLATE_TYPES.items()]
        
        return jsonify(templates)
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get a specific template's information."""
    try:
        if template_id not in TEMPLATE_TYPES:
            return jsonify({'error': 'Template not found'}), 404
            
        template_info = TEMPLATE_TYPES[template_id]
        return jsonify({
            'id': template_id,
            'name': template_info['name'],
            'description': template_info['description'],
            'fields': template_info['fields']
        })
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/generate/<template_id>', methods=['POST'])
@jwt_required()
def generate_document(template_id):
    """Generate a document from a template with enhanced validation."""
    try:
        if template_id not in TEMPLATE_TYPES:
            return jsonify({'error': 'Template not found'}), 404
            
        template_info = TEMPLATE_TYPES[template_id]
        data = request.get_json()
        
        if not data:
            raise BadRequest('No data provided')
            
        # Validate all fields
        validation_errors = []
        for field in template_info['fields']:
            field_value = data.get(field['name'])
            field_errors = validate_field_value(field, field_value)
            validation_errors.extend(field_errors)
            
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': validation_errors
            }), 400
            
        # Generate PDF with error handling
        try:
            pdf_buffer = generate_pdf_from_template(template_info['template'], data)
        except Exception as e:
            logger.error(f"PDF generation error: {str(e)}")
            return jsonify({'error': 'Failed to generate PDF'}), 500
            
        # Generate a meaningful filename
        filename = f"{template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Send the PDF file with proper headers
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename,
            max_age=0
        )
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating document: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 