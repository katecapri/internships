"""fill place, department, direction, curator and relation tables

Revision ID: 004
Revises: 003
Create Date: 2023-05-19 11:00:00

"""
import csv
import bcrypt
from datetime import datetime
from uuid import uuid4
from alembic import op
from sqlalchemy import Table, MetaData

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('places', 'departments', 'places_departments', 'curators', 'directions', 'departments_directions', 'users'))
    places_table = Table('places', meta)
    departments_table = Table('departments', meta)
    places_departments_table = Table("places_departments", meta)
    curators_table = Table("curators", meta)
    directions_table = Table('directions', meta)
    departments_directions_table = Table("departments_directions", meta)
    users_table = Table("users", meta)

    manager_app_role_id = str(op.get_bind().execute("SELECT id from app_roles WHERE code = 'MANAGER';").scalar_one())
    curators_email_id_dict = dict()
    curator_password = bcrypt.hashpw("curator_password".encode(), bcrypt.gensalt()).decode()
    with open('/application/src/migrations/initial_data/curators.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_user_id = str(uuid4())
            new_curator_id = str(uuid4())
            op.bulk_insert(users_table, [{"id": new_user_id, "name": row['Name'], "email": row['Email'],
                                          "is_email_confirmed": True, "creation_date": datetime.now(),
                                          "app_role_id": manager_app_role_id, "password": curator_password}])
            op.bulk_insert(curators_table, [{'id': new_curator_id, "user_id": new_user_id}])
            curators_email_id_dict[row['Email']] = new_curator_id

    directions_name_id_dict = dict()
    with open('/application/src/migrations/initial_data/directions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_direction_id = str(uuid4())
            op.bulk_insert(directions_table, [{"id": new_direction_id, "name": row['Name'], "display": row['Display'],
                                               "curator_id": curators_email_id_dict[row['Curator_email']]}])
            directions_name_id_dict[row['Name']] = new_direction_id

    departments_name_id_dict = dict()
    with open('/application/src/migrations/initial_data/departments with directions.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_department_id = str(uuid4())
            op.bulk_insert(departments_table, [{"id": new_department_id, "name": row['Department']}])
            departments_name_id_dict[row['Department']] = new_department_id
            op.bulk_insert(departments_directions_table,
                           [{"department_id": new_department_id, "direction_id": directions_name_id_dict[row['Direction']]}])

    with open('/application/src/migrations/initial_data/places with departments.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_place_id = str(uuid4())
            op.bulk_insert(places_table, [{"id": new_place_id, "name": row['Place'], "address": "Москва",
                                           "creation_date": datetime.now()}])
            op.bulk_insert(places_departments_table,
                           [{"place_id": new_place_id, "department_id": departments_name_id_dict[row['Department']]}])


def downgrade() -> None:
    op.execute("DELETE FROM places_departments")
    op.execute("DELETE FROM places")
    op.execute("DELETE FROM departments_directions")
    op.execute("DELETE FROM departments")
    op.execute("DELETE FROM directions")
    op.execute("DELETE FROM curators")
