import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class DocumentValidationError(Exception):
    """Exception raised for document template validation errors."""
    pass

class DocumentTemplateEngine:
    """Engine for managing and generating legal document templates."""
    
    def __init__(self, templates_dir: str):
        """Initialize the template engine with templates directory."""
        self.templates_dir = templates_dir
        self.templates = self._load_templates()
        
        # Register fonts for multi-language support
        self._register_fonts()
    
    def _register_fonts(self):
        """Register custom fonts for multi-language support."""
        fonts_dir = os.path.join(os.path.dirname(self.templates_dir), 'fonts')
        if os.path.exists(fonts_dir):
            for font_file in os.listdir(fonts_dir):
                if font_file.endswith('.ttf'):
                    font_name = os.path.splitext(font_file)[0]
                    pdfmetrics.registerFont(
                        TTFont(font_name, os.path.join(fonts_dir, font_file))
                    )
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load all template definitions from the templates directory."""
        templates = {}
        definitions_dir = os.path.join(self.templates_dir, 'definitions')
        
        if not os.path.exists(definitions_dir):
            os.makedirs(definitions_dir)
            
        for filename in os.listdir(definitions_dir):
            if filename.endswith('.json'):
                with open(os.path.join(definitions_dir, filename)) as f:
                    template = json.load(f)
                    templates[template['id']] = template
        
        return templates
    
    def validate_data(self, template_id: str, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate the provided data against template requirements."""
        if template_id not in self.templates:
            raise DocumentValidationError(f"Template '{template_id}' not found")
            
        template = self.templates[template_id]
        errors = []
        
        # Check required fields
        for field in template['required_fields']:
            if field not in data or not data[field]:
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Validate field types and formats
        for field, value in data.items():
            if field in template.get('field_validations', {}):
                validation = template['field_validations'][field]
                if validation.get('type') == 'date':
                    try:
                        datetime.strptime(value, validation.get('format', '%Y-%m-%d'))
                    except ValueError:
                        errors.append(f"Invalid date format for field '{field}'")
                elif validation.get('type') == 'number':
                    try:
                        float(value)
                    except ValueError:
                        errors.append(f"Invalid number format for field '{field}'")
        
        return len(errors) == 0, errors
    
    def generate_document(self, template_id: str, data: Dict[str, Any], output_path: str) -> Dict[str, Any]:
        """Generate a PDF document from a template and data."""
        # Validate template and data
        is_valid, errors = self.validate_data(template_id, data)
        if not is_valid:
            raise DocumentValidationError('\n'.join(errors))
        
        template = self.templates[template_id]
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        normal_style = styles['Normal']
        
        # Build document content
        story = []
        
        # Add title
        story.append(Paragraph(template['name'], title_style))
        story.append(Spacer(1, 12))
        
        # Add sections
        for section in template['sections']:
            # Add section title
            story.append(Paragraph(section['title'], styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Format section content with provided data
            content = section['content']
            for field, value in data.items():
                placeholder = '{' + field + '}'
                if placeholder in content:
                    content = content.replace(placeholder, str(value))
            
            # Add formatted content
            story.append(Paragraph(content, normal_style))
            story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        # Return metadata about the generated document
        return {
            'template_id': template_id,
            'output_path': output_path,
            'timestamp': datetime.now().isoformat(),
            'fields_used': list(data.keys())
        }
    
    def get_template_fields(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata about a template's fields."""
        if template_id not in self.templates:
            return None
            
        template = self.templates[template_id]
        return {
            'id': template['id'],
            'name': template['name'],
            'required_fields': template['required_fields'],
            'optional_fields': template.get('optional_fields', []),
            'field_validations': template.get('field_validations', {})
        }
    
    def get_document_versions(self, base_filename: str) -> List[Dict[str, Any]]:
        """Get all versions of a document."""
        versions = []
        base_dir = os.path.dirname(base_filename)
        base_name = os.path.splitext(os.path.basename(base_filename))[0]
        
        # Look for versioned files
        for filename in os.listdir(base_dir):
            if filename.startswith(f"{base_name}_v") and filename.endswith('.pdf'):
                version_num = int(filename.split('_v')[1].split('.')[0])
                file_path = os.path.join(base_dir, filename)
                versions.append({
                    'version': version_num,
                    'path': file_path,
                    'filename': filename,
                    'created_at': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })
        
        # Sort by version number
        versions.sort(key=lambda x: x['version'])
        return versions
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """Get list of available templates with metadata."""
        return [
            {
                'id': template['id'],
                'name': template['name'],
                'category': template['category'],
                'description': template['description'],
                'requires_signature': template.get('requires_signature', False)
            }
            for template in self.templates.values()
        ] 