from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from src.user.models import User, Group, UserGroup, Candidate, Trainee
from src.base_crud import BaseCRUD
from src.init_database import Session


class UserRepository:
    def __init__(self):
        self.db_session = Session
        self.model = User
        self.model_candidate = Candidate
        self.model_group = Group
        self.model_user_group = UserGroup
        self.model_trainee = Trainee
        self.base = BaseCRUD(db_session=self.db_session)

    def create_user(self, user):
        with self.base.transaction():
            new_user = self.base.insert(
                self.model,
                id=uuid4(),
                email=user.email,
                name=user.name,
                is_email_confirmed=user.is_email_confirmed,
                password=user.password,
                creation_date=datetime.now(),
                app_role_id=user.app_role_id
            )
            self.base.commit()
        return new_user.id

    def has_admin_user(self, admin_app_role_id):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.app_role_id == admin_app_role_id) \
                    .limit(1)
                result = self.base.get_one_by_statement(stmt)
                if result:
                    return True
        except NoResultFound:
            return False

    def get_user_by_email(self, email):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.email == email)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_user_by_id(self, user_id):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.id == user_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def update_user_password(self, user_id, password):
        try:
            stmt = update(self.model).where(
                self.model.id == user_id,
            ).values(
                password=password,
            ).returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None

    def verify_email(self, user_id):
        try:
            stmt = update(self.model).where(
                self.model.id == user_id,
            ).values(
                is_email_confirmed=True,
            ).returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None

    def get_users(self):
        try:
            with self.base.transaction():
                stmt = select(self.model).order_by(self.model.creation_date)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return None

    def update_user(self, user_id, update_user_info):
        try:
            stmt = update(self.model).where(
                self.model.id == user_id,
            )
            if update_user_info["email"]:
                stmt = stmt.values(email=update_user_info["email"])
            if update_user_info["name"]:
                stmt = stmt.values(name=update_user_info["name"])
            if update_user_info["isEmailConfirmed"]:
                stmt = stmt.values(is_email_confirmed=update_user_info["isEmailConfirmed"])
            if update_user_info["appRoleId"]:
                stmt = stmt.values(app_role_id=update_user_info["appRoleId"])
            stmt = stmt.returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None

    def delete_user(self, user_id):
        try:
            stmt = delete(self.model).where(self.model.id == user_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def get_users_by_app_role_id(self, app_role_id):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.app_role_id == app_role_id)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_group_id_by_name(self, name):
        try:
            with self.base.transaction():
                stmt = select(self.model_group.id) \
                    .where(self.model_group.name == name)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def save_user_group_relation(self, user_id, group_id):
        with self.base.transaction():
            self.base.insert(
                self.model_user_group,
                user_id=user_id,
                group_id=group_id
            )
            self.base.commit()

    def get_group_by_id(self, group_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_group) \
                    .where(self.model_group.id == group_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_groups_by_restricted_value_for_app_role(self, restricted_value):
        try:
            with self.base.transaction():
                stmt = select(self.model_group) \
                    .where(self.model_group.restricted == "APP_ROLE",
                           self.model_group.restricted_value == restricted_value)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return None

    def get_group_by_name(self, group_name):
        try:
            with self.base.transaction():
                stmt = select(self.model_group) \
                    .where(self.model_group.name == group_name)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_group_by_code(self, group_code):
        try:
            with self.base.transaction():
                stmt = select(self.model_group) \
                    .where(self.model_group.code == group_code)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def delete_user_groups_by_user_id(self, user_id):
        try:
            stmt = delete(self.model_user_group)\
                .where(self.model_user_group.user_id == user_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def save_new_candidate(self, user_id):
        with self.base.transaction():
            new_candidate_id = uuid4()
            self.base.insert(
                self.model_candidate,
                id=new_candidate_id,
                user_id=user_id,
                is_confirmed=False
            )
            self.base.commit()
            return new_candidate_id

    def save_new_trainee(self, user_id, route_id=None):
        with self.base.transaction():
            new_trainee_id = uuid4()
            self.base.insert(
                self.model_trainee,
                id=new_trainee_id,
                user_id=user_id,
                route_id=route_id
            )
            self.base.commit()
            return new_trainee_id

    def get_candidate_by_user_id(self, user_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_candidate) \
                    .where(self.model_candidate.user_id == user_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_trainee_by_user_id(self, user_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_trainee) \
                    .where(self.model_trainee.user_id == user_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def confirm_candidate(self, user_id):
        try:
            stmt = update(self.model_candidate).where(
                self.model_candidate.user_id == user_id,
            ).values(is_confirmed=True)
            stmt = stmt.returning(self.model_candidate)
            return self.base.update_by_statement(self.model_candidate, stmt)
        except NoResultFound:
            return None

    def get_trainees_by_route_id(self, route_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_trainee) \
                    .where(self.model_trainee.route_id == route_id)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def set_route_to_candidate(self, user_id, route_id):
        try:
            stmt = update(self.model_candidate)\
                .where(self.model_candidate.user_id == user_id)\
                .values(route_id=route_id)\
                .returning(self.model_candidate)
            return self.base.update_by_statement(self.model_candidate, stmt)
        except NoResultFound:
            return []

    def set_route_to_trainee(self, user_id, route_id):
        try:
            stmt = update(self.model_trainee)\
                .where(self.model_trainee.user_id == user_id)\
                .values(route_id=route_id)\
                .returning(self.model_trainee)
            return self.base.update_by_statement(self.model_trainee, stmt)
        except NoResultFound:
            return []
