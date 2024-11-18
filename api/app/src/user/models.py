from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from src.user.services.user_core import VerificationType, RestrictedGroupType
from src.app_role.models import AppRole, AppRolePermission
from src.route.models import Route
from src.init_database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    email = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    is_email_confirmed = Column(Boolean(), nullable=False, default=False)
    password = Column(String(), nullable=True)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    app_role_id = Column(postgresql.UUID(as_uuid=True),
                         ForeignKey(AppRole.id, ondelete="RESTRICT"), nullable=False)

    app_role = relationship(AppRole, backref='users', lazy='subquery')
    user_groups = relationship('UserGroup', backref='user_groups', lazy='subquery')
    trainees = relationship('Trainee', back_populates='user', lazy='subquery')

    @property
    def groups(self):
        return [user_group.group for user_group in self.user_groups]


class Verification(Base):
    __tablename__ = 'verifications'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    type = Column(Enum(VerificationType), nullable=False)
    code = Column(String(), nullable=False)
    expired_time = Column(DateTime(), nullable=False)
    used_time = Column(DateTime(), nullable=True)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    restricted = Column(Enum(RestrictedGroupType), nullable=False)
    restricted_value = Column(String(), nullable=False)
    parent_group_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)
    hierarchical = Column(Boolean(), nullable=False, default=False)
    code = Column(String(), nullable=False, unique=True)

    rules = relationship('GroupPermissionRule', cascade="all, delete", lazy='joined')


class UserGroup(Base):
    __tablename__ = 'users_groups'

    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"),
                     primary_key=True, nullable=False)
    group_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Group.id),
                      primary_key=True, nullable=False)

    group = relationship(Group, backref='user_groups', lazy='subquery')


class GroupPermissionRule(Base):
    __tablename__ = 'group_permission_rules'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    group_id = Column(postgresql.UUID(as_uuid=True),
                      ForeignKey(Group.id, ondelete="CASCADE"), nullable=False)
    app_role_permission_id = Column(postgresql.UUID(as_uuid=True),
                                    ForeignKey(AppRolePermission.id, ondelete="CASCADE"), nullable=False)
    has_access = Column(Boolean(), nullable=False, default=False)
    create_permission = Column(Boolean(), nullable=False, default=False)
    read_permission = Column(Boolean(), nullable=False, default=False)
    update_permission = Column(Boolean(), nullable=False, default=False)
    delete_permission = Column(Boolean(), nullable=False, default=False)
    view_all_permission = Column(Boolean(), nullable=False, default=False)
    modify_all_permission = Column(Boolean(), nullable=False, default=False)

    group = relationship(Group, back_populates='rules')
    app_role_permission = relationship(AppRolePermission, back_populates='group_rules')


class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    is_confirmed = Column(Boolean(), nullable=False, default=False)
    route_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('routes.id'), nullable=True)

    user = relationship(User, cascade="all, delete", lazy='subquery')
    route = relationship(Route, cascade="all, delete", backref='candidates', lazy='subquery')


class Trainee(Base):
    __tablename__ = 'trainees'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    route_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('routes.id'), nullable=True)

    user = relationship(User, cascade="all, delete", lazy='subquery')
    route = relationship(Route, cascade="all, delete", back_populates='trainees', lazy='subquery')
