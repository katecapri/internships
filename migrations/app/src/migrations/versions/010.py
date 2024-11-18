"""Add Candidate

Revision ID: 010
Revises: 009
Create Date: 2023-05-22 12:00:00

"""
from alembic import op
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('candidates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('is_confirmed', sa.Boolean(), default=False, nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('candidates')
