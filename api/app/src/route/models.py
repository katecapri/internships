from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, Enum, Date, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from src.route.services.route_core import RouteType, StepType, FieldType, CorrectnessCriteria, \
    TemplateType, RequestStatus, DurationItem
from src.init_database import Base


class Route(Base):
    __tablename__ = 'routes'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    route_type = Column(Enum(RouteType), nullable=False)
    from_group = Column(postgresql.UUID(as_uuid=True), ForeignKey('groups.code'), nullable=False)
    to_group = Column(postgresql.UUID(as_uuid=True), ForeignKey('groups.code'), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    start_date = Column(Date(), nullable=False)
    end_date = Column(Date(), nullable=False)

    steps = relationship('RouteStep', cascade="all, delete", lazy='subquery')
    trainees = relationship('Trainee', back_populates='route', lazy='subquery')


class RouteStep(Base):
    __tablename__ = 'route_steps'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    step_type = Column(Enum(StepType), nullable=False)
    order = Column(Integer(), nullable=False)
    route_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Route.id, ondelete="CASCADE"), nullable=False)
    is_start = Column(Boolean(), nullable=False)
    auto_verification = Column(Boolean(), nullable=False)
    points_value = Column(String(), nullable=False)

    request_field_templates = relationship('RouteRequestFieldTemplate', cascade="all, delete", lazy='subquery')
    route = relationship(Route, back_populates='steps')
    time_sheep_step = relationship('RouteTimeSheepStep', cascade="all, delete", lazy='subquery')


class RouteRequestFieldTemplate(Base):
    __tablename__ = 'route_request_field_templates'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    route_step_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(RouteStep.id, ondelete="CASCADE"), nullable=False)
    field_name = Column(String(), nullable=False)
    field_type = Column(Enum(FieldType), nullable=False)
    values_for_select_field = Column(Text(), nullable=True)
    correctness_criteria = Column(Enum(CorrectnessCriteria), nullable=True)
    verification_value = Column(String(), nullable=False)
    must_be_verified = Column(Boolean(), nullable=False, default=False)

    route_step = relationship(RouteStep, back_populates='request_field_templates')


class Template(Base):
    __tablename__ = 'templates'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    template_type = Column(Enum(TemplateType), nullable=False)
    from_group = Column(postgresql.UUID(as_uuid=True), ForeignKey('groups.code'), nullable=False)
    to_group = Column(postgresql.UUID(as_uuid=True), ForeignKey('groups.code'), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())

    steps = relationship('TemplateStep', cascade="all, delete", lazy='subquery')


class TemplateStep(Base):
    __tablename__ = 'template_steps'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    step_type = Column(Enum(StepType), nullable=False)
    order = Column(Integer(), nullable=False)
    template_id = Column(postgresql.UUID(as_uuid=True),
                         ForeignKey(Template.id, ondelete="CASCADE"), nullable=False)
    is_start = Column(Boolean(), nullable=False, default=False)
    auto_verification = Column(Boolean(), nullable=False, default=False)
    points_value = Column(Integer(), nullable=False)

    request_field_templates = relationship('TemplateRequestFieldTemplate', cascade="all, delete", lazy='subquery')
    template = relationship(Template, back_populates='steps')
    time_sheep_step = relationship('TemplateTimeSheepStep', cascade="all, delete", lazy='subquery')


class TemplateRequestFieldTemplate(Base):
    __tablename__ = 'template_request_field_templates'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    template_step_id = Column(postgresql.UUID(as_uuid=True),
                              ForeignKey(TemplateStep.id, ondelete="CASCADE"), nullable=False)
    field_name = Column(String(), nullable=False)
    field_type = Column(Enum(FieldType), nullable=False)
    values_for_select_field = Column(Text(), nullable=True)
    correctness_criteria = Column(Enum(CorrectnessCriteria), nullable=True)
    verification_value = Column(String(), nullable=True)
    must_be_verified = Column(Boolean(), nullable=False, default=False)

    template_step = relationship(TemplateStep, back_populates='request_field_templates')


class Request(Base):
    __tablename__ = 'requests'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    request_status = Column(Enum(RequestStatus), nullable=False)
    route_step_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(RouteStep.id), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    approval_date = Column(DateTime(), nullable=True)
    rejection_date = Column(DateTime(), nullable=True)

    fields = relationship('RequestField', cascade="all, delete", lazy='subquery')
    verifications = relationship('RequestVerification', cascade="all, delete", lazy='subquery')
    route_step = relationship(RouteStep, backref='requests', lazy='subquery')
    user = relationship('User', backref='requests', lazy='subquery')


class RequestField(Base):
    __tablename__ = 'request_fields'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    request_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Request.id, ondelete="CASCADE"), nullable=False)
    field_name = Column(String(), nullable=False)
    field_type = Column(Enum(FieldType), nullable=False)
    values_for_select_field = Column(Text(), nullable=True)
    correctness_criteria = Column(Enum(CorrectnessCriteria), nullable=True)
    verification_value = Column(String(), nullable=True)
    must_be_verified = Column(Boolean(), nullable=False, default=False)
    field_value = Column(String(), nullable=False)

    request = relationship(Request, back_populates='fields')


class RequestVerification(Base):
    __tablename__ = 'request_verifications'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    request_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Request.id, ondelete="CASCADE"), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    is_correct = Column(Boolean(), nullable=False, default=False)
    verification_error = Column(String(), nullable=True)

    request = relationship(Request, back_populates='verifications')


class RouteTimeSheepStep(Base):
    __tablename__ = 'route_time_sheep_steps'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    route_step_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(RouteStep.id, ondelete="CASCADE"), nullable=False)
    duration = Column(Integer(), nullable=False)
    duration_item = Column(Enum(DurationItem), nullable=False)
    minimum_fill_percent = Column(Integer(), nullable=False)

    route_step = relationship(RouteStep, back_populates='time_sheep_step')


class TemplateTimeSheepStep(Base):
    __tablename__ = 'template_time_sheep_steps'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    template_step_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(TemplateStep.id, ondelete="CASCADE"), nullable=False)
    duration = Column(Integer(), nullable=False)
    duration_item = Column(Enum(DurationItem), nullable=False)
    minimum_fill_percent = Column(Integer(), nullable=False)

    template_step = relationship(TemplateStep, back_populates='time_sheep_step')
