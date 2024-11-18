"""Add curators to curator group and fill rules for /direction and /place entry_points

Revision ID: 006
Revises: 005
Create Date: 2023-05-19 13:00:00

"""
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    curator_group_id = str(op.get_bind().execute("SELECT id FROM groups WHERE name = 'Куратор';").scalar_one())
    curator_user_ids_objects = op.get_bind().execute("SELECT user_id FROM curators;").fetchall()
    curator_user_ids = [str(curator_user_id[0]) for curator_user_id in curator_user_ids_objects]

    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('app_role_permissions', 'app_role_permission_rules', 'users_groups'))
    app_role_permissions_table = Table("app_role_permissions", meta)
    app_role_permission_rules_table = Table("app_role_permission_rules", meta)
    users_groups_table = Table("users_groups", meta)
    for user_id in curator_user_ids:
        op.bulk_insert(users_groups_table, [{"user_id": user_id, "group_id": curator_group_id}])

    guest_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Гость';").scalar_one())
    admin_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Админ';").scalar_one())
    app_user_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Пользователь приложения';").scalar_one())
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Менеджер';").scalar_one())

    direction_bo_id = str(uuid4())
    place_bo_id = str(uuid4())
    op.bulk_insert(
        app_role_permissions_table,
        [{"id": direction_bo_id, "level": "BUSINESS_OBJECT", "target_name": "direction", "entry_point": "/direction"},
         {"id": place_bo_id, "level": "BUSINESS_OBJECT", "target_name": "place", "entry_point": "/place"},
         ],
    )

    op.bulk_insert(
        app_role_permission_rules_table,
        [{"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": direction_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": direction_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": direction_bo_id, "has_access": False,
          "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": direction_bo_id, "has_access": True,
          "create_permission": False, "read_permission": True, "update_permission": True,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": True},

         {"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": place_bo_id, "has_access": False,
          "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": place_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": place_bo_id, "has_access": False,
          "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": place_bo_id, "has_access": True,
          "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True}
         ]
    )


def downgrade() -> None:
    direction_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'direction';").scalar_one())
    place_bo_id = str(op.get_bind().execute("SELECT id app_role_permissions groups WHERE target_name = 'place';").scalar_one())
    op.execute(f"DELETE FROM app_role_permission_rules WHERE app_role_permission_id IN ('{place_bo_id}', '{direction_bo_id}');")
    op.execute(f"DELETE FROM app_role_permissions WHERE id IN ('{place_bo_id}', '{direction_bo_id}');")
    curator_group_id = str(op.get_bind().execute("SELECT id FROM groups WHERE name = 'Куратор';").scalar_one())
    op.execute(f"DELETE FROM users_groups WHERE group_id = '{curator_group_id}');")
