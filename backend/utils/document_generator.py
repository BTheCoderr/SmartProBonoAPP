"""
Document Generator Utility for SmartProBono

This module provides functions to generate documents from templates.
It supports HTML templates with Jinja2 and conversion to PDF.
"""
import os
import uuid
from datetime import datetime
import jinja2
import pdfkit
from flask import current_app
import logging

# Set up logging
logger = logging.getLogger(__name__)

class DocumentGenerator:
    """Class for generating documents from templates"""
    
    def __init__(self, templates_dir=None):
        """Initialize with templates directory"""
        self.templates_dir = templates_dir or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'templates'
        )
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir)
        )
        
    def list_templates(self):
        """List all available templates"""
        try:
            templates = []
            for filename in os.listdir(self.templates_dir):
                if filename.endswith(('.html', '.txt')):
                    templates.append({
                        'id': os.path.splitext(filename)[0],
                        'name': os.path.splitext(filename)[0].replace('_', ' ').title(),
                        'filename': filename,
                        'type': os.path.splitext(filename)[1][1:].upper()
                    })
            return templates
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            return []

    def render_template(self, template_name, context=None):
        """Render a template with the given context"""
        try:
            if not template_name.endswith(('.html', '.txt')):
                template_name += '.html'
                
            template = self.env.get_template(template_name)
            context = context or {}
            
            # Add common template variables
            context.update({
                'current_date': datetime.now().strftime('%B %d, %Y'),
                'document_id': str(uuid.uuid4())[:8].upper()
            })
            
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {str(e)}")
            raise ValueError(f"Failed to render template: {str(e)}")

    def generate_pdf(self, html_content, output_path=None):
        """Generate PDF from HTML content"""
        try:
            output_path = output_path or os.path.join(
                current_app.config.get('DOCUMENT_UPLOAD_FOLDER', '/tmp'),
                f"document_{uuid.uuid4()}.pdf"
            )
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert HTML to PDF
            options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8',
                'no-outline': None
            }
            
            pdfkit.from_string(html_content, output_path, options=options)
            return output_path
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise ValueError(f"Failed to generate PDF: {str(e)}")

    def generate_document(self, template_name, context=None, output_format='pdf'):
        """Generate document from template with context"""
        try:
            html_content = self.render_template(template_name, context)
            
            if output_format.lower() == 'html':
                return html_content
                
            elif output_format.lower() == 'pdf':
                return self.generate_pdf(html_content)
                
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
                
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}")
            raise ValueError(f"Failed to generate document: {str(e)}")

# Create a singleton instance
document_generator = DocumentGenerator()

def render_template(template_name, context=None):
    """Convenience function to render a template"""
    return document_generator.render_template(template_name, context)

def generate_document(template_name, context=None, output_format='pdf'):
    """Convenience function to generate a document"""
    return document_generator.generate_document(template_name, context, output_format)

def list_templates():
    """Convenience function to list available templates"""
    return document_generator.list_templates() 