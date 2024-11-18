"""Add route_id column for candidate

Revision ID: 019
Revises: 018
Create Date: 2023-05-25 12:00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '019'
down_revision = '018'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('candidates', sa.Column('route_id', postgresql.UUID(as_uuid=True),
                                          sa.ForeignKey("routes.id"), nullable=True))


def downgrade() -> None:
    op.drop_column('candidates', 'route_id')
