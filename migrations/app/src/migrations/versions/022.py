"""Add 20 candidates

Revision ID: 022
Revises: 021
Create Date: 2023-05-26 15:00:00

"""
import csv
import bcrypt
from datetime import datetime
from alembic import op
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '022'
down_revision = '021'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('users', 'candidates', 'users_groups', 'requests', 'request_verifications', 'request_fields'))
    users_table = sa.Table('users', meta)
    candidates_table = sa.Table('candidates', meta)
    users_groups_table = sa.Table('users_groups', meta)
    requests_table = sa.Table('requests', meta)
    request_verifications_table = sa.Table('request_verifications', meta)
    request_fields_table = sa.Table('request_fields', meta)
    app_user_app_role_id = str(op.get_bind().execute("SELECT id from app_roles WHERE code = 'APP_USER';").scalar_one())
    internship_selection_route_id = str(op.get_bind().execute("SELECT id from routes WHERE route_type = 'internshipSelection' AND start_date = '2023-09-01' AND (creation_date BETWEEN '2023-05-23' AND '2023-05-25');").scalar_one())
    route_step_id = str(op.get_bind().execute(f"SELECT id from route_steps WHERE route_id = '{internship_selection_route_id}';").scalar_one())
    group_candidate_id = str(op.get_bind().execute("SELECT id from groups WHERE code = 'traineeCandidate';").scalar_one())
    candidate_password = bcrypt.hashpw("candidate_password".encode(), bcrypt.gensalt()).decode()
    candidates_dict = dict()
    with open('/application/src/migrations/initial_data/candidates.csv') as f:
        reader = csv.DictReader(f)
        i = 1
        for row in reader:
            new_user_id = str(uuid4())
            new_candidate_id = str(uuid4())
            op.bulk_insert(users_table, [{"id": new_user_id, "name": row['Name'], "email": row['Email'],
                                          "is_email_confirmed": True, "creation_date": datetime.now(),
                                          "app_role_id": app_user_app_role_id, "password": candidate_password}])
            op.bulk_insert(users_groups_table, [{'user_id': new_user_id, "group_id": group_candidate_id}])
            is_confirmed = True if i < 17 else False
            op.bulk_insert(candidates_table, [{'id': new_candidate_id, "user_id": new_user_id,
                                              "route_id": str(internship_selection_route_id),
                                               "is_confirmed": is_confirmed}])
            candidates_dict[i] = new_user_id
            i += 1

    for i in range(1, 18):
        new_request_id = str(uuid4())
        op.bulk_insert(requests_table, [{"id": new_request_id, "user_id": candidates_dict[i],
                                         "request_status": "approved", "route_step_id": route_step_id,
                                         "creation_date": datetime.now(), "approval_date": datetime.now(),
                                         "rejection_date": None}])
        op.bulk_insert(request_verifications_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                                      "creation_date": datetime.now(), "is_correct": True,
                                                      "verification_error": None}])
        op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                               "field_name": 'Вы закончили 3 курса бакалавриата?',
                                               "field_type": 'boolean', "values_for_select_field": None,
                                               "correctness_criteria": 'quality', "verification_value": 'true',
                                               "must_be_verified": True, "field_value": 'true'}])
        op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                               "field_name": 'Гражданство', "field_type": 'selectWithInput',
                                               "values_for_select_field": '["Россия", "SELECT_OTHER"]',
                                               "correctness_criteria": 'quality', "verification_value": 'Россия',
                                               "must_be_verified": True, "field_value": 'Россия'}])
        op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                               "field_name": 'Возраст на момент начала отбора',
                                               "field_type": 'number', "values_for_select_field": None,
                                               "correctness_criteria": 'range', "verification_value": '{"min":18, "max":35}',
                                               "must_be_verified": True, "field_value": 22}])
    new_request_id = str(uuid4())
    op.bulk_insert(requests_table, [{"id": new_request_id, "user_id": candidates_dict[17],
                                     "request_status": "rejected", "route_step_id": route_step_id,
                                     "creation_date": datetime.now(), "approval_date": None,
                                     "rejection_date": datetime.now()}])
    op.bulk_insert(request_verifications_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                                  "creation_date": datetime.now(), "is_correct": False,
                                                  "verification_error": """{"fieldName": "\u0412\u043e\u0437\u0440\u0430\u0441\u0442 \u043d\u0430 \u043c\u043e\u043c\u0435\u043d\u0442 \u043d\u0430\u0447\u0430\u043b\u0430 \u043e\u0442\u0431\u043e\u0440\u0430", "correctnessCriteria": "range", "verificationValue": "{\"min\":18, \"max\":35}", "fieldValue": "45"}"""}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Вы закончили 3 курса бакалавриата?',
                                           "field_type": 'boolean', "values_for_select_field": None,
                                           "correctness_criteria": 'quality', "verification_value": 'true',
                                           "must_be_verified": True, "field_value": 'true'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Гражданство', "field_type": 'selectWithInput',
                                           "values_for_select_field": '["Россия", "SELECT_OTHER"]',
                                           "correctness_criteria": 'quality', "verification_value": 'Россия',
                                           "must_be_verified": True, "field_value": 'Россия'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Возраст на момент начала отбора',
                                           "field_type": 'number', "values_for_select_field": None,
                                           "correctness_criteria": 'range',
                                           "verification_value": '{"min":18, "max":35}',
                                           "must_be_verified": True, "field_value": 45}])
    new_request_id = str(uuid4())
    op.bulk_insert(requests_table, [{"id": new_request_id, "user_id": candidates_dict[18],
                                     "request_status": "rejected", "route_step_id": route_step_id,
                                     "creation_date": datetime.now(), "approval_date": None,
                                     "rejection_date": datetime.now()}])
    op.bulk_insert(request_verifications_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                                  "creation_date": datetime.now(), "is_correct": False,
                                                  "verification_error": """{"fieldName": "\u0412\u044b \u0437\u0430\u043a\u043e\u043d\u0447\u0438\u043b\u0438 3 \u043a\u0443\u0440\u0441\u0430 \u0431\u0430\u043a\u0430\u043b\u0430\u0432\u0440\u0438\u0430\u0442\u0430?", "correctnessCriteria": "quality", "verificationValue": "true", "fieldValue": "false"}"""}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Вы закончили 3 курса бакалавриата?',
                                           "field_type": 'boolean', "values_for_select_field": None,
                                           "correctness_criteria": 'quality', "verification_value": 'true',
                                           "must_be_verified": True, "field_value": 'false'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Гражданство', "field_type": 'selectWithInput',
                                           "values_for_select_field": '["Россия", "SELECT_OTHER"]',
                                           "correctness_criteria": 'quality', "verification_value": 'Россия',
                                           "must_be_verified": True, "field_value": 'Россия'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Возраст на момент начала отбора',
                                           "field_type": 'number', "values_for_select_field": None,
                                           "correctness_criteria": 'range',
                                           "verification_value": '{"min":18, "max":35}',
                                           "must_be_verified": True, "field_value": 22}])
    new_request_id = str(uuid4())
    op.bulk_insert(requests_table, [{"id": new_request_id, "user_id": candidates_dict[19],
                                     "request_status": "rejected", "route_step_id": route_step_id,
                                     "creation_date": datetime.now(), "approval_date": None,
                                     "rejection_date": datetime.now()}])
    op.bulk_insert(request_verifications_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                                  "creation_date": datetime.now(), "is_correct": False,
                                                  "verification_error": """{"fieldName": "\u0413\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u043e", "correctnessCriteria": "quality", "verificationValue": "\u0420\u043e\u0441\u0441\u0438\u044f", "fieldValue": "\u0411\u0435\u043b\u043e\u0440\u0443\u0441\u0441\u0438\u044f"}"""}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Вы закончили 3 курса бакалавриата?',
                                           "field_type": 'boolean', "values_for_select_field": None,
                                           "correctness_criteria": 'quality', "verification_value": 'true',
                                           "must_be_verified": True, "field_value": 'true'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Гражданство', "field_type": 'selectWithInput',
                                           "values_for_select_field": '["Россия", "SELECT_OTHER"]',
                                           "correctness_criteria": 'quality', "verification_value": 'Россия',
                                           "must_be_verified": True, "field_value": 'Белоруссия'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Возраст на момент начала отбора',
                                           "field_type": 'number', "values_for_select_field": None,
                                           "correctness_criteria": 'range',
                                           "verification_value": '{"min":18, "max":35}',
                                           "must_be_verified": True, "field_value": 22}])
    new_request_id = str(uuid4())
    op.bulk_insert(requests_table, [{"id": new_request_id, "user_id": candidates_dict[20],
                                     "request_status": "rejected", "route_step_id": route_step_id,
                                     "creation_date": datetime.now(), "approval_date": None,
                                     "rejection_date": datetime.now()}])
    op.bulk_insert(request_verifications_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                                  "creation_date": datetime.now(), "is_correct": False,
                                                  "verification_error": """{"fieldName": "\u0412\u043e\u0437\u0440\u0430\u0441\u0442 \u043d\u0430 \u043c\u043e\u043c\u0435\u043d\u0442 \u043d\u0430\u0447\u0430\u043b\u0430 \u043e\u0442\u0431\u043e\u0440\u0430", "correctnessCriteria": "range", "verificationValue": "{\"min\":18, \"max\":35}", "fieldValue": "45"}"""}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Вы закончили 3 курса бакалавриата?',
                                           "field_type": 'boolean', "values_for_select_field": None,
                                           "correctness_criteria": 'quality', "verification_value": 'true',
                                           "must_be_verified": True, "field_value": 'true'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Гражданство', "field_type": 'selectWithInput',
                                           "values_for_select_field": '["Россия", "SELECT_OTHER"]',
                                           "correctness_criteria": 'quality', "verification_value": 'Россия',
                                           "must_be_verified": True, "field_value": 'Белоруссия'}])
    op.bulk_insert(request_fields_table, [{'id': str(uuid4()), "request_id": new_request_id,
                                           "field_name": 'Возраст на момент начала отбора',
                                           "field_type": 'number', "values_for_select_field": None,
                                           "correctness_criteria": 'range',
                                           "verification_value": '{"min":18, "max":35}',
                                           "must_be_verified": True, "field_value": 45}])


def downgrade() -> None:
    candidates_id = list()
    with open('/application/src/migrations/initial_data/candidates.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            candidate_id = str(op.get_bind().execute(f"SELECT id from users WHERE email = '{row['Email']}';").scalar_one())
            candidates_id.append(candidate_id)
    candidates_id_tuple = tuple(candidates_id)
    op.execute(f"DELETE FROM requests WHERE user_id IN {candidates_id_tuple};")
    op.execute(f"DELETE FROM users WHERE user_id IN IN {candidates_id_tuple};")
    