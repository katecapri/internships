"""Fill 6 routes

Revision ID: 017
Revises: 016
Create Date: 2023-05-24 15:00:00

"""
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '017'
down_revision = '016'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('routes', 'route_steps', 'route_request_field_templates', 'route_time_sheep_steps'))
    routes_table = Table("routes", meta)
    route_steps_table = Table("route_steps", meta)
    route_request_field_templates_table = Table("route_request_field_templates", meta)
    route_time_sheep_steps_table = Table("route_time_sheep_steps", meta)

    route_id_1 = str(uuid4())
    route_id_2 = str(uuid4())
    route_id_3 = str(uuid4())
    op.bulk_insert(
        routes_table,
        [{"id": route_id_1, "route_type": "internshipSelection", "from_group": "traineeCandidate",
          "to_group": "trainee", "creation_date": "2023-02-01",
          "start_date": "2023-03-01", "end_date": "2023-08-31"},
         {"id": route_id_2, "route_type": "internshipSelection", "from_group": "traineeCandidate",
          "to_group": "trainee", "creation_date": "2022-08-01",
          "start_date": "2022-09-01", "end_date": "2023-02-28"},
         {"id": route_id_3, "route_type": "internshipSelection", "from_group": "traineeCandidate",
          "to_group": "trainee", "creation_date": "2023-05-24",
          "start_date": "2023-09-01", "end_date": "2024-02-29"}
         ],
    )
    for route_id in [route_id_1, route_id_2, route_id_3]:
        route_step_id = str(uuid4())
        op.bulk_insert(
            route_steps_table,
            [{"id": route_step_id, "step_type": "request", "order": 1, "route_id": route_id,
              "is_start": True, "auto_verification": True, "points_value": 10}
             ],
        )

        op.bulk_insert(
            route_request_field_templates_table,
            [{"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Гражданство",
              "field_type": "selectWithInput", "values_for_select_field": '[\"Россия\", \"SELECT_OTHER\"]',
              "correctness_criteria": "quality", "verification_value": "Россия", "must_be_verified": True},
             {"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Возраст на момент начала отбора",
              "field_type": "number", "correctness_criteria": "range", "verification_value": '{"min":18, "max":35}',
              "must_be_verified": True, "values_for_select_field": None},
             {"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Вы закончили 3 курса бакалавриата?",
              "field_type": "boolean", "correctness_criteria": "quality", "verification_value": "true",
              "must_be_verified": True, "values_for_select_field": None},
             {"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Опыт работы",
              "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
              "values_for_select_field": None},
             {"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Опыт волонтерства",
              "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
              "values_for_select_field": None},
             {"id": str(uuid4()), "route_step_id": route_step_id, "field_name": "Опыт проектной работы",
              "field_type": "string", "must_be_verified": False, "correctness_criteria": None, "verification_value": None,
              "values_for_select_field": None},
             ],
        )

    route_id_4 = str(uuid4())
    route_id_5 = str(uuid4())
    route_id_6 = str(uuid4())
    op.bulk_insert(
        routes_table,
        [{"id": route_id_4, "route_type": "internship", "from_group": "trainee",
          "to_group": "graduate", "creation_date": "2023-02-01",
          "start_date": "2023-03-01", "end_date": "2023-08-31"},
         {"id": route_id_5, "route_type": "internship", "from_group": "trainee",
          "to_group": "graduate", "creation_date": "2022-08-01",
          "start_date": "2022-09-01", "end_date": "2023-02-28"},
         {"id": route_id_6, "route_type": "internship", "from_group": "trainee",
          "to_group": "graduate", "creation_date": "2023-05-24",
          "start_date": "2023-09-01", "end_date": "2024-02-29"}
         ],
    )
    for route_id in [route_id_4, route_id_5, route_id_6]:
        route_step_id_1 = str(uuid4())
        route_step_id_2 = str(uuid4())
        route_step_id_3 = str(uuid4())
        op.bulk_insert(
            route_steps_table,
            [{"id": route_step_id_1, "step_type": "timeSheet", "order": 1, "route_id": route_id,
              "is_start": False, "auto_verification": True, "points_value": 10},
             {"id": route_step_id_2, "step_type": "timeSheet", "order": 2, "route_id": route_id,
              "is_start": False, "auto_verification": True, "points_value": 10},
             {"id": route_step_id_3, "step_type": "timeSheet", "order": 3, "route_id": route_id,
              "is_start": False, "auto_verification": True, "points_value": 10},
             ],
        )

        op.bulk_insert(
            route_time_sheep_steps_table,
            [{"id": str(uuid4()), "route_step_id": route_step_id_1, "duration": 60,
              "duration_item": "days", "minimum_fill_percent": 50},
             {"id": str(uuid4()), "route_step_id": route_step_id_2, "duration": 60,
              "duration_item": "days", "minimum_fill_percent": 50},
             {"id": str(uuid4()), "route_step_id": route_step_id_3, "duration": 60,
              "duration_item": "days", "minimum_fill_percent": 50},
             ],
        )


def downgrade() -> None:
    op.execute("DELETE FROM routes WHERE id IN (SELECT id FROM routes WHERE creation_date IN ('2023-02-01', '2022-08-01', '2023-05-24'));")

