"""Set route_id in trainees table NOT NULL

Revision ID: 020
Revises: 019
Create Date: 2023-05-25 15:00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '020'
down_revision = '019'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE trainees ALTER COLUMN route_id DROP NOT NULL;")


def downgrade() -> None:
    op.execute("ALTER TABLE trainees ALTER COLUMN route_id SET NOT NULL;")
