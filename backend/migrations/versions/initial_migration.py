"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-03-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('first_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('practice_areas', sa.String(255)),
        sa.Column('years_of_experience', sa.Integer),
        sa.Column('languages', sa.String(255)),
        sa.Column('state', sa.String(2)),
        sa.Column('availability', sa.Text),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create cases table
    op.create_table('cases',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('case_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('priority', sa.String(50), nullable=False),
        sa.Column('client_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('lawyer_id', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('created', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create documents table
    op.create_table('documents',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('document_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('case_id', sa.String(36), sa.ForeignKey('cases.id'), nullable=False),
        sa.Column('created_by', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('file_path', sa.String(255)),
        sa.Column('file_size', sa.Integer),
        sa.Column('file_type', sa.String(50)),
        sa.Column('created', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create attorney_requests table
    op.create_table('attorney_requests',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('client_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('attorney_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('message', sa.Text),
        sa.Column('legal_issue_type', sa.String(50)),
        sa.Column('case_description', sa.Text),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create case_timeline_events table
    op.create_table('case_timeline_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('case_id', sa.String(36), sa.ForeignKey('cases.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('metadata', sa.Text),
        sa.Column('created_by', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('event_date', sa.DateTime, nullable=False)
    )

    # Create case_next_steps table
    op.create_table('case_next_steps',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('case_id', sa.String(36), sa.ForeignKey('cases.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('due_date', sa.DateTime),
        sa.Column('completed', sa.Boolean, default=False),
        sa.Column('completed_at', sa.DateTime),
        sa.Column('completed_by', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('created_by', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_cases_client_id', 'cases', ['client_id'])
    op.create_index('ix_cases_lawyer_id', 'cases', ['lawyer_id'])
    op.create_index('ix_documents_case_id', 'documents', ['case_id'])
    op.create_index('ix_attorney_requests_client_id', 'attorney_requests', ['client_id'])
    op.create_index('ix_attorney_requests_attorney_id', 'attorney_requests', ['attorney_id'])
    op.create_index('ix_case_timeline_events_case_id', 'case_timeline_events', ['case_id'])
    op.create_index('ix_case_next_steps_case_id', 'case_next_steps', ['case_id'])

def downgrade():
    # Drop tables in reverse order
    op.drop_table('case_next_steps')
    op.drop_table('case_timeline_events')
    op.drop_table('attorney_requests')
    op.drop_table('documents')
    op.drop_table('cases')
    op.drop_table('users') 