"""Create routes and templates tables

Revision ID: 012
Revises: 011
Create Date: 2023-05-23 10:00:00

"""
from alembic import op
from datetime import datetime
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '012'
down_revision = '011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('routes',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('route_type', sa.String(), nullable=False),
                    sa.Column('from_group', sa.String(), nullable=False),
                    sa.Column('to_group', sa.String(), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('start_date', sa.Date(), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=False),
                    sa.ForeignKeyConstraint(['from_group'], ['groups.code']),
                    sa.ForeignKeyConstraint(['to_group'], ['groups.code']),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('route_steps',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('step_type', sa.String(), nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.Column('route_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('is_start', sa.Boolean(), nullable=False),
                    sa.Column('auto_verification', sa.Boolean(), nullable=False),
                    sa.Column('points_value', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('route_request_field_templates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('route_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('field_name', sa.String(), nullable=False),
                    sa.Column('field_type', sa.String(), nullable=False),
                    sa.Column('values_for_select_field', sa.String(), nullable=True),
                    sa.Column('correctness_criteria', sa.String(), nullable=True),
                    sa.Column('verification_value', sa.String(), nullable=True),
                    sa.Column('must_be_verified', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['route_step_id'], ['route_steps.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('templates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('template_type', sa.String(), nullable=False),
                    sa.Column('from_group', sa.String(), nullable=False),
                    sa.Column('to_group', sa.String(), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.ForeignKeyConstraint(['from_group'], ['groups.code']),
                    sa.ForeignKeyConstraint(['to_group'], ['groups.code']),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('template_steps',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('step_type', sa.String(), nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('is_start', sa.Boolean(), nullable=False),
                    sa.Column('auto_verification', sa.Boolean(), nullable=False),
                    sa.Column('points_value', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('template_request_field_templates',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('template_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('field_name', sa.String(), nullable=False),
                    sa.Column('field_type', sa.String(), nullable=False),
                    sa.Column('values_for_select_field', sa.String(), nullable=True),
                    sa.Column('correctness_criteria', sa.String(), nullable=True),
                    sa.Column('verification_value', sa.String(), nullable=True),
                    sa.Column('must_be_verified', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['template_step_id'], ['template_steps.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('template_request_field_templates')
    op.drop_table('template_steps')
    op.drop_table('templates')
    op.drop_table('route_request_field_templates')
    op.drop_table('route_steps')
    op.drop_table('routes')
