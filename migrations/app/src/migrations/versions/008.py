"""Rename app role name "Пользователь приложения" to "Участник"

Revision ID: 008
Revises: 007
Create Date: 2023-05-21 15:00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE app_roles SET name = 'Участник' WHERE code = 'APP_USER';")


def downgrade() -> None:
    op.execute("UPDATE app_roles SET name = 'Пользователь приложения' WHERE code = 'APP_USER';")
