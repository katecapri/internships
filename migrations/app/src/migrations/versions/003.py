"""create place, department, direction, curator and relation tables

Revision ID: 003
Revises: 002
Create Date: 2023-05-19 10:00:00

"""
from datetime import datetime
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('places',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('departments',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('places_departments',
                    sa.Column('place_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('department_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('place_id', 'department_id'))

    op.create_table('curators',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('directions',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('curator_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('display', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['curator_id'], ['curators.id']),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('departments_directions',
                    sa.Column('department_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('direction_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['direction_id'], ['directions.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('department_id', 'direction_id'))


def downgrade() -> None:
    op.drop_table('departments_directions')
    op.drop_table('directions')
    op.drop_table('curators')
    op.drop_table('places_departments')
    op.drop_table('places')

