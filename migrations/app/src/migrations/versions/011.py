"""Add group codes

Revision ID: 011
Revises: 010
Create Date: 2023-05-22 13:00:00

"""
from alembic import op
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('groups', sa.Column('code', sa.String(), nullable=True))
    op.execute(
        """
        UPDATE groups SET code = 'trainee' WHERE name = 'Стажер';
        UPDATE groups SET code = 'graduate' WHERE name = 'Выпускник';
        UPDATE groups SET code = 'traineeCandidate' WHERE name = 'Кандидат';
        UPDATE groups SET code = 'staff' WHERE name = 'Кадры';
        UPDATE groups SET code = 'mentor' WHERE name = 'Наставник';
        UPDATE groups SET code = 'curator' WHERE name = 'Куратор';
        ALTER TABLE groups ALTER COLUMN code SET NOT NULL;
        """)
    op.create_unique_constraint("uq_groups_code", "groups", ["code"])


def downgrade() -> None:
    op.drop_column('groups', 'code')
