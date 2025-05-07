"""
Migration script to add subscription fields to beta_signups table
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers
revision = 'add_subscription_fields'
down_revision = None
depends_on = None

def upgrade():
    """Add subscription-related columns to beta_signups table"""
    op.add_column('beta_signups', sa.Column('subscription_preferences', JSONB, nullable=True))
    op.add_column('beta_signups', sa.Column('subscribed_at', sa.DateTime(), nullable=True))
    op.add_column('beta_signups', sa.Column('is_subscribed', sa.Boolean(), server_default='false', nullable=False))
    
    # Create index on is_subscribed column for faster queries
    op.create_index(op.f('ix_beta_signups_is_subscribed'), 'beta_signups', ['is_subscribed'], unique=False)

def downgrade():
    """Remove subscription-related columns from beta_signups table"""
    op.drop_index(op.f('ix_beta_signups_is_subscribed'), table_name='beta_signups')
    op.drop_column('beta_signups', 'is_subscribed')
    op.drop_column('beta_signups', 'subscribed_at')
    op.drop_column('beta_signups', 'subscription_preferences') 