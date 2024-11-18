from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects import postgresql

from src.init_database import Base


class PointsEvent(Base):
    __tablename__ = 'points_events'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    owner_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    increase = Column(Boolean(), nullable=False)
    value = Column(String(), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    reason = Column(String(), nullable=True)
