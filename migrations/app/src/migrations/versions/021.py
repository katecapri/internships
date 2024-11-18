"""Allow Manager read app_roles

Revision ID: 021
Revises: 020
Create Date: 2023-05-26 12:00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '021'
down_revision = '020'
branch_labels = None
depends_on = None


def upgrade() -> None:
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE code = 'MANAGER';").scalar_one())
    app_role_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'app_role';").scalar_one())
    op.execute(f"UPDATE app_role_permission_rules SET read_permission = true WHERE app_role_id = '{manager_app_role_id}' AND app_role_permission_id = '{app_role_bo_id}';")


def downgrade() -> None:
    manager_app_role_id = str(op.get_bind().execute("SELECT id FROM app_roles WHERE code = 'MANAGER';").scalar_one())
    app_role_bo_id = str(op.get_bind().execute("SELECT id FROM app_role_permissions WHERE target_name = 'app_role';").scalar_one())
    op.execute(f"UPDATE app_role_permission_rules SET read_permission = false WHERE app_role_id = '{manager_app_role_id}' AND app_role_permission_id = '{app_role_bo_id}';")
