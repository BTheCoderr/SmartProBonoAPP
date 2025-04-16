"""Add queue tables

Revision ID: 20240320_01
Revises: initial_migration
Create Date: 2024-03-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '20240320_01'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Create queue_cases table
    op.create_table(
        'queue_cases',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('case_id', sa.String(36), sa.ForeignKey('cases.id'), nullable=False),
        sa.Column('priority', sa.String(20), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('situation_type', sa.String(50), nullable=False),
        sa.Column('metadata', sa.Text),
        sa.Column('assigned_lawyer_id', sa.String(36), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('assigned_at', sa.DateTime, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending')
    )
    
    # Create queue_history table
    op.create_table(
        'queue_history',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('timestamp', sa.DateTime, nullable=False, default=datetime.utcnow),
        sa.Column('total_cases', sa.Integer, nullable=False),
        sa.Column('urgent_cases', sa.Integer, nullable=False),
        sa.Column('high_cases', sa.Integer, nullable=False),
        sa.Column('medium_cases', sa.Integer, nullable=False),
        sa.Column('low_cases', sa.Integer, nullable=False),
        sa.Column('average_wait_time', sa.Float),
        sa.Column('longest_wait_time', sa.Float)
    )
    
    # Create indexes for better query performance
    op.create_index('idx_queue_cases_priority', 'queue_cases', ['priority'])
    op.create_index('idx_queue_cases_status', 'queue_cases', ['status'])
    op.create_index('idx_queue_cases_timestamp', 'queue_cases', ['timestamp'])
    op.create_index('idx_queue_history_timestamp', 'queue_history', ['timestamp'])


def downgrade():
    # Drop tables in reverse order
    op.drop_index('idx_queue_history_timestamp')
    op.drop_index('idx_queue_cases_timestamp')
    op.drop_index('idx_queue_cases_status')
    op.drop_index('idx_queue_cases_priority')
    op.drop_table('queue_history')
    op.drop_table('queue_cases') 