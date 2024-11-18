from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects import postgresql

from src.init_database import Base


class EmailEvent(Base):
    __tablename__ = 'email_events'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    email_to = Column(String(), nullable=False)
