"""
PDF generation service using WeasyPrint
"""
from typing import Dict, Any, Optional, List
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Image, ListFlowable,
    ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import jinja2
from weasyprint import HTML, CSS
from docxtpl import DocxTemplate
import json
import uuid
import tempfile
import PyPDF2
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from .document_filter_service import get_document_filter_service
from reportlab.pdfgen import canvas
from io import BytesIO

class PDFService:
    """Service for generating PDF documents."""
    
    def __init__(self):
        # Set up Jinja2 environment for templates
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        self.document_filter = get_document_filter_service()
        
        # Default CSS for legal documents
        self.default_css = CSS(string='''
            @page {
                size: letter;
                margin: 2.5cm 2cm;
                @top-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                }
            }
            body {
                font-family: "Times New Roman", Times, serif;
                font-size: 12pt;
                line-height: 1.5;
            }
            .header {
                text-align: center;
                margin-bottom: 2em;
            }
            .title {
                font-size: 14pt;
                font-weight: bold;
                text-align: center;
                margin: 1em 0;
            }
            .section {
                margin: 1em 0;
            }
            .section-title {
                font-weight: bold;
                margin-bottom: 0.5em;
            }
            .signature {
                margin-top: 2em;
                page-break-inside: avoid;
            }
            .signature-line {
                border-top: 1px solid black;
                width: 50%;
                margin-top: 2em;
            }
            .footer {
                font-size: 9pt;
                text-align: center;
                margin-top: 2em;
            }
        ''')
    
    def generate_legal_document(
        self,
        template_id: str,
        data: Dict[str, Any],
        output_format: str = 'pdf',
        encryption_password: Optional[str] = None,
        watermark_text: Optional[str] = None,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        add_page_numbers: bool = True,
        confidential: bool = False
    ) -> str:
        """
        Generate a legal document from a template.
        
        Args:
            template_id: The ID of the template to use
            data: Dictionary containing the template variables
            output_format: Output format ('pdf' or 'html')
            encryption_password: Optional password to encrypt the PDF
            watermark_text: Optional watermark text to add to the document
            header_text: Optional header text to add to the document
            footer_text: Optional footer text to add to the document
            add_page_numbers: Whether to add page numbers to the document
            confidential: Whether to add a confidential stamp to the document
            
        Returns:
            str: Path to the generated file
        """
        try:
            # Validate output format
            if output_format not in ['pdf', 'html']:
                raise ValueError(f"Invalid output format: {output_format}")
                
            # Load template
            template = self.jinja_env.get_template(f'legal/{template_id}.html')
            
            # Add common variables
            context = {
                **data,
                'generated_at': datetime.utcnow(),
                'document_id': f'DOC-{uuid.uuid4().hex[:8].upper()}'
            }
            
            # Render HTML
            html_content = template.render(**context)
            
            if output_format == 'html':
                # Save HTML to temporary file
                with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                    tmp.write(html_content.encode('utf-8'))
                    return tmp.name
            
            # Prepare stylesheets
            stylesheets = [self.default_css]
            
            # Add document filters if specified
            if watermark_text:
                stylesheets.append(self.document_filter.add_watermark(watermark_text))
                
            if header_text or footer_text:
                stylesheets.append(self.document_filter.add_header_footer(header_text, footer_text))
                
            if add_page_numbers:
                stylesheets.append(self.document_filter.add_page_numbers())
                
            if confidential:
                stylesheets.append(self.document_filter.apply_confidential_stamp())
            
            # Generate PDF
            html = HTML(string=html_content)
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                html.write_pdf(
                    target=tmp.name,
                    stylesheets=stylesheets,
                    presentational_hints=True,
                    optimize_size=('fonts', 'images'),
                    metadata={
                        'title': f"Legal Document - {template_id}",
                        'author': 'SmartProBono',
                        'subject': 'Legal Document',
                        'keywords': context['document_id'],
                        'generator': 'WeasyPrint'
                    }
                )
                
                # If encryption is requested, encrypt the PDF
                if encryption_password:
                    encrypted_file_path = self.encrypt_pdf(tmp.name, encryption_password)
                    return encrypted_file_path
                    
                return tmp.name
                
        except Exception as e:
            raise Exception(f"Failed to generate document: {str(e)}")
    
    def add_watermark(self, html: str, watermark_text: str) -> CSS:
        """Add a watermark to the document."""
        return self.document_filter.add_watermark(watermark_text)
    
    def add_header_footer(
        self,
        html: str,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> CSS:
        """Add custom header and footer to the document."""
        return self.document_filter.add_header_footer(header_text, footer_text)
        
    def encrypt_pdf(self, pdf_path: str, password: str) -> str:
        """
        Encrypt a PDF file with a password using Fernet encryption.
        
        Args:
            pdf_path: Path to the PDF file to encrypt
            password: Password to use for encryption
            
        Returns:
            str: Path to the encrypted file
        """
        try:
            # Create a key derivation function
            salt = b'smartprobono_salt'  # In production, use a secure random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # Generate key from password
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            fernet = Fernet(key)
            
            # Read PDF file
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
            
            # Encrypt the data
            encrypted_data = fernet.encrypt(pdf_data)
            
            # Create output path with .enc extension
            encrypted_path = f"{pdf_path}.enc"
            
            # Write encrypted data
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
                
            return encrypted_path
        except Exception as e:
            raise Exception(f"Failed to encrypt PDF: {str(e)}")
            
    def decrypt_pdf(self, encrypted_path: str, password: str) -> str:
        """
        Decrypt an encrypted PDF file.
        
        Args:
            encrypted_path: Path to the encrypted PDF file
            password: Password used for encryption
            
        Returns:
            str: Path to the decrypted PDF file
        """
        try:
            # Create a key derivation function
            salt = b'smartprobono_salt'  # Must match the salt used for encryption
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # Generate key from password
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            fernet = Fernet(key)
            
            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Create output path (remove .enc extension)
            if encrypted_path.endswith('.enc'):
                decrypted_path = encrypted_path[:-4]
            else:
                decrypted_path = f"{encrypted_path}.decrypted.pdf"
            
            # Write decrypted data
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)
                
            return decrypted_path
        except Exception as e:
            raise Exception(f"Failed to decrypt PDF: {str(e)}")

def generate_pdf(form_type, data):
    """
    Generate a PDF document from form data.
    
    Args:
        form_type (str): Type of form to generate
        data (dict): Form data to use in generation
    
    Returns:
        bytes: Generated PDF file data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    title = form_type.replace('_', ' ').title()
    story.append(Paragraph(title, title_style))

    if form_type == 'small_claims':
        story.extend(_generate_small_claims(data, styles))
    elif form_type == 'eviction_response':
        story.extend(_generate_eviction_response(data, styles))
    elif form_type == 'fee_waiver':
        story.extend(_generate_fee_waiver(data, styles))
    else:
        raise ValueError(f'Unknown form type: {form_type}')

    # Build PDF
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def _generate_small_claims(data, styles):
    """Generate Small Claims form content."""
    story = []
    
    # Court Information
    story.append(Paragraph('Court Information', styles['Heading2']))
    court_data = [
        ['County:', data['court_county']],
        ['State:', data['court_state']],
        ['Case Number:', data.get('case_number', 'Not Assigned')]
    ]
    story.append(_create_table(court_data))
    story.append(Spacer(1, 20))
    
    # Parties
    story.append(Paragraph('Plaintiff', styles['Heading2']))
    plaintiff_data = [
        ['Name:', data['plaintiff_name']],
        ['Address:', data['plaintiff_address']]
    ]
    story.append(_create_table(plaintiff_data))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph('Defendant', styles['Heading2']))
    defendant_data = [
        ['Name:', data['defendant_name']],
        ['Address:', data['defendant_address']]
    ]
    story.append(_create_table(defendant_data))
    story.append(Spacer(1, 20))
    
    # Claim Information
    story.append(Paragraph('Claim Information', styles['Heading2']))
    claim_data = [
        ['Amount:', f"${data['claim_amount']:.2f}"],
        ['Filing Date:', data['filing_date']],
        ['Incident Date:', data['incident_date']],
        ['Incident Location:', data.get('incident_location', 'Not Specified')],
        ['Filing Fee:', f"${data.get('filing_fee', 0):.2f}"]
    ]
    story.append(_create_table(claim_data))
    story.append(Spacer(1, 20))
    
    # Claim Description
    story.append(Paragraph('Claim Description', styles['Heading2']))
    story.append(Paragraph(data['claim_description'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Facts
    story.append(Paragraph('Supporting Facts', styles['Heading2']))
    story.append(Paragraph('1. ' + data['fact_1'], styles['Normal']))
    if data.get('fact_2'):
        story.append(Paragraph('2. ' + data['fact_2'], styles['Normal']))
    if data.get('fact_3'):
        story.append(Paragraph('3. ' + data['fact_3'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Evidence and Witnesses
    if data.get('evidence_list'):
        story.append(Paragraph('Evidence', styles['Heading2']))
        story.append(Paragraph(data['evidence_list'], styles['Normal']))
        story.append(Spacer(1, 20))
    
    if data.get('witness_list'):
        story.append(Paragraph('Witnesses', styles['Heading2']))
        story.append(Paragraph(data['witness_list'], styles['Normal']))
    
    return story

def _generate_eviction_response(data, styles):
    """Generate Eviction Response form content."""
    story = []
    
    # Case Information
    story.append(Paragraph('Case Information', styles['Heading2']))
    case_data = [
        ['Case Number:', data['case_number']],
        ['Response Date:', data['response_date']]
    ]
    story.append(_create_table(case_data))
    story.append(Spacer(1, 20))
    
    # Parties
    story.append(Paragraph('Tenant Information', styles['Heading2']))
    tenant_data = [
        ['Name:', data['tenant_name']],
        ['Address:', data['tenant_address']]
    ]
    story.append(_create_table(tenant_data))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph('Landlord Information', styles['Heading2']))
    landlord_data = [
        ['Name:', data['landlord_name']],
        ['Address:', data['landlord_address']]
    ]
    story.append(_create_table(landlord_data))
    story.append(Spacer(1, 20))
    
    # Property
    story.append(Paragraph('Property Information', styles['Heading2']))
    property_data = [['Property Address:', data['property_address']]]
    story.append(_create_table(property_data))
    story.append(Spacer(1, 20))
    
    # Defense
    story.append(Paragraph('Defense Explanation', styles['Heading2']))
    story.append(Paragraph(data['defense_explanation'], styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Additional Information
    if data.get('rent_details'):
        story.append(Paragraph('Rent Details', styles['Heading2']))
        story.append(Paragraph(data['rent_details'], styles['Normal']))
        story.append(Spacer(1, 20))
    
    if data.get('maintenance_issues'):
        story.append(Paragraph('Maintenance Issues', styles['Heading2']))
        story.append(Paragraph(data['maintenance_issues'], styles['Normal']))
        story.append(Spacer(1, 20))
    
    if data.get('additional_facts'):
        story.append(Paragraph('Additional Facts', styles['Heading2']))
        story.append(Paragraph(data['additional_facts'], styles['Normal']))
    
    return story

def _generate_fee_waiver(data, styles):
    """Generate Fee Waiver form content."""
    story = []
    
    # Applicant Information
    story.append(Paragraph('Applicant Information', styles['Heading2']))
    applicant_data = [
        ['Name:', data['applicant_name']],
        ['Case Number:', data.get('case_number', 'Not Assigned')],
        ['Court Name:', data['court_name']],
        ['Filing Date:', data['filing_date']]
    ]
    story.append(_create_table(applicant_data))
    story.append(Spacer(1, 20))
    
    # Financial Information
    story.append(Paragraph('Financial Information', styles['Heading2']))
    financial_data = [
        ['Monthly Income:', f"${data['monthly_income']:.2f}"],
        ['Household Size:', str(data['household_size'])]
    ]
    story.append(_create_table(financial_data))
    story.append(Spacer(1, 20))
    
    # Public Benefits
    if data.get('public_benefits'):
        story.append(Paragraph('Public Benefits', styles['Heading2']))
        benefits_text = ', '.join(data['public_benefits'])
        story.append(Paragraph(benefits_text, styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Expenses
    if data.get('expenses'):
        story.append(Paragraph('Monthly Expenses', styles['Heading2']))
        expenses_data = [[k, f"${v:.2f}"] for k, v in data['expenses'].items()]
        story.append(_create_table(expenses_data))
        story.append(Spacer(1, 20))
    
    # Hardship Explanation
    if data.get('hardship_explanation'):
        story.append(Paragraph('Hardship Explanation', styles['Heading2']))
        story.append(Paragraph(data['hardship_explanation'], styles['Normal']))
    
    return story

def _create_table(data):
    """Create a formatted table for the PDF."""
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))
    return table

# Create a singleton instance
pdf_service = PDFService()

def get_pdf_service() -> PDFService:
    """Get the PDF service instance."""
    return pdf_service 