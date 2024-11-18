from uuid import uuid4

from sqlalchemy import select, update, delete, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from src.app_role.models import AppRole, AppRolePermission, AppRolePermissionRule
from src.app_role.services.app_role_core import AppRolePermissionLevel
from src.base_crud import BaseCRUD
from src.init_database import Session


class AppRoleRepository:
    def __init__(self):
        self.db_session = Session
        self.model = AppRole
        self.model_permission = AppRolePermission
        self.model_permission_rule = AppRolePermissionRule
        self.base = BaseCRUD(db_session=self.db_session)

    def get_app_role_uuid_by_code(self, code):
        try:
            with self.base.transaction():
                stmt = select(self.model.id).where(self.model.code == code)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_app_roles(self):
        try:
            with self.base.transaction():
                stmt = select(self.model)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return None

    def get_app_role_by_id(self, app_role_id):
        try:
            with self.base.transaction():
                stmt = select(self.model).where(self.model.id == app_role_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_permission_rules_by_app_role_id(self, app_role_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_permission_rule) \
                    .options(joinedload(self.model_permission_rule.app_role_permission)) \
                    .where(self.model_permission_rule.app_role_id == app_role_id)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def create_app_role(self, name, code, description):
        with self.base.transaction():
            new_app_role = self.base.insert(
                self.model,
                id=uuid4(),
                name=name,
                code=code,
                description=description
            )
            self.base.commit()
        return new_app_role.id

    def create_app_role_permission_rule(self, app_role_permission_rule):
        with self.base.transaction():
            new_app_role_permission_rule = self.base.insert(
                self.model_permission_rule,
                id=uuid4(),
                app_role_id=app_role_permission_rule.app_role_id,
                app_role_permission_id=app_role_permission_rule.app_role_permission_id,
                has_access=app_role_permission_rule.has_access,
                create_permission=app_role_permission_rule.create_permission,
                read_permission=app_role_permission_rule.read_permission,
                update_permission=app_role_permission_rule.update_permission,
                delete_permission=app_role_permission_rule.delete_permission,
                view_all_permission=app_role_permission_rule.view_all_permission,
                modify_all_permission=app_role_permission_rule.modify_all_permission
            )
            self.base.commit()
        return new_app_role_permission_rule.id

    def get_app_role_permission_by_id(self, app_role_permission_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_permission).where(self.model_permission.id == app_role_permission_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return []

    def update_app_role(self, app_role_id, name, code, description):
        try:
            stmt = update(self.model).where(self.model.id == app_role_id)\
                .values(
                name=name,
                code=code,
                description=description,
            ).returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None

    def delete_app_role_permission_rules_by_app_role_id(self, app_role_id):
        try:
            stmt = delete(self.model_permission_rule).where(self.model_permission_rule.app_role_id == app_role_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def delete_app_role_by_id(self, app_role_id):
        try:
            self.delete_app_role_permission_rules_by_app_role_id(app_role_id)
            stmt = delete(self.model).where(self.model.id == app_role_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def get_permission_rule(self, app_role_id, app_role_permission_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_permission_rule).where(
                    self.model_permission_rule.app_role_id == app_role_id,
                    self.model_permission_rule.app_role_permission_id == app_role_permission_id,
                )
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_app_role_permission_by_attrs(self, level, target_name_or_entry_point):
        try:
            with self.base.transaction():
                if level == AppRolePermissionLevel.COMPONENT:
                    stmt = select(self.model_permission).where(
                        self.model_permission.level == level,
                        self.model_permission.target_name == target_name_or_entry_point
                    )
                else:
                    stmt = select(self.model_permission).where(
                        self.model_permission.level == level,
                        self.model_permission.entry_point == target_name_or_entry_point
                    )
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_groups_for_app_role_by_code(self, app_role_code):
        try:
            query_dict = {"app_role_code": app_role_code}
            with self.base.transaction():
                stmt = text("""
                SELECT * FROM groups WHERE restricted = 'APP_ROLE' AND restricted_value = :app_role_code;""")
                return self.base.get_data_by_statement_with_kwargs(stmt, query_dict)
        except NoResultFound:
            return []
