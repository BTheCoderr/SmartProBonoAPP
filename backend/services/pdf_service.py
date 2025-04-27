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

class PDFService:
    """Service for generating PDF documents."""
    
    def __init__(self):
        # Set up Jinja2 environment for templates
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        
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
        output_format: str = 'pdf'
    ) -> str:
        """
        Generate a legal document from a template.
        
        Args:
            template_id: The ID of the template to use
            data: Dictionary containing the template variables
            output_format: Output format ('pdf' or 'html')
            
        Returns:
            str: Path to the generated file
        """
        try:
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
            
            # Generate PDF
            html = HTML(string=html_content)
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                html.write_pdf(
                    target=tmp.name,
                    stylesheets=[self.default_css],
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
                return tmp.name
                
        except Exception as e:
            raise Exception(f"Failed to generate document: {str(e)}")
    
    def add_watermark(self, html: str, watermark_text: str) -> str:
        """Add a watermark to the document."""
        watermark_css = CSS(string=f'''
            @page {{
                @bottom-center {{
                    content: "{watermark_text}";
                    font-family: Arial;
                    font-size: 9pt;
                    color: rgba(0, 0, 0, 0.3);
                }}
            }}
        ''')
        return watermark_css
    
    def add_header_footer(
        self,
        html: str,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> str:
        """Add custom header and footer to the document."""
        header_footer_css = CSS(string=f'''
            @page {{
                @top-center {{
                    content: "{header_text or ''}";
                    font-family: Arial;
                    font-size: 9pt;
                }}
                @bottom-center {{
                    content: "{footer_text or ''}";
                    font-family: Arial;
                    font-size: 9pt;
                }}
            }}
        ''')
        return header_footer_css

# Create a singleton instance
pdf_service = PDFService()

def get_pdf_service() -> PDFService:
    """Get the PDF service instance."""
    return pdf_service 