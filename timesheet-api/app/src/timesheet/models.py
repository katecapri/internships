from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Enum, DateTime, Boolean, Text, Date
from sqlalchemy.dialects import postgresql

from src.timesheet.services.timesheet_core import DayType
from src.init_database import Base


class TimesheetDay(Base):
    __tablename__ = 'timesheet_days'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    owner_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    route_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    timesheet_date = Column(Date(), nullable=False)
    date_type = Column(Enum(DayType), nullable=False)


class TimesheetEvent(Base):
    __tablename__ = 'timesheet_events'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    owner_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    route_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    end_date = Column(DateTime(), nullable=True)
    interrupted = Column(Boolean(), nullable=True)
    event_body = Column(Text(), nullable=False)
