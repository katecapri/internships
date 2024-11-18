"""Fill rules for /points entry_point

Revision ID: 007
Revises: 006
Create Date: 2023-05-20 10:00:00

"""
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('app_role_permissions', 'app_role_permission_rules'))
    app_role_permissions_table = Table("app_role_permissions", meta)
    app_role_permission_rules_table = Table("app_role_permission_rules", meta)

    guest_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Гость';").scalar_one())
    admin_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Админ';").scalar_one())
    app_user_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Пользователь приложения';").scalar_one())
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Менеджер';").scalar_one())

    points_bo_id = str(uuid4())
    op.bulk_insert(
        app_role_permissions_table,
        [{"id": points_bo_id, "level": "BUSINESS_OBJECT", "target_name": "points", "entry_point": "/points"},
         ],
    )

    op.bulk_insert(
        app_role_permission_rules_table,
        [{"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": points_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": points_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": points_bo_id, "has_access": False,
          "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": points_bo_id, "has_access": True,
          "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": True},
         ]
    )


def downgrade() -> None:
    points_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'points';").scalar_one())
    op.execute(f"DELETE FROM app_role_permission_rules WHERE app_role_permission_id = '{points_bo_id}';")
    op.execute(f"DELETE FROM app_role_permissions WHERE id = '{points_bo_id}';")
