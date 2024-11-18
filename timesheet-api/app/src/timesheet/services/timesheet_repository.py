import logging
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from src.timesheet.models import TimesheetDay, TimesheetEvent
from src.timesheet.services.timesheet_core import DayType

from src.base_crud import BaseCRUD
from src.init_database import Session

logger = logging.getLogger('app')


class TimesheetRepository:
    def __init__(self):
        self.db_session = Session
        self.model_day = TimesheetDay
        self.model_event = TimesheetEvent
        self.base = BaseCRUD(db_session=self.db_session)

    def get_timesheet_days_by_user_and_route(self, user_id, route_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_day)\
                    .where(self.model_day.owner_id == user_id,
                           self.model_day.route_id == route_id)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return []

    def get_timesheet_event_by_id(self, event_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_event).where(self.model_event.id == event_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def create_timesheet_event(self, event_id, user_id, route_id, event_body):
        with self.base.transaction():
            self.base.insert(
                self.model_event,
                id=event_id,
                owner_id=user_id,
                route_id=route_id,
                creation_date=datetime.now(),
                event_body=event_body
            )
            self.base.commit()

    def create_new_timesheet(self, user_id, route_id, start_date, end_date):
        try:
            date = start_date
            with self.base.transaction():
                while date <= end_date:
                    self.base.insert(
                        self.model_day,
                        id=uuid4(),
                        owner_id=user_id,
                        route_id=route_id,
                        timesheet_date=date,
                        date_type=DayType.work if datetime.isoweekday(date) in range(1, 6) else DayType.dayOff
                    )
                    date = date + timedelta(days=1)
                self.base.commit()
            return True
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    def close_timesheet_event(self, event_id, is_interrupted):
        try:
            stmt = update(self.model_event).where(
                self.model_event.id == event_id,
            ).values(interrupted=is_interrupted,
                     end_date=datetime.now())
            stmt = stmt.returning(self.model_event)
            return self.base.update_by_statement(self.model_event, stmt)
        except NoResultFound:
            return None

    def update_timesheet_day(self, user_id, route_id, event_date, day_type):
        try:
            stmt = update(self.model_day).where(
                self.model_day.owner_id == user_id,
                self.model_day.route_id == route_id,
                self.model_day.timesheet_date == event_date,
            ).values(date_type=day_type)
            stmt = stmt.returning(self.model_day)
            return self.base.update_by_statement(self.model_day, stmt)
        except NoResultFound:
            return None
