"""
Document template models for SmartProBono.

These models represent:
- DocumentTemplate: Main template definition
- DocumentTemplateVersion: Versions of a template with content and field schema
- GeneratedDocument: Documents generated from templates
"""
from datetime import datetime
import enum
import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.models.base import Base


class DocumentStatus(enum.Enum):
    """Status values for generated documents."""
    DRAFT = "draft"
    FINAL = "final"
    ARCHIVED = "archived"


class DocumentTemplate(Base):
    """Document template model."""
    __tablename__ = "document_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    current_version_id = Column(UUID(as_uuid=True), ForeignKey("document_template_versions.id"), nullable=True)

    # Relationships
    versions = relationship("DocumentTemplateVersion", 
                          foreign_keys="DocumentTemplateVersion.template_id",
                          back_populates="template",
                          cascade="all, delete-orphan")
    current_version = relationship("DocumentTemplateVersion", 
                                 foreign_keys=[current_version_id],
                                 post_update=True)
    created_by_user = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<DocumentTemplate {self.id}: {self.title}>"


class DocumentTemplateVersion(Base):
    """Document template version model."""
    __tablename__ = "document_template_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("document_templates.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)  # Template content with placeholders
    field_schema = Column(JSON, nullable=False)  # JSON schema for template fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_current = Column(Boolean, default=False, nullable=False)

    # Relationships
    template = relationship("DocumentTemplate", 
                          foreign_keys=[template_id], 
                          back_populates="versions")
    created_by_user = relationship("User", foreign_keys=[created_by])
    generated_documents = relationship("GeneratedDocument", 
                                     back_populates="template_version", 
                                     cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DocumentTemplateVersion {self.id}: v{self.version_number} ({self.template_id})>"


class GeneratedDocument(Base):
    """Generated document model."""
    __tablename__ = "generated_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    template_version_id = Column(UUID(as_uuid=True), ForeignKey("document_template_versions.id"), nullable=False)
    field_values = Column(JSON, nullable=False)  # Values used to generate the document
    file_path = Column(String(1024), nullable=True)  # Path to the generated file, if any
    file_format = Column(String(10), nullable=True)  # e.g., pdf, docx
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=True)

    # Relationships
    template_version = relationship("DocumentTemplateVersion", back_populates="generated_documents")
    created_by_user = relationship("User", foreign_keys=[created_by])
    case = relationship("Case", back_populates="generated_documents")

    def __repr__(self):
        return f"<GeneratedDocument {self.id}: {self.title} ({self.status.value})>" 