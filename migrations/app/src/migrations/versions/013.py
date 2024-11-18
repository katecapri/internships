"""Fill templates and rules for /template and /route entry_points

Revision ID: 013
Revises: 012
Create Date: 2023-05-23 11:00:00

"""
from datetime import datetime
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('app_role_permissions', 'app_role_permission_rules',
                       'templates', 'template_steps', 'template_request_field_templates'))
    app_role_permissions_table = Table("app_role_permissions", meta)
    app_role_permission_rules_table = Table("app_role_permission_rules", meta)
    templates_table = Table("templates", meta)
    template_steps_table = Table("template_steps", meta)
    template_request_field_templates_table = Table("template_request_field_templates", meta)

    template_id = str(uuid4())
    op.bulk_insert(
        templates_table,
        [{"id": template_id, "template_type": "internshipSelection", "from_group": "traineeCandidate",
          "to_group": "trainee", "creation_date": datetime.now().date()}
         ],
    )

    template_step_id = str(uuid4())
    op.bulk_insert(
        template_steps_table,
        [{"id": template_step_id, "step_type": "request", "order": 1, "template_id": template_id,
          "is_start": True, "auto_verification": True, "points_value": 10}
         ],
    )

    op.bulk_insert(
        template_request_field_templates_table,
        [{"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Гражданство",
          "field_type": "selectWithInput", "values_for_select_field": '[\"Россия\", \"SELECT_OTHER\"]',
          "correctness_criteria": "quality", "verification_value": "Россия", "must_be_verified": True},
         {"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Возраст на момент начала отбора",
          "field_type": "number", "correctness_criteria": "range", "verification_value": "{min:18, max:35}",
          "must_be_verified": True, "values_for_select_field": None},
         {"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Вы закончили 3 курса бакалавриата?",
          "field_type": "boolean", "correctness_criteria": "quality", "verification_value": "true",
          "must_be_verified": True, "values_for_select_field": None},
         {"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Опыт работы",
          "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
          "values_for_select_field": None},
         {"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Опыт волонтерства",
          "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
          "values_for_select_field": None},
         {"id": str(uuid4()), "template_step_id": template_step_id, "field_name": "Опыт проектной работы",
          "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
          "values_for_select_field": None},
         ],
    )

    guest_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Гость';").scalar_one())
    admin_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Админ';").scalar_one())
    app_user_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Участник';").scalar_one())
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE name = 'Менеджер';").scalar_one())

    template_bo_id = str(uuid4())
    route_bo_id = str(uuid4())
    op.bulk_insert(
        app_role_permissions_table,
        [{"id": template_bo_id, "level": "BUSINESS_OBJECT", "target_name": "template", "entry_point": "/template"},
         {"id": route_bo_id, "level": "BUSINESS_OBJECT", "target_name": "route", "entry_point": "/route"},
         ],
    )

    op.bulk_insert(
        app_role_permission_rules_table,
        [{"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": template_bo_id,
          "has_access": False, "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": template_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": template_bo_id,
          "has_access": False, "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": template_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},

         {"id": str(uuid4()), "app_role_id": guest_app_role_id, "app_role_permission_id": route_bo_id,
          "has_access": False, "create_permission": False, "read_permission": False, "update_permission": False,
          "delete_permission": False, "view_all_permission": False, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": admin_app_role_id, "app_role_permission_id": route_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         {"id": str(uuid4()), "app_role_id": app_user_app_role_id, "app_role_permission_id": route_bo_id,
          "has_access": False, "create_permission": False, "read_permission": True, "update_permission": False,
          "delete_permission": False, "view_all_permission": True, "modify_all_permission": False},
         {"id": str(uuid4()), "app_role_id": manager_app_role_id, "app_role_permission_id": route_bo_id,
          "has_access": True, "create_permission": True, "read_permission": True, "update_permission": True,
          "delete_permission": True, "view_all_permission": True, "modify_all_permission": True},
         ]
    )


def downgrade() -> None:
    template_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'template';").scalar_one())
    route_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'route';").scalar_one())
    op.execute(f"DELETE FROM app_role_permission_rules WHERE app_role_permission_id = '{template_bo_id}';")
    op.execute(f"DELETE FROM app_role_permission_rules WHERE app_role_permission_id = '{route_bo_id}';")
    op.execute(f"DELETE FROM app_role_permissions WHERE id = '{template_bo_id}';")
    op.execute(f"DELETE FROM app_role_permissions WHERE id = '{route_bo_id}';")
    op.execute("DELETE FROM template_request_field_templates")
    op.execute("DELETE FROM template_steps")
    op.execute("DELETE FROM templates")
