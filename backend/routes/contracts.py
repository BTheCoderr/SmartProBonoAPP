from flask import Blueprint, request, jsonify, send_file
from jinja2 import Template
import pdfkit
import os
from datetime import datetime
import tempfile
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from dotenv import load_dotenv

load_dotenv()

# Support Information
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@smartprobono.org')
SUPPORT_HOURS = '9:00 AM - 5:00 PM EST'
SUPPORT_RESPONSE_TIME = '24-48 hours'

contracts_bp = Blueprint('contracts', __name__, url_prefix='/api/contracts')

# Template definitions with placeholders and metadata
TEMPLATES = {
    'Last Will and Testament': {
        'template': '''
            <div class="legal-document">
                <h1 class="document-title">LAST WILL AND TESTAMENT</h1>
                
                <p class="preamble">I, {{fullName}}, residing at {{address}}, being of sound mind and memory, do hereby make, publish, and declare this to be my Last Will and Testament, hereby revoking all previous wills and codicils made by me.</p>
                
                <h2>ARTICLE I - PRELIMINARY DECLARATIONS</h2>
                <p>A. I am currently a resident of {{state}}.</p>
                <p>B. Family Status: {{familyStatus}}</p>
                
                <h2>ARTICLE II - DISPOSITION OF PROPERTY</h2>
                {{#each beneficiaries}}
                <p>I give, devise, and bequeath {{this.share}} to {{this.name}}, {{this.relationship}}.</p>
                {{/each}}
                
                <h2>ARTICLE III - EXECUTOR</h2>
                <p>I hereby nominate and appoint {{executor.name}}, residing at {{executor.address}}, as Executor of this Will. If {{executor.name}} is unable or unwilling to serve, I appoint {{alternateExecutor.name}} as alternate Executor.</p>
                
                <div class="signature-section">
                    <p>IN WITNESS WHEREOF, I have hereunto set my hand this {{date}}.</p>
                    <div class="signature-line">
                        <p>____________________________</p>
                        <p>{{fullName}} (Testator)</p>
                    </div>
                </div>
                
                <div class="witness-section">
                    <h3>WITNESSES</h3>
                    <p>This Will was signed, published, and declared by {{fullName}}, as their Last Will and Testament, in our presence, and we, at their request and in their presence, and in the presence of each other, have subscribed our names as witnesses.</p>
                    <div class="witness-signatures">
                        <div class="signature-line">
                            <p>____________________________</p>
                            <p>Witness 1 Signature</p>
                        </div>
                        <div class="signature-line">
                            <p>____________________________</p>
                            <p>Witness 2 Signature</p>
                        </div>
                    </div>
                </div>
            </div>
        ''',
        'required_fields': ['fullName', 'address', 'state', 'familyStatus', 'beneficiaries', 'executor'],
        'optional_fields': ['alternateExecutor'],
        'validation_rules': {
            'fullName': r'^[A-Za-z\s\-\'\.]+$',
            'state': r'^[A-Za-z\s]+$',
            'beneficiaries': {
                'min_length': 1,
                'fields': ['name', 'relationship', 'share']
            }
        }
    },
    
    'Power of Attorney': {
        'template': '''
            <div class="legal-document">
                <h1 class="document-title">DURABLE POWER OF ATTORNEY</h1>
                
                <p class="preamble">This Durable Power of Attorney is made on {{date}} by {{grantor}} ("Principal"), residing at {{grantorAddress}}.</p>
                
                <h2>1. APPOINTMENT OF AGENT</h2>
                <p>I hereby appoint {{attorney.name}}, residing at {{attorney.address}} ("Agent"), to act as my Attorney-in-Fact.</p>
                
                <h2>2. POWERS GRANTED</h2>
                <div class="powers-section">
                    {{#each powers}}
                    <p>☐ {{this.description}}</p>
                    {{/each}}
                </div>
                
                <h2>3. DURABILITY</h2>
                <p>This Power of Attorney shall not be affected by my subsequent disability or incapacity.</p>
                
                <h2>4. EFFECTIVE DATE</h2>
                <p>This Power of Attorney shall become effective on {{effectiveDate}}.</p>
                
                <h2>5. TERMINATION</h2>
                <p>This Power of Attorney shall terminate upon my death or by my revocation in writing.</p>
                
                <div class="signature-section">
                    <p>IN WITNESS WHEREOF, I have hereunto set my hand on {{date}}.</p>
                    <div class="signature-line">
                        <p>____________________________</p>
                        <p>{{grantor}} (Principal)</p>
                    </div>
                </div>
                
                <div class="notary-section">
                    <h3>NOTARY ACKNOWLEDGMENT</h3>
                    <p>State of ________________</p>
                    <p>County of ________________</p>
                    <p>On {{date}}, before me personally appeared {{grantor}}, proved to me through satisfactory evidence of identification to be the person whose name is signed above.</p>
                    <div class="signature-line">
                        <p>____________________________</p>
                        <p>Notary Public</p>
                        <p>My Commission Expires: ________________</p>
                    </div>
                </div>
            </div>
        ''',
        'required_fields': ['grantor', 'grantorAddress', 'attorney', 'powers', 'effectiveDate'],
        'validation_rules': {
            'powers': {
                'min_length': 1,
                'fields': ['description']
            }
        }
    },
    
    'Rental Agreement': '''
        RENTAL AGREEMENT
        
        This agreement is made between {{landlord}} ("Landlord") and {{tenant}} ("Tenant").
        
        PROPERTY:
        {{property}}
        
        TERM:
        {{term}}
        
        RENT:
        {{rent}}
        
        Date: {{date}}
        Signatures:
        Landlord: _________________
        Tenant: _________________
    ''',
    
    'Employment Contract': {
        'template': '''
            <div class="legal-document">
                <h1 class="document-title">EMPLOYMENT AGREEMENT</h1>
                
                <p class="preamble">This Employment Agreement (the "Agreement") is made and entered into on {{date}} by and between:</p>
                
                <p><strong>{{employer.name}}</strong>, a company organized under the laws of {{employer.state}}, having its principal place of business at {{employer.address}} (the "Employer")</p>
                
                <p>and</p>
                
                <p><strong>{{employee.name}}</strong>, residing at {{employee.address}} (the "Employee").</p>
                
                <h2>1. POSITION AND DUTIES</h2>
                <p>1.1. Position: The Employee shall be employed as {{position.title}} and shall perform the duties described in Schedule A attached hereto.</p>
                <p>1.2. Reporting: The Employee shall report to {{position.reportsTo}}.</p>
                
                <h2>2. TERM AND TERMINATION</h2>
                <p>2.1. Commencement: This Agreement shall commence on {{startDate}}.</p>
                <p>2.2. Term: {{#if isFixedTerm}}This Agreement shall continue for a fixed term of {{term}} months.{{else}}This Agreement shall continue indefinitely until terminated in accordance with this Agreement.{{/if}}</p>
                
                <h2>3. COMPENSATION</h2>
                <p>3.1. Base Salary: The Employee shall receive a base salary of {{compensation.baseSalary}} per {{compensation.paymentInterval}}.</p>
                {{#if compensation.bonus}}
                <p>3.2. Bonus: {{compensation.bonus}}</p>
                {{/if}}
                
                <h2>4. BENEFITS</h2>
                <div class="benefits-section">
                    {{#each benefits}}
                    <p>• {{this}}</p>
                    {{/each}}
                </div>
                
                <h2>5. WORKING HOURS AND LOCATION</h2>
                <p>5.1. Hours: {{workSchedule.hours}}</p>
                <p>5.2. Location: {{workSchedule.location}}</p>
                
                <h2>6. CONFIDENTIALITY</h2>
                <p>The Employee agrees to maintain the confidentiality of the Employer's proprietary information and trade secrets during and after employment.</p>
                
                <h2>7. INTELLECTUAL PROPERTY</h2>
                <p>All work product developed by the Employee during the course of employment shall be the exclusive property of the Employer.</p>
                
                <h2>8. NON-COMPETE</h2>
                <p>{{nonCompete}}</p>
                
                <div class="signature-section">
                    <p>IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.</p>
                    
                    <div class="signatures">
                        <div class="signature-block">
                            <p class="signature-line">____________________________</p>
                            <p>For and on behalf of {{employer.name}}</p>
                            <p>Name: {{employer.signatoryName}}</p>
                            <p>Title: {{employer.signatoryTitle}}</p>
                            <p>Date: {{date}}</p>
                        </div>
                        
                        <div class="signature-block">
                            <p class="signature-line">____________________________</p>
                            <p>{{employee.name}}</p>
                            <p>Employee</p>
                            <p>Date: {{date}}</p>
                        </div>
                    </div>
                </div>
                
                <div class="schedule-section">
                    <h2>SCHEDULE A - JOB DUTIES</h2>
                    <div class="duties-section">
                        {{#each position.duties}}
                        <p>• {{this}}</p>
                        {{/each}}
                    </div>
                </div>
            </div>
        ''',
        'required_fields': [
            'employer.name', 'employer.state', 'employer.address', 
            'employee.name', 'employee.address',
            'position.title', 'position.reportsTo', 'position.duties',
            'startDate', 'compensation.baseSalary', 'compensation.paymentInterval',
            'workSchedule.hours', 'workSchedule.location'
        ],
        'optional_fields': [
            'isFixedTerm', 'term', 'compensation.bonus', 'benefits',
            'nonCompete', 'employer.signatoryName', 'employer.signatoryTitle'
        ],
        'validation_rules': {
            'employer.name': r'^[A-Za-z0-9\s\-\.,&]+$',
            'employee.name': r'^[A-Za-z\s\-\'\.]+$',
            'compensation.baseSalary': r'^\$?\d+(?:,\d{3})*(?:\.\d{2})?$',
            'position.duties': {
                'min_length': 1
            }
        }
    },
    
    'Non-Disclosure Agreement': '''
        NON-DISCLOSURE AGREEMENT
        
        This agreement is made between {{disclosingParty}} ("Disclosing Party") and {{receivingParty}} ("Receiving Party").
        
        PURPOSE:
        {{purpose}}
        
        DURATION:
        {{duration}}
        
        Date: {{date}}
        Signatures:
        Disclosing Party: _________________
        Receiving Party: _________________
    ''',
    
    'Service Agreement': '''
        SERVICE AGREEMENT
        
        This agreement is made between {{serviceProvider}} ("Provider") and {{client}} ("Client").
        
        SERVICES:
        {{services}}
        
        COMPENSATION:
        {{compensation}}
        
        Date: {{date}}
        Signatures:
        Provider: _________________
        Client: _________________
    '''
}

# CSS styles for PDF documents
PDF_STYLES = '''
    <style>
        .legal-document {
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.6;
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .document-title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        
        h2 {
            font-size: 18px;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        
        .preamble {
            text-align: justify;
            margin-bottom: 25px;
        }
        
        .signature-section {
            margin-top: 50px;
        }
        
        .signature-line {
            margin-top: 30px;
            border-top: 1px solid #000;
            width: 250px;
            text-align: center;
        }
        
        .witness-section, .notary-section {
            margin-top: 40px;
            page-break-inside: avoid;
        }
        
        .witness-signatures {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }
        
        .powers-section {
            margin-left: 20px;
        }
    </style>
'''

def validate_form_data(template_name, form_data):
    """Validate form data against template requirements."""
    template_info = TEMPLATES[template_name]
    
    # Check required fields
    for field in template_info['required_fields']:
        if field not in form_data:
            return False, f"Missing required field: {field}"
    
    # Validate field formats
    if 'validation_rules' in template_info:
        import re
        for field, rule in template_info['validation_rules'].items():
            if isinstance(rule, str):  # Regex validation
                if field in form_data and not re.match(rule, str(form_data[field])):
                    return False, f"Invalid format for field: {field}"
            elif isinstance(rule, dict):  # Complex validation
                if 'min_length' in rule and len(form_data.get(field, [])) < rule['min_length']:
                    return False, f"Field {field} requires at least {rule['min_length']} items"
                if 'fields' in rule:
                    for item in form_data.get(field, []):
                        for required_field in rule['fields']:
                            if required_field not in item:
                                return False, f"Missing required subfield {required_field} in {field}"
    
    return True, None

def create_styled_paragraph(text, style='Normal'):
    styles = getSampleStyleSheet()
    return Paragraph(text, styles[style])

@contracts_bp.route('/generate', methods=['POST'])
def generate_contract():
    try:
        data = request.get_json()
        template_name = data.get('template')
        form_data = data.get('data')
        language = data.get('language', 'English')

        if not template_name or not form_data:
            return jsonify({'error': 'Missing required fields'}), 400

        # Create a temporary file to store the PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            # Create the PDF document
            doc = SimpleDocTemplate(
                tmp.name,
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
            elements.append(Paragraph(f'Language: {language}', styles['Normal']))

            # Build the PDF
            doc.build(elements)

            # Read the generated PDF
            with open(tmp.name, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

        # Clean up the temporary file
        os.unlink(tmp.name)

        # Send the PDF file
        return send_file(
            BytesIO(pdf_content),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{template_name.lower().replace("_", "-")}-{datetime.now().strftime("%Y%m%d")}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@contracts_bp.route('/templates', methods=['GET'])
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