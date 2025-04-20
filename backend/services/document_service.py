"""
Document service for template management and document generation.

This service provides functionality for:
- Creating, updating, and managing document templates
- Creating and managing template versions
- Generating documents from templates
- Retrieving and deleting documents
"""

import os
import uuid
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from jinja2 import Template, TemplateSyntaxError, StrictUndefined
from weasyprint import HTML

from backend.models.document_template import (
    DocumentTemplate, DocumentTemplateVersion, GeneratedDocument, DocumentStatus
)
from backend.models.database import db
from backend.services.file_storage_service import FileStorageService

# Configure logging
logger = logging.getLogger(__name__)

class DocumentService:
    """Service for document template management and document generation."""
    
    @staticmethod
    def create_template(
        title: str,
        description: str,
        category: str,
        content: str,
        field_schema: Dict[str, Any],
        created_by: uuid.UUID
    ) -> Tuple[Optional[DocumentTemplate], Optional[str]]:
        """
        Create a new document template with an initial version.
        
        Args:
            title: Template title
            description: Template description
            category: Template category
            content: Initial template content
            field_schema: JSON schema for template fields
            created_by: User ID of creator
            
        Returns:
            Tuple of (template, error_message)
        """
        try:
            # Validate template syntax
            try:
                # Parse the template to check for syntax errors
                Template(content, undefined=StrictUndefined)
            except TemplateSyntaxError as e:
                return None, f"Template syntax error: {str(e)}"
            
            # Start a transaction
            new_template = DocumentTemplate(
                title=title,
                description=description,
                category=category,
                is_published=False,
                created_by=created_by
            )
            
            db.session.add(new_template)
            db.session.flush()  # Get the template ID
            
            # Create initial version
            new_version = DocumentTemplateVersion(
                template_id=new_template.id,
                version_number=1,
                content=content,
                field_schema=field_schema,
                created_by=created_by,
                is_current=True
            )
            
            db.session.add(new_version)
            db.session.flush()
            
            # Set the current version
            new_template.current_version_id = new_version.id
            
            db.session.commit()
            logger.info(f"Created template {new_template.id} with initial version {new_version.id}")
            
            return new_template, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating template: {str(e)}")
            return None, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating template: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def update_template(
        template_id: uuid.UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        is_published: Optional[bool] = None
    ) -> Tuple[Optional[DocumentTemplate], Optional[str]]:
        """
        Update a document template's metadata (not content).
        
        Args:
            template_id: ID of template to update
            title: New title (if changing)
            description: New description (if changing)
            category: New category (if changing)
            is_published: New published status (if changing)
            
        Returns:
            Tuple of (updated_template, error_message)
        """
        try:
            template = DocumentTemplate.query.get(template_id)
            if not template:
                return None, f"Template with ID {template_id} not found"
            
            # Update fields if provided
            if title is not None:
                template.title = title
            
            if description is not None:
                template.description = description
            
            if category is not None:
                template.category = category
            
            if is_published is not None:
                template.is_published = is_published
            
            # Update timestamp
            template.updated_at = datetime.utcnow()
            
            db.session.commit()
            logger.info(f"Updated template {template_id}")
            
            return template, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error updating template: {str(e)}")
            return None, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating template: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def create_template_version(
        template_id: uuid.UUID,
        content: str,
        field_schema: Dict[str, Any],
        created_by: uuid.UUID,
        set_as_current: bool = True
    ) -> Tuple[Optional[DocumentTemplateVersion], Optional[str]]:
        """
        Create a new version for an existing template.
        
        Args:
            template_id: ID of the template
            content: New template content
            field_schema: New field schema
            created_by: User ID of creator
            set_as_current: Whether to set this as the current version
            
        Returns:
            Tuple of (version, error_message)
        """
        try:
            # Check if template exists
            template = DocumentTemplate.query.get(template_id)
            if not template:
                return None, f"Template with ID {template_id} not found"
            
            # Validate template syntax
            try:
                # Parse the template to check for syntax errors
                Template(content, undefined=StrictUndefined)
            except TemplateSyntaxError as e:
                return None, f"Template syntax error: {str(e)}"
            
            # Get highest version number
            latest_version = DocumentTemplateVersion.query.filter_by(
                template_id=template_id
            ).order_by(DocumentTemplateVersion.version_number.desc()).first()
            
            new_version_number = 1
            if latest_version:
                new_version_number = latest_version.version_number + 1
            
            # Create new version
            new_version = DocumentTemplateVersion(
                template_id=template_id,
                version_number=new_version_number,
                content=content,
                field_schema=field_schema,
                created_by=created_by,
                is_current=set_as_current
            )
            
            db.session.add(new_version)
            
            # Update current version if requested
            if set_as_current:
                # First set all existing versions to not current
                DocumentTemplateVersion.query.filter_by(
                    template_id=template_id,
                    is_current=True
                ).update({"is_current": False})
                
                # Then set the template's current version
                template.current_version_id = new_version.id
                template.updated_at = datetime.utcnow()
            
            db.session.commit()
            logger.info(f"Created version {new_version.id} for template {template_id}")
            
            return new_version, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating template version: {str(e)}")
            return None, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating template version: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def get_templates(
        category: Optional[str] = None,
        is_published: Optional[bool] = None,
        created_by: Optional[uuid.UUID] = None
    ) -> List[DocumentTemplate]:
        """
        Get templates with optional filtering.
        
        Args:
            category: Filter by category
            is_published: Filter by published status
            created_by: Filter by creator
            
        Returns:
            List of matching templates
        """
        query = DocumentTemplate.query
        
        if category is not None:
            query = query.filter(DocumentTemplate.category == category)
        
        if is_published is not None:
            query = query.filter(DocumentTemplate.is_published == is_published)
        
        if created_by is not None:
            query = query.filter(DocumentTemplate.created_by == created_by)
        
        return query.order_by(DocumentTemplate.title).all()

    @staticmethod
    def get_template_by_id(template_id: uuid.UUID) -> Optional[DocumentTemplate]:
        """Get a template by ID."""
        return DocumentTemplate.query.get(template_id)

    @staticmethod
    def get_template_version_by_id(version_id: uuid.UUID) -> Optional[DocumentTemplateVersion]:
        """Get a template version by ID."""
        return DocumentTemplateVersion.query.get(version_id)

    @staticmethod
    def generate_document(
        template_version_id: uuid.UUID,
        field_values: Dict[str, Any],
        title: str,
        created_by: uuid.UUID,
        case_id: Optional[uuid.UUID] = None,
        generate_file: bool = False,
        file_format: str = 'pdf'
    ) -> Tuple[Optional[GeneratedDocument], Optional[str]]:
        """
        Generate a document from a template version.
        
        Args:
            template_version_id: ID of the template version
            field_values: Values for the template fields
            title: Title for the generated document
            created_by: User ID of creator
            case_id: Optional case ID to associate with
            generate_file: Whether to generate and store a file
            file_format: Format for generated file ('pdf' or 'html')
            
        Returns:
            Tuple of (document, error_message)
        """
        try:
            # Get the template version
            version = DocumentTemplateVersion.query.get(template_version_id)
            if not version:
                return None, f"Template version with ID {template_version_id} not found"
            
            # Validate field values against schema
            # This would be more sophisticated in a real implementation
            schema = version.field_schema
            required_fields = schema.get('required', [])
            for field in required_fields:
                if field not in field_values:
                    return None, f"Missing required field: {field}"
            
            # Render the template
            try:
                template = Template(version.content)
                rendered_content = template.render(**field_values)
            except TemplateSyntaxError as e:
                return None, f"Template syntax error: {str(e)}"
            except Exception as e:
                return None, f"Error rendering template: {str(e)}"
            
            # Generate file if requested
            file_path = None
            if generate_file:
                try:
                    # Generate appropriate filename
                    filename = f"{title.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
                    file_path = DocumentService._generate_document_file(
                        rendered_content, 
                        filename,
                        file_format
                    )
                except Exception as e:
                    logger.error(f"Error generating document file: {str(e)}")
                    return None, f"Error generating document file: {str(e)}"
            
            # Create document record
            document = GeneratedDocument(
                title=title,
                template_version_id=template_version_id,
                field_values=field_values,
                file_path=file_path,
                file_format=file_format if file_path else None,
                status=DocumentStatus.DRAFT,
                created_by=created_by,
                case_id=case_id
            )
            
            db.session.add(document)
            db.session.commit()
            
            logger.info(f"Generated document {document.id} from template version {template_version_id}")
            return document, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error generating document: {str(e)}")
            return None, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error generating document: {str(e)}")
            return None, f"Error: {str(e)}"

    @staticmethod
    def _generate_document_file(content: str, filename: str, format: str) -> str:
        """
        Generate a document file from rendered content.
        
        Args:
            content: Rendered HTML content
            filename: Base filename (without extension)
            format: File format ('pdf' or 'html')
            
        Returns:
            Path to the generated file
        """
        # This is a stub implementation
        # In a real app, this would use PDF generation libraries
        # or save HTML to a file storage service
        
        # For now, we'll just return a placeholder path
        return f"/path/to/documents/{filename}.{format}"

    @staticmethod
    def get_document_by_id(document_id: uuid.UUID) -> Optional[GeneratedDocument]:
        """Get a generated document by ID."""
        return GeneratedDocument.query.get(document_id)

    @staticmethod
    def get_documents_for_case(case_id: uuid.UUID) -> List[GeneratedDocument]:
        """Get all documents associated with a case."""
        return GeneratedDocument.query.filter_by(case_id=case_id).order_by(
            GeneratedDocument.created_at.desc()
        ).all()

    @staticmethod
    def delete_template(template_id: uuid.UUID) -> Tuple[bool, Optional[str]]:
        """
        Delete a document template and all its versions.
        
        Args:
            template_id: ID of the template to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            template = DocumentTemplate.query.get(template_id)
            if not template:
                return False, f"Template with ID {template_id} not found"
            
            # Delete all versions (should cascade, but being explicit)
            DocumentTemplateVersion.query.filter_by(template_id=template_id).delete()
            
            # Delete the template
            db.session.delete(template)
            db.session.commit()
            
            logger.info(f"Deleted template {template_id}")
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error deleting template: {str(e)}")
            return False, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting template: {str(e)}")
            return False, f"Error: {str(e)}"

    @staticmethod
    def delete_document(document_id: uuid.UUID) -> Tuple[bool, Optional[str]]:
        """
        Delete a generated document.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            document = GeneratedDocument.query.get(document_id)
            if not document:
                return False, f"Document with ID {document_id} not found"
            
            # Delete the file if it exists
            if document.file_path:
                try:
                    # In a real implementation, this would use a file storage service
                    # to delete the actual file
                    pass
                except Exception as e:
                    logger.warning(f"Error deleting document file: {str(e)}")
                    # Continue with database deletion even if file deletion fails
            
            # Delete the document record
            db.session.delete(document)
            db.session.commit()
            
            logger.info(f"Deleted document {document_id}")
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error deleting document: {str(e)}")
            return False, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting document: {str(e)}")
            return False, f"Error: {str(e)}" 