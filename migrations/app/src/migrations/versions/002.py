"""create group tables and fill groups

Revision ID: 002
Revises: 001
Create Date: 2023-05-18 15:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('groups',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('restricted', sa.String(), nullable=False),
                    sa.Column('restricted_value', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('users_groups',
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('user_id', 'group_id'))

    op.create_table('group_permission_rules',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('group_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('app_role_permission_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('has_access', sa.Boolean(), default=False, nullable=False),
                    sa.Column('create_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('read_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('update_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('delete_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('view_all_permission', sa.Boolean(), default=False, nullable=False),
                    sa.Column('modify_all_permission', sa.Boolean(), default=False, nullable=False),
                    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['app_role_permission_id'], ['app_role_permissions.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('groups',))
    groups_table = sa.Table('groups', meta)
    op.bulk_insert(
        groups_table,
        [{"id": str(uuid4()), "name": "Кандидат", "restricted": "APP_ROLE", "restricted_value": "APP_USER"},
         {"id": str(uuid4()), "name": "Стажер", "restricted": "APP_ROLE", "restricted_value": "APP_USER"},
         {"id": str(uuid4()), "name": "Выпускник", "restricted": "APP_ROLE", "restricted_value": "APP_USER"},
         ],
    )


def downgrade() -> None:
    op.drop_table('group_permission_rules')
    op.drop_table('users_groups')
    op.drop_table('groups')
