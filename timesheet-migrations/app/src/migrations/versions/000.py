"""Create timesheet_days and timesheet_events tables

Revision ID: 000
Revises:
Create Date: 2023-05-19 20:00:00

"""
from datetime import datetime
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('timesheet_days',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('route_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('timesheet_date', sa.Date(), nullable=False),
                    sa.Column('date_type', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('timesheet_events',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('route_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('end_date', sa.DateTime(), nullable=True),
                    sa.Column('interrupted', sa.Boolean(), nullable=True),
                    sa.Column('event_body', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('timesheet_events')
    op.drop_table('timesheet_days')

