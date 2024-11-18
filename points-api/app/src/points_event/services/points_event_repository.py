from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.points_event.models import PointsEvent

from src.base_crud import BaseCRUD
from src.init_database import Session


class PointsEventRepository:
    def __init__(self):
        self.db_session = Session
        self.model = PointsEvent
        self.base = BaseCRUD(db_session=self.db_session)

    def get_points_event_by_id(self, points_event_id):
        try:
            stmt = select(self.model).where(self.model.id == points_event_id)
            return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_points_events_by_user_id(self, user_id):
        try:
            stmt = select(self.model) \
                .order_by(self.model.creation_date.desc())\
                .where(self.model.owner_id == user_id)
            return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def save_points_event(self, points_event):
        with self.base.transaction():
            self.base.insert(
                self.model,
                id=points_event.id,
                owner_id=points_event.owner_id,
                increase=points_event.increase,
                value=points_event.value,
                creation_date=datetime.now(),
                reason=points_event.reason,
            )
            self.base.commit()
        return points_event.id
