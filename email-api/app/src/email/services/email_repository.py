from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.email.models import EmailEvent

from src.base_crud import BaseCRUD
from src.init_database import Session


class EmailRepository:
    def __init__(self):
        self.db_session = Session
        self.model = EmailEvent
        self.base = BaseCRUD(db_session=self.db_session)

    def get_email_event_by_id(self, email_event_id):
        try:
            with self.base.transaction():
                stmt = select(self.model).where(self.model.id == email_event_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def save_email_event(self, email_event_id, email_to):
        with self.base.transaction():
            self.base.insert(
                self.model,
                id=email_event_id,
                creation_date=datetime.now(),
                email_to=email_to,
            )
            self.base.commit()
            return email_event_id
