"""create email event table

Revision ID: 000
Revises:
Create Date: 2023-05-21 17:00:00

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('email_events',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('email_to', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('email_events')

