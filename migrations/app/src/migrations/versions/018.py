"""Add Trainee table and create 3 trainees

Revision ID: 018
Revises: 017
Create Date: 2023-05-24 17:00:00

"""
import csv
import bcrypt
from datetime import datetime
from alembic import op
from uuid import uuid4
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '018'
down_revision = '017'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('trainees',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('route_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.id']),
                    sa.PrimaryKeyConstraint('id'))

    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect(only=('users', 'trainees', 'users_groups'))
    users_table = sa.Table('users', meta)
    trainees_table = sa.Table('trainees', meta)
    users_groups_table = sa.Table('users_groups', meta)
    app_user_app_role_id = str(op.get_bind().execute("SELECT id from app_roles WHERE code = 'APP_USER';").scalar_one())
    internship_routes_id = op.get_bind().execute("SELECT id from routes WHERE route_type = 'internship';").unique().all()
    group_trainee_id = str(op.get_bind().execute("SELECT id from groups WHERE code = 'trainee';").scalar_one())
    trainee_password = bcrypt.hashpw("trainee_password".encode(), bcrypt.gensalt()).decode()
    with open('/application/src/migrations/initial_data/trainees.csv') as f:
        reader = csv.DictReader(f)
        i = 0
        for row in reader:
            new_user_id = str(uuid4())
            new_trainee_id = str(uuid4())
            op.bulk_insert(users_table, [{"id": new_user_id, "name": row['Name'], "email": row['Email'],
                                          "is_email_confirmed": True, "creation_date": datetime.now(),
                                          "app_role_id": app_user_app_role_id, "password": trainee_password}])
            op.bulk_insert(users_groups_table, [{'user_id': new_user_id, "group_id": group_trainee_id}])
            op.bulk_insert(trainees_table, [{'id': new_trainee_id, "user_id": new_user_id,
                                             "route_id": str(internship_routes_id[i][0])}])
            i += 1


def downgrade() -> None:
    op.drop_table('trainees')
    trainees_email_list = list()
    with open('/application/src/migrations/initial_data/trainees.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trainees_email_list.append(row['Email'])
    trainees_email_tuple = tuple(trainees_email_list)
    op.execute(f"DELETE FROM users WHERE email IN {trainees_email_tuple};")