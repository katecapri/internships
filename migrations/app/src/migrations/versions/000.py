"""create user, verification and app_roles tables

Revision ID: 000
Revises:
Create Date: 2023-05-16 12:00:00

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
    op.create_table('app_roles',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('app_role_permissions',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('level', sa.String(), nullable=False),
                    sa.Column('target_name', sa.String(), nullable=False),
                    sa.Column('entry_point', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('app_role_permission_rules',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('app_role_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('app_role_permission_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('has_access', sa.Boolean(), default=False, nullable=False),
                    sa.Column('create_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('read_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('update_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('delete_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('view_all_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('modify_all_permission', sa.Boolean(), default=False, nullable=False),
                    sa.ForeignKeyConstraint(['app_role_id'], ['app_roles.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['app_role_permission_id'], ['app_role_permissions.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('users',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('is_email_confirmed', sa.Boolean(), default=False, nullable=False),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('app_role_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['app_role_id'], ['app_roles.id']),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('verifications',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('code', sa.String(), nullable=False),
                    sa.Column('expired_time', sa.DateTime(), nullable=False),
                    sa.Column('used_time', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))


def downgrade() -> None:
    op.drop_table('verifications')
    op.drop_table('users')
    op.drop_table('app_role_permission_rules')
    op.drop_table('app_role_permissions')
    op.drop_table('app_roles')

