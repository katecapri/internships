"""add data to app_roles tables

Revision ID: 001
Revises: 000
Create Date: 2023-05-16 13:00:00

"""
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '001'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('app_roles', 'app_role_permissions', 'app_role_permission_rules'))
    app_roles_table = Table('app_roles', meta)
    app_role_permissions_table = Table("app_role_permissions", meta)
    app_role_permission_rules_table = Table("app_role_permission_rules", meta)
    guest_id = str(uuid4())
    admin_id = str(uuid4())
    app_user_id = str(uuid4())
    manager_id = str(uuid4())
    op.bulk_insert(
        app_roles_table,
        [{"id": guest_id, "name": "Гость", "code": "GUEST", "description": ""},
         {"id": admin_id, "name": "Админ", "code": "ADMIN", "description": ""},
         {"id": app_user_id, "name": "Пользователь приложения", "code": "APP_USER", "description": "Кандидат, стажер, выпускник"},
         {"id": manager_id,  "name": "Менеджер", "code": "MANAGER", "description": "Куратор, наставник"},
         ],
    )
    cabinet_id = str(uuid4())
    admin_console_id = str(uuid4())
    user_bo_id = str(uuid4())
    app_role_bo_id = str(uuid4())
    news_bo_id = str(uuid4())
    op.bulk_insert(
        app_role_permissions_table,
        [{"id": cabinet_id, "level": "COMPONENT", "target_name": "cabinet", "entry_point": ""},
         {"id": admin_console_id, "level": "COMPONENT", "target_name": "admin_console", "entry_point": ""},
         {"id": user_bo_id, "level": "BUSINESS_OBJECT", "target_name": "user", "entry_point": "/user"},
         {"id": app_role_bo_id, "level": "BUSINESS_OBJECT", "target_name": "app_role", "entry_point": "/appRole"},
         {"id": news_bo_id, "level": "BUSINESS_OBJECT", "target_name": "news", "entry_point": "/news"},
         ],
    )
    op.bulk_insert(
        app_role_permission_rules_table,
        [{"id": str(uuid4()), "app_role_id": guest_id, "app_role_permission_id": cabinet_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": guest_id, "app_role_permission_id": admin_console_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": guest_id, "app_role_permission_id": user_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": guest_id, "app_role_permission_id": app_role_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": guest_id, "app_role_permission_id": news_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},

         {"id": str(uuid4()), "app_role_id": admin_id, "app_role_permission_id": cabinet_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": admin_id, "app_role_permission_id": admin_console_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": admin_id, "app_role_permission_id": user_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": admin_id, "app_role_permission_id": app_role_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": admin_id, "app_role_permission_id": news_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},

         {"id": str(uuid4()), "app_role_id": app_user_id, "app_role_permission_id": cabinet_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_id, "app_role_permission_id": admin_console_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": app_user_id, "app_role_permission_id": user_bo_id, "has_access": False,
          "create_permission": False, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": app_user_id, "app_role_permission_id": app_role_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": app_user_id, "app_role_permission_id": news_bo_id, "has_access": False,
          "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": False},

         {"id": str(uuid4()), "app_role_id": manager_id, "app_role_permission_id": cabinet_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_id, "app_role_permission_id": admin_console_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": manager_id, "app_role_permission_id": user_bo_id, "has_access": False,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_id, "app_role_permission_id": app_role_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_id, "app_role_permission_id": news_bo_id, "has_access": False,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": False}
         ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM app_role_permission_rules")
    op.execute("DELETE FROM app_role_permissions")
    op.execute("DELETE FROM app_roles")
