"""
Marshmallow schemas for document management.

These schemas handle serialization/deserialization for:
- Document templates
- Template versions
- Generated documents
"""

from marshmallow import Schema, fields, validate, EXCLUDE


class DocumentTemplateSchema(Schema):
    """Schema for document templates."""
    class Meta:
        unknown = EXCLUDE
    
    id = fields.UUID(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    category = fields.String(required=True)
    is_published = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by = fields.UUID(dump_only=True)
    current_version_id = fields.UUID(dump_only=True)


class DocumentTemplateVersionSchema(Schema):
    """Schema for document template versions."""
    class Meta:
        unknown = EXCLUDE
    
    id = fields.UUID(dump_only=True)
    template_id = fields.UUID(required=True)
    version_number = fields.Integer(dump_only=True)
    content = fields.String(required=True)
    field_schema = fields.Dict(required=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.UUID(dump_only=True)
    is_current = fields.Boolean(dump_only=True)


class GeneratedDocumentSchema(Schema):
    """Schema for generated documents."""
    class Meta:
        unknown = EXCLUDE
    
    id = fields.UUID(dump_only=True)
    title = fields.String(required=True)
    template_version_id = fields.UUID(required=True)
    field_values = fields.Dict(required=True)
    file_path = fields.String(dump_only=True)
    file_format = fields.String()
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    created_by = fields.UUID(dump_only=True)
    case_id = fields.UUID()


# Create schema instances
template_schema = DocumentTemplateSchema()
template_list_schema = DocumentTemplateSchema(many=True)
version_schema = DocumentTemplateVersionSchema()
version_list_schema = DocumentTemplateVersionSchema(many=True)
document_schema = GeneratedDocumentSchema()
document_list_schema = GeneratedDocumentSchema(many=True) 