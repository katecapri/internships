"""Add TemplateTimeSheetStep, RouteTimeSheetStep tables and fill second template - internship

Revision ID: 016
Revises: 015
Create Date: 2023-05-24 13:00:00

"""
from datetime import datetime
from alembic import op
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('route_time_sheep_steps',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('route_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('duration', sa.Integer(), nullable=False),
                    sa.Column('duration_item', sa.String(), nullable=False),
                    sa.Column('minimum_fill_percent', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['route_step_id'], ['route_steps.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))

    op.create_table('template_time_sheep_steps',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('template_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('duration', sa.Integer(), nullable=False),
                    sa.Column('duration_item', sa.String(), nullable=False),
                    sa.Column('minimum_fill_percent', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['template_step_id'], ['template_steps.id'], ondelete='cascade'),
                    sa.PrimaryKeyConstraint('id'))

    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('templates', 'template_steps', 'template_time_sheep_steps'))
    templates_table = sa.Table("templates", meta)
    template_steps_table = sa.Table("template_steps", meta)
    template_time_sheep_steps_table = sa.Table("template_time_sheep_steps", meta)

    template_id = str(uuid4())
    op.bulk_insert(
        templates_table,
        [{"id": template_id, "template_type": "internship", "from_group": "trainee",
          "to_group": "graduate", "creation_date": datetime.now()}
         ],
    )

    template_step_id_1 = str(uuid4())
    template_step_id_2 = str(uuid4())
    template_step_id_3 = str(uuid4())
    op.bulk_insert(
        template_steps_table,
        [{"id": template_step_id_1, "step_type": "timeSheet", "order": 1, "template_id": template_id,
          "is_start": False, "auto_verification": True, "points_value": 10},
         {"id": template_step_id_2, "step_type": "timeSheet", "order": 2, "template_id": template_id,
          "is_start": False, "auto_verification": True, "points_value": 10},
         {"id": template_step_id_3, "step_type": "timeSheet", "order": 3, "template_id": template_id,
          "is_start": False, "auto_verification": True, "points_value": 10},
         ],
    )

    op.bulk_insert(
        template_time_sheep_steps_table,
        [{"id": str(uuid4()), "template_step_id": template_step_id_1, "duration": 60,
          "duration_item": "days", "minimum_fill_percent": 50},
         {"id": str(uuid4()), "template_step_id": template_step_id_2, "duration": 60,
          "duration_item": "days", "minimum_fill_percent": 50},
         {"id": str(uuid4()), "template_step_id": template_step_id_3, "duration": 60,
          "duration_item": "days", "minimum_fill_percent": 50},
         ],
    )


def downgrade() -> None:
    op.drop_table('template_time_sheep_steps')
    op.drop_table('route_time_sheep_steps')
    internship_template = str(op.get_bind().execute("SELECT id FROM templates WHERE template_type = 'internship';").scalar_one())
    op.execute(f"DELETE FROM templates WHERE id = '{internship_template}';")
    op.execute(f"DELETE FROM template_steps WHERE template_id = '{internship_template}';")

