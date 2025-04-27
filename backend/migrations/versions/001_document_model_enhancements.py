"""Add document model enhancements

Revision ID: 001_document_model_enhancements
Revises: 
Create Date: 2024-05-17

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '001_document_model_enhancements'
down_revision = None  # Update this to the previous migration if needed
branch_labels = None
depends_on = None


def upgrade():
    # Add content column for storing document content/HTML
    op.add_column('document', sa.Column('content', sa.Text(), nullable=True))
    
    # Add tags column for document categorization
    op.add_column('document', sa.Column('tags', sa.Text(), nullable=True, server_default='[]'))
    
    # Add history column for version tracking
    op.add_column('document', sa.Column('history', sa.Text(), nullable=True, server_default='[]'))
    
    # Add email_shares column for tracking shared emails
    op.add_column('document', sa.Column('email_shares', sa.Text(), nullable=True, server_default='[]'))
    
    # Make case_id nullable to allow documents without a case
    op.alter_column('document', 'case_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade():
    # Remove added columns in reverse order
    op.drop_column('document', 'email_shares')
    op.drop_column('document', 'history')
    op.drop_column('document', 'tags')
    op.drop_column('document', 'content')
    
    # Make case_id non-nullable again
    op.alter_column('document', 'case_id',
                    existing_type=sa.Integer(),
                    nullable=False) 