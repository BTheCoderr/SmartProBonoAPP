"""
Document template service for SmartProBono.

This service handles the creation, retrieval, and rendering of document templates.
"""
import os
import json
import re
import logging
import tempfile
import markdown
import jinja2
from typing import Dict, List, Any, Optional, Tuple, Union
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from weasyprint import HTML

from models.database import db
from models.document_template import DocumentTemplate, GeneratedDocument, TemplateCategory

# Configure logging
logger = logging.getLogger(__name__)

class DocumentTemplateService:
    """Service for working with document templates and generating documents."""
    
    @staticmethod
    def create_template(
        title: str,
        content: str,
        field_schema: Dict[str, Any],
        category: str,
        created_by: UUID,
        description: str = None,
        metadata: Dict[str, Any] = None,
        is_published: bool = True
    ) -> DocumentTemplate:
        """
        Create a new document template.
        
        Args:
            title: Title of the template
            content: HTML/Markdown content with variable placeholders
            field_schema: JSON schema defining the fields/variables
            category: Category of the template
            created_by: ID of the user creating the template
            description: Optional description of the template
            metadata: Optional additional metadata
            is_published: Whether the template is published
            
        Returns:
            Newly created DocumentTemplate
        """
        try:
            # Validate the template
            DocumentTemplateService._validate_template(content, field_schema)
            
            template = DocumentTemplate(
                title=title,
                content=content,
                field_schema=field_schema,
                category=TemplateCategory[category.upper()],
                created_by=created_by,
                description=description,
                metadata=metadata,
                is_published=is_published
            )
            
            db.session.add(template)
            db.session.commit()
            
            logger.info(f"Created new document template: {template.id}")
            return template
        
        except ValueError as e:
            logger.error(f"Validation error creating template: {str(e)}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating template: {str(e)}")
            raise ValueError(f"Failed to create template: {str(e)}")
    
    @staticmethod
    def update_template(
        template_id: UUID,
        updated_by: UUID,
        **update_data
    ) -> DocumentTemplate:
        """
        Update an existing template creating a new version.
        
        Args:
            template_id: ID of the template to update
            updated_by: ID of the user making the update
            update_data: Data to update (title, content, field_schema, etc.)
            
        Returns:
            Updated DocumentTemplate
        """
        try:
            old_template = DocumentTemplate.query.get(template_id)
            if not old_template:
                raise ValueError(f"Template with ID {template_id} not found")
            
            # If content or field_schema is updated, validate them
            if 'content' in update_data and 'field_schema' in update_data:
                DocumentTemplateService._validate_template(
                    update_data['content'], 
                    update_data['field_schema']
                )
            elif 'content' in update_data:
                DocumentTemplateService._validate_template(
                    update_data['content'], 
                    old_template.field_schema
                )
            elif 'field_schema' in update_data:
                DocumentTemplateService._validate_template(
                    old_template.content, 
                    update_data['field_schema']
                )
            
            # Create a new version
            new_template = DocumentTemplate(
                title=update_data.get('title', old_template.title),
                content=update_data.get('content', old_template.content),
                field_schema=update_data.get('field_schema', old_template.field_schema),
                category=TemplateCategory[update_data.get('category', old_template.category.name).upper()] 
                    if 'category' in update_data else old_template.category,
                created_by=updated_by,
                description=update_data.get('description', old_template.description),
                metadata=update_data.get('metadata', old_template.metadata),
                is_published=update_data.get('is_published', old_template.is_published),
                version=old_template.version + 1,
                parent_template_id=old_template.id
            )
            
            db.session.add(new_template)
            
            # Mark old template as not published if the new one is published
            if new_template.is_published:
                old_template.is_published = False
                
            db.session.commit()
            
            logger.info(f"Updated template {template_id}, created new version: {new_template.id}")
            return new_template
            
        except ValueError as e:
            logger.error(f"Validation error updating template: {str(e)}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error updating template: {str(e)}")
            raise ValueError(f"Failed to update template: {str(e)}")
    
    @staticmethod
    def get_template(template_id: UUID) -> Optional[DocumentTemplate]:
        """Get a document template by ID."""
        return DocumentTemplate.query.get(template_id)
    
    @staticmethod
    def get_templates(
        category: str = None,
        published_only: bool = True,
        user_id: UUID = None,
        search_term: str = None
    ) -> List[DocumentTemplate]:
        """
        Get document templates with optional filtering.
        
        Args:
            category: Optional category to filter by
            published_only: Whether to only include published templates
            user_id: Optional user ID to filter by (templates created by user)
            search_term: Optional search term for title and description
            
        Returns:
            List of matching DocumentTemplate objects
        """
        query = DocumentTemplate.query
        
        if published_only:
            query = query.filter(DocumentTemplate.is_published == True)
            
        if category:
            try:
                category_enum = TemplateCategory[category.upper()]
                query = query.filter(DocumentTemplate.category == category_enum)
            except KeyError:
                logger.warning(f"Invalid category: {category}")
                # Return empty list for invalid category
                return []
                
        if user_id:
            query = query.filter(DocumentTemplate.created_by == user_id)
            
        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(
                (DocumentTemplate.title.ilike(search_filter)) | 
                (DocumentTemplate.description.ilike(search_filter))
            )
            
        # Get latest versions
        query = query.order_by(DocumentTemplate.version.desc())
        
        return query.all()
    
    @staticmethod
    def generate_document(
        template_id: UUID,
        field_values: Dict[str, Any],
        user_id: UUID,
        title: str = None,
        case_id: UUID = None,
        format: str = 'html'
    ) -> Union[GeneratedDocument, Tuple[GeneratedDocument, str]]:
        """
        Generate a document from a template with provided field values.
        
        Args:
            template_id: ID of the template to use
            field_values: Values for the template variables
            user_id: ID of the user generating the document
            title: Optional title for the generated document
            case_id: Optional ID of the case to associate with
            format: Output format ('html', 'pdf', 'md')
            
        Returns:
            GeneratedDocument record and file path if applicable
        """
        try:
            template = DocumentTemplate.query.get(template_id)
            if not template:
                raise ValueError(f"Template with ID {template_id} not found")
            
            # Validate field values against schema
            DocumentTemplateService._validate_field_values(field_values, template.field_schema)
            
            # Render the template
            rendered_content = DocumentTemplateService._render_template(
                template.content, 
                field_values
            )
            
            # Set a default title if not provided
            if not title:
                title = f"{template.title} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Create the generated document record
            document = GeneratedDocument(
                template_id=template_id,
                title=title,
                field_values=field_values,
                content=rendered_content,
                created_by=user_id,
                case_id=case_id
            )
            
            db.session.add(document)
            db.session.commit()
            
            # Generate file if requested
            file_path = None
            if format == 'pdf':
                file_path = DocumentTemplateService._generate_pdf(
                    rendered_content, 
                    document.id
                )
                document.document_path = file_path
                db.session.commit()
                
            logger.info(f"Generated document {document.id} from template {template_id}")
            
            if file_path:
                return document, file_path
            return document
            
        except ValueError as e:
            logger.error(f"Validation error generating document: {str(e)}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error generating document: {str(e)}")
            raise ValueError(f"Failed to generate document: {str(e)}")
    
    @staticmethod
    def _validate_template(content: str, field_schema: Dict[str, Any]) -> bool:
        """
        Validate that a template's content and field schema are compatible.
        
        Args:
            content: Template content with variables
            field_schema: JSON schema defining the variables
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        # Extract variables from content
        variables = set(re.findall(r'{{\s*(\w+)\s*}}', content))
        
        # Check for required variables in schema
        schema_fields = set(field_schema.get('properties', {}).keys())
        schema_required = set(field_schema.get('required', []))
        
        # Check that all required fields are in the content
        missing_vars = schema_required - variables
        if missing_vars:
            raise ValueError(f"Template content missing required variables: {missing_vars}")
            
        # Check that all variables in content are defined in schema
        undefined_vars = variables - schema_fields
        if undefined_vars:
            raise ValueError(f"Template content contains undefined variables: {undefined_vars}")
            
        return True
    
    @staticmethod
    def _validate_field_values(field_values: Dict[str, Any], field_schema: Dict[str, Any]) -> bool:
        """
        Validate field values against the schema.
        
        Args:
            field_values: Values for the template variables
            field_schema: JSON schema defining the variables
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        # Check for required fields
        schema_required = set(field_schema.get('required', []))
        provided_fields = set(field_values.keys())
        
        missing_fields = schema_required - provided_fields
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
            
        # Validate field types (basic validation)
        properties = field_schema.get('properties', {})
        for field_name, field_value in field_values.items():
            if field_name not in properties:
                raise ValueError(f"Unknown field: {field_name}")
                
            field_type = properties[field_name].get('type')
            
            # Simple type checking
            if field_type == 'string' and not isinstance(field_value, str):
                raise ValueError(f"Field {field_name} should be a string")
            elif field_type == 'number' and not isinstance(field_value, (int, float)):
                raise ValueError(f"Field {field_name} should be a number")
            elif field_type == 'boolean' and not isinstance(field_value, bool):
                raise ValueError(f"Field {field_name} should be a boolean")
                
        return True
    
    @staticmethod
    def _render_template(content: str, field_values: Dict[str, Any]) -> str:
        """
        Render a template with the provided values.
        
        Args:
            content: Template content with variables
            field_values: Values for the template variables
            
        Returns:
            Rendered template content
        """
        # Create a Jinja2 environment
        env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=True
        )
        
        # Parse template
        template = env.from_string(content)
        
        # Render with provided values
        rendered = template.render(**field_values)
        
        return rendered
    
    @staticmethod
    def _generate_pdf(html_content: str, document_id: UUID) -> str:
        """
        Generate a PDF file from HTML content.
        
        Args:
            html_content: HTML content to convert
            document_id: ID of the document for file naming
            
        Returns:
            Path to the generated PDF file
        """
        try:
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join('uploads', 'documents')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Define output file path
            file_path = os.path.join(upload_dir, f"document_{document_id}.pdf")
            
            # Convert HTML to PDF
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp:
                temp.write(html_content.encode('utf-8'))
                temp_path = temp.name
            
            # Generate PDF with WeasyPrint
            HTML(filename=temp_path).write_pdf(file_path)
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise ValueError(f"Failed to generate PDF: {str(e)}")
    
    @staticmethod
    def get_template_fields(template_id: UUID) -> Dict[str, Any]:
        """
        Get the field schema for a template.
        
        Args:
            template_id: ID of the template
            
        Returns:
            Field schema from the template
        """
        template = DocumentTemplate.query.get(template_id)
        if not template:
            raise ValueError(f"Template with ID {template_id} not found")
            
        return template.field_schema 