"""Add parent_group_id and hierarchical to groups

Revision ID: 009
Revises: 008
Create Date: 2023-05-21 15:00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.text("ALTER TABLE groups ADD COLUMN hierarchical BOOLEAN DEFAULT false NOT NULL;"))
    op.add_column('groups', sa.Column('parent_group_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key('groups_parent_group_id_fkey', 'groups', 'groups', ['parent_group_id'], ['id'],
                          ondelete='SET NULL')
    hr_group_id = str(op.get_bind().execute("SELECT id FROM groups WHERE name = 'Кадры';").scalar_one())
    curator_group_id = str(op.get_bind().execute("SELECT id FROM groups WHERE name = 'Куратор';").scalar_one())
    op.execute(f"UPDATE groups SET parent_group_id = '{hr_group_id}', hierarchical = true WHERE name = 'Наставник';")
    op.execute(f"UPDATE groups SET parent_group_id = '{curator_group_id}', hierarchical = true WHERE name = 'Кадры';")
    op.execute(f"UPDATE groups SET hierarchical = true WHERE name = 'Куратор';")


def downgrade() -> None:
    op.drop_column('groups', 'parent_group_id')
    op.drop_column('groups', 'hierarchical')
