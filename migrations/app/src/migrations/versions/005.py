"""add groups for managers

Revision ID: 005
Revises: 004
Create Date: 2023-05-19 12:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('groups',))
    groups_table = sa.Table('groups', meta)
    op.bulk_insert(
        groups_table,
        [{"id": str(uuid4()), "name": "Кадры", "restricted": "APP_ROLE", "restricted_value": "MANAGER"},
         {"id": str(uuid4()), "name": "Наставник", "restricted": "APP_ROLE", "restricted_value": "MANAGER"},
         {"id": str(uuid4()), "name": "Куратор", "restricted": "APP_ROLE", "restricted_value": "MANAGER"},
         ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM groups WHERE name in ('Кадры', 'Наставник', 'Куратор');")
