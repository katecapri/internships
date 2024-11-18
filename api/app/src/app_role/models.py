from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from src.app_role.services.app_role_core import AppRolePermissionLevel
from src.init_database import Base


class AppRole(Base):
    __tablename__ = 'app_roles'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    code = Column(String(), nullable=False)
    description = Column(String(), nullable=True)

    rules = relationship('AppRolePermissionRule', cascade="all, delete", lazy='joined')


class AppRolePermission(Base):
    __tablename__ = 'app_role_permissions'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    level = Column(Enum(AppRolePermissionLevel), nullable=False)
    target_name = Column(String(), nullable=False)
    entry_point = Column(String(), nullable=False)

    rules = relationship('AppRolePermissionRule', cascade="all, delete", lazy='joined')
    group_rules = relationship("GroupPermissionRule", cascade="all, delete", lazy='joined')


class AppRolePermissionRule(Base):
    __tablename__ = 'app_role_permission_rules'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    app_role_id = Column(postgresql.UUID(as_uuid=True),
                         ForeignKey(AppRole.id, ondelete="CASCADE"), nullable=False)
    app_role_permission_id = Column(postgresql.UUID(as_uuid=True),
                                    ForeignKey(AppRolePermission.id, ondelete="CASCADE"), nullable=False)
    has_access = Column(Boolean(), nullable=False, default=False)
    create_permission = Column(Boolean(), nullable=False, default=False)
    read_permission = Column(Boolean(), nullable=False, default=False)
    update_permission = Column(Boolean(), nullable=False, default=False)
    delete_permission = Column(Boolean(), nullable=False, default=False)
    view_all_permission = Column(Boolean(), nullable=False, default=False)
    modify_all_permission = Column(Boolean(), nullable=False, default=False)

    app_role = relationship(AppRole, back_populates='rules')
    app_role_permission = relationship(AppRolePermission, back_populates='rules')
