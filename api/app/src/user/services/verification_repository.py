from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from src.user.models import Verification
from src.base_crud import BaseCRUD
from src.init_database import Session


class VerificationRepository:
    def __init__(self):
        self.db_session = Session
        self.model = Verification
        self.base = BaseCRUD(db_session=self.db_session)

    def create_verification(self, verification_code):
        with self.base.transaction():
            new_verification_code = self.base.insert(
                self.model,
                id=uuid4(),
                user_id=verification_code.user_id,
                type=verification_code.verification_type,
                code=verification_code.code,
                expired_time=datetime.now() + timedelta(hours=24)
            )
            self.base.commit()
        return new_verification_code.code

    def get_verification_by_code(self, code):
        try:
            with self.base.transaction():
                stmt = select(self.model) \
                    .where(self.model.code == str(code)) \
                    .limit(1)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def update_verification_used_time_by_id(self, verification_id):
        try:
            stmt = update(self.model).where(
                self.model.id == verification_id,
            ).values(
                used_time=datetime.now()
            ).returning(self.model)
            return self.base.update_by_statement(self.model, stmt)
        except NoResultFound:
            return None
