"""Document generation and handling service"""
import os
import logging
import tempfile
from datetime import datetime
import uuid
from flask import current_app, render_template
from weasyprint import HTML, CSS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from jinja2 import Template

logger = logging.getLogger(__name__)

class DocumentService:
    """Service for document generation and handling"""
    
    @staticmethod
    def render_template_with_data(template_content, data):
        """
        Render a template with provided data
        
        Args:
            template_content (str): The template content
            data (dict): The data to render the template with
            
        Returns:
            str: The rendered template
        """
        try:
            template = Template(template_content)
            return template.render(**data)
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            raise

    @staticmethod
    def generate_pdf_from_html(html_content, css_content=None):
        """
        Generate a PDF from HTML content
        
        Args:
            html_content (str): The HTML content
            css_content (str, optional): The CSS content
            
        Returns:
            bytes: The PDF content
        """
        try:
            # Create a temporary file for the PDF
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_pdf.close()
            
            # Generate PDF from HTML
            html = HTML(string=html_content)
            
            # Apply CSS if provided
            stylesheets = []
            if css_content:
                css_file = tempfile.NamedTemporaryFile(delete=False, suffix='.css')
                css_file.write(css_content.encode('utf-8'))
                css_file.close()
                stylesheets.append(CSS(filename=css_file.name))
            
            # Write PDF to temporary file
            html.write_pdf(temp_pdf.name, stylesheets=stylesheets)
            
            # Read the PDF content
            with open(temp_pdf.name, 'rb') as f:
                pdf_content = f.read()
            
            # Clean up temporary files
            os.unlink(temp_pdf.name)
            if css_content and 'css_file' in locals():
                os.unlink(css_file.name)
            
            return pdf_content
        except Exception as e:
            logger.error(f"Error generating PDF from HTML: {e}")
            # Clean up temporary files in case of error
            if 'temp_pdf' in locals() and os.path.exists(temp_pdf.name):
                os.unlink(temp_pdf.name)
            if css_content and 'css_file' in locals() and os.path.exists(css_file.name):
                os.unlink(css_file.name)
            raise

    @staticmethod
    def generate_simple_pdf(title, content, author=None):
        """
        Generate a simple PDF with basic content
        
        Args:
            title (str): The PDF title
            content (str): The PDF content
            author (str, optional): The PDF author
            
        Returns:
            bytes: The PDF content
        """
        try:
            # Create a temporary file for the PDF
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_pdf.close()
            
            # Create the PDF
            c = canvas.Canvas(temp_pdf.name, pagesize=letter)
            width, height = letter
            
            # Add metadata
            c.setTitle(title)
            if author:
                c.setAuthor(author)
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(72, height - 72, title)
            
            # Add content
            c.setFont("Helvetica", 12)
            y = height - 100
            for line in content.split('\n'):
                if y < 72:
                    c.showPage()
                    y = height - 72
                c.drawString(72, y, line)
                y -= 14
            
            # Add footer with date
            c.setFont("Helvetica", 8)
            c.drawString(72, 36, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            c.save()
            
            # Read the PDF content
            with open(temp_pdf.name, 'rb') as f:
                pdf_content = f.read()
            
            # Clean up temporary file
            os.unlink(temp_pdf.name)
            
            return pdf_content
        except Exception as e:
            logger.error(f"Error generating simple PDF: {e}")
            # Clean up temporary file in case of error
            if 'temp_pdf' in locals() and os.path.exists(temp_pdf.name):
                os.unlink(temp_pdf.name)
            raise

    @staticmethod
    def get_template(template_id):
        """
        Get a document template by ID
        
        Args:
            template_id (str): The template ID
            
        Returns:
            dict: The template data
        """
        # In a real app, this would fetch from a database
        templates = {
            "fee_waiver": {
                "id": "fee_waiver",
                "name": "Fee Waiver Application",
                "html_template": """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Fee Waiver Application</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        h1 { text-align: center; }
                        .section { margin-top: 20px; }
                        .field { margin-bottom: 10px; }
                        .label { font-weight: bold; }
                    </style>
                </head>
                <body>
                    <h1>APPLICATION FOR WAIVER OF COURT FEES</h1>
                    
                    <div class="section">
                        <h2>Personal Information</h2>
                        <div class="field">
                            <span class="label">Full Name:</span> {{ full_name }}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Case Information</h2>
                        <div class="field">
                            <span class="label">Case Number:</span> {{ case_number or 'N/A' }}
                        </div>
                        <div class="field">
                            <span class="label">Court Name:</span> {{ court_name }}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Financial Information</h2>
                        <div class="field">
                            <span class="label">Monthly Income:</span> ${{ monthly_income }}
                        </div>
                        <div class="field">
                            <span class="label">Household Size:</span> {{ household_size }}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Declaration</h2>
                        <p>I declare under penalty of perjury that the information provided above is true and correct.</p>
                        <div class="field" style="margin-top: 50px;">
                            <span class="label">Signature:</span> _______________________________
                        </div>
                        <div class="field">
                            <span class="label">Date:</span> {{ now().strftime('%Y-%m-%d') }}
                        </div>
                    </div>
                </body>
                </html>
                """
            },
            "housing_defense": {
                "id": "housing_defense",
                "name": "Housing Defense Letter",
                "html_template": """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Housing Defense Letter</title>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.5; }
                        .date { text-align: right; margin-bottom: 20px; }
                        .header { font-weight: bold; margin-bottom: 20px; }
                        .closing { margin-top: 30px; }
                        .signature { margin-top: 50px; }
                    </style>
                </head>
                <body>
                    <div class="date">{{ now().strftime('%B %d, %Y') }}</div>
                    
                    <div class="header">
                        {{ landlord_name }}<br>
                        [Landlord Address]<br>
                        Re: {{ address }}
                    </div>
                    
                    <p>Dear {{ landlord_name }},</p>
                    
                    <p>I am writing regarding the property at {{ address }}.</p>
                    
                    <p>{{ issue_description }}</p>
                    
                    <p>{{ requested_remedy }}</p>
                    
                    <p>Please respond to this letter within 14 days. I hope we can resolve this matter amicably.</p>
                    
                    <div class="closing">
                        Sincerely,
                    </div>
                    
                    <div class="signature">
                        {{ tenant_name }}
                    </div>
                </body>
                </html>
                """
            },
            "expungement_petition": {
                "id": "expungement_petition",
                "name": "Expungement Petition",
                "html_template": """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Petition for Expungement</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        h1 { text-align: center; }
                        .court-info { text-align: center; margin-bottom: 30px; }
                        .section { margin-top: 20px; }
                        .field { margin-bottom: 10px; }
                        .label { font-weight: bold; }
                        .signature { margin-top: 50px; }
                    </style>
                </head>
                <body>
                    <div class="court-info">
                        [COURT NAME]<br>
                        [COURT ADDRESS]
                    </div>
                    
                    <h1>PETITION FOR EXPUNGEMENT OF CRIMINAL RECORD</h1>
                    
                    <div class="section">
                        <h2>Petitioner Information</h2>
                        <div class="field">
                            <span class="label">Name:</span> {{ petitioner_name }}
                        </div>
                        <div class="field">
                            <span class="label">Date of Birth:</span> {{ dob }}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Case Information</h2>
                        <div class="field">
                            <span class="label">Case Number:</span> {{ case_number }}
                        </div>
                        <div class="field">
                            <span class="label">Conviction Date:</span> {{ conviction_date }}
                        </div>
                        <div class="field">
                            <span class="label">Offense:</span> {{ offense }}
                        </div>
                        <div class="field">
                            <span class="label">Date Sentence Completed:</span> {{ sentence_completed }}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>Statement of Reasons</h2>
                        <p>{{ reason_for_expungement }}</p>
                    </div>
                    
                    <div class="section">
                        <p>I hereby petition the court to expunge the above criminal record and declare under penalty of perjury that the foregoing is true and correct.</p>
                    </div>
                    
                    <div class="signature">
                        <div class="field">
                            <span class="label">Signature:</span> _______________________________
                        </div>
                        <div class="field">
                            <span class="label">Date:</span> {{ now().strftime('%Y-%m-%d') }}
                        </div>
                    </div>
                </body>
                </html>
                """
            }
        }
        
        return templates.get(template_id)


# Create context functions for templates
def now():
    """Return current datetime for use in templates"""
    return datetime.now()


def generate_document(template_id, data, format='pdf'):
    """
    Generate a document from a template with provided data
    
    Args:
        template_id (str): The template ID
        data (dict): The data to render the template with
        format (str): The output format (pdf or html)
        
    Returns:
        dict: The generated document info
    """
    try:
        # Get the template
        template = DocumentService.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Add helper functions to template data
        template_data = {**data, 'now': now}
        
        # Render the template
        html_content = DocumentService.render_template_with_data(template['html_template'], template_data)
        
        # Generate document ID
        document_id = f"doc_{uuid.uuid4().hex[:10]}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create appropriate output based on format
        if format == 'html':
            # Return HTML content
            return {
                'id': document_id,
                'template_id': template_id,
                'format': 'html',
                'content': html_content,
                'filename': f"{template_id}_{datetime.now().strftime('%Y%m%d')}.html",
                'generated_at': datetime.now().isoformat()
            }
        else:
            # Generate PDF
            pdf_content = DocumentService.generate_pdf_from_html(html_content)
            
            # In a real app, you'd save this PDF to a file or database
            # For now, save to a temporary file for demo purposes
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, f"{document_id}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf_content)
                
            return {
                'id': document_id,
                'template_id': template_id,
                'format': 'pdf',
                'path': pdf_path,
                'filename': f"{template_id}_{datetime.now().strftime('%Y%m%d')}.pdf",
                'generated_at': datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error generating document: {str(e)}")
        raise

def generate_pdf(document_id, format='pdf'):
    """
    Generate or retrieve a PDF document
    
    Args:
        document_id (str): The document ID
        format (str): The output format
        
    Returns:
        str: The path to the generated PDF
    """
    # In a real app, you would retrieve the saved document
    # For demo purposes, we'll create a simple PDF
    
    try:
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"{document_id}.pdf")
        
        # Check if the file already exists (from previous generate_document call)
        if os.path.exists(pdf_path):
            return pdf_path
            
        # Generate a simple PDF
        pdf_content = DocumentService.generate_simple_pdf(
            title=f"Document {document_id}",
            content=f"This is a demonstration PDF for document ID: {document_id}\n\nGenerated for testing purposes.",
            author="SmartProBono System"
        )
        
        # Save to file
        with open(pdf_path, 'wb') as f:
            f.write(pdf_content)
            
        return pdf_path
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise

# Create a singleton instance
document_service = DocumentService() 