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

# Create a singleton instance
pdf_service = PDFService()

def get_pdf_service() -> PDFService:
    """Get the PDF service instance."""
    return pdf_service 