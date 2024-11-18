"""Create requests tables

Revision ID: 014
Revises: 013
Create Date: 2023-05-23 15:00:00

"""
from alembic import op
from datetime import datetime
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '014'
down_revision = '013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('requests',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('request_status', sa.String(), nullable=False),
                    sa.Column('route_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('approval_date', sa.DateTime(), nullable=True),
                    sa.Column('rejection_date', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
                    sa.ForeignKeyConstraint(['route_step_id'], ['route_steps.id']),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('request_verifications',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('request_id',  postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), default=datetime.now(), nullable=False),
                    sa.Column('is_correct', sa.Boolean(), nullable=False),
                    sa.Column('verification_error', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('request_fields',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('field_name', sa.String(), nullable=False),
                    sa.Column('field_type', sa.String(), nullable=False),
                    sa.Column('values_for_select_field', sa.String(), nullable=True),
                    sa.Column('correctness_criteria', sa.String(), nullable=True),
                    sa.Column('verification_value', sa.String(), nullable=True),
                    sa.Column('must_be_verified', sa.Boolean(), nullable=False),
                    sa.Column('field_value', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ondelete="cascade"),
                    sa.PrimaryKeyConstraint('id'))

    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('app_role_permissions', 'app_role_permission_rules'))
    app_role_permissions_table = sa.Table("app_role_permissions", meta)
    app_role_permission_rules_table = sa.Table("app_role_permission_rules", meta)

    guest_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Гость';").scalar_one())
    admin_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Админ';").scalar_one())
    app_user_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Участник';").scalar_one())
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Менеджер';").scalar_one())

    request_bo_id = str(uuid4())
    op.bulk_insert(
        app_role_permissions_table,
        [{"id": request_bo_id, "level": "BUSINESS_OBJECT", "target_name": "request", "entry_point": "/request"}],
    )

    op.bulk_insert(
        app_role_permission_rules_table,
        [{"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": request_bo_id,
          "has_access": False, "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": request_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": request_bo_id,
          "has_access": False, "create_permission": True, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": request_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         ]
    )


def downgrade() -> None:
    op.drop_table('route_request_field_templates')
    op.drop_table('request_verifications')
    op.drop_table('requests')
    request_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'request';").scalar_one())
    op.execute(f"DELETE FROM app_role_permission_rules WHERE app_role_permission_id = '{request_bo_id}';")
    op.execute(f"DELETE FROM app_role_permissions WHERE id = '{request_bo_id}';")
