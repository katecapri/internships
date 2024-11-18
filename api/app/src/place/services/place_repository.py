from uuid import uuid4

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from src.place.models import Direction, Department, Curator, DepartmentDirection, Place, PlaceDepartment
from src.base_crud import BaseCRUD
from src.init_database import Session


class PlaceRepository:
    def __init__(self):
        self.db_session = Session
        self.model_direction = Direction
        self.model_department = Department
        self.model_curator = Curator
        self.model_place = Place
        self.model_department_direction = DepartmentDirection
        self.model_place_department = PlaceDepartment
        self.base = BaseCRUD(db_session=self.db_session)

    def get_directions(self):
        try:
            with self.base.transaction():
                stmt = select(self.model_direction)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return None

    def get_direction_by_id(self, direction_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_direction) \
                    .where(self.model_direction.id == direction_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def update_direction(self, direction_id, update_direction_data):
        try:
            stmt = update(self.model_direction).where(
                self.model_direction.id == direction_id,
            )
            if update_direction_data["name"]:
                stmt = stmt.values(name=update_direction_data["name"])
            if update_direction_data["display"]:
                stmt = stmt.values(display=update_direction_data["display"])
            stmt = stmt.returning(self.model_direction)
            return self.base.update_by_statement(self.model_direction, stmt)
        except NoResultFound:
            return None

    def get_direction_by_name(self, direction_name):
        try:
            with self.base.transaction():
                stmt = select(self.model_direction) \
                    .where(self.model_direction.name == direction_name)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_department_by_id(self, department_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_department) \
                    .where(self.model_department.id == department_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_curator_by_id(self, curator_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_curator) \
                    .where(self.model_curator.id == curator_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def delete_direction_departments_by_direction_id(self, direction_id):
        try:
            stmt = delete(self.model_department_direction)\
                .where(self.model_department_direction.direction_id == direction_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def save_direction_departments(self, direction_id, department_ids):
        with self.base.transaction():
            for department_id in department_ids:
                self.base.insert(
                    self.model_department_direction,
                    department_id=department_id,
                    direction_id=direction_id
                )
                self.base.commit()

    def get_places(self):
        try:
            with self.base.transaction():
                stmt = select(self.model_place)
                return self.base.get_many_by_statement(stmt)
        except NoResultFound:
            return None

    def create_place(self, name, address):
        with self.base.transaction():
            new_place = self.base.insert(
                self.model_place,
                id=uuid4(),
                name=name,
                address=address
            )
            self.base.commit()
        return new_place.id

    def get_place_by_id(self, place_id):
        try:
            with self.base.transaction():
                stmt = select(self.model_place) \
                    .where(self.model_place.id == place_id)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def get_place_by_name(self, place_name):
        try:
            with self.base.transaction():
                stmt = select(self.model_place) \
                    .where(self.model_place.name == place_name)
                return self.base.get_one_by_statement(stmt)
        except NoResultFound:
            return None

    def update_place(self, place_id, update_place_data):
        try:
            stmt = update(self.model_place).where(
                self.model_place.id == place_id,
            )
            if update_place_data["name"]:
                stmt = stmt.values(name=update_place_data["name"])
            if update_place_data["address"]:
                stmt = stmt.values(address=update_place_data["address"])
            stmt = stmt.returning(self.model_place)
            return self.base.update_by_statement(self.model_place, stmt)
        except NoResultFound:
            return None

    def delete_place_departments_by_place_id(self, place_id):
        try:
            stmt = delete(self.model_place_department)\
                .where(self.model_place_department.place_id == place_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None

    def save_place_departments(self, place_id, department_ids):
        with self.base.transaction():
            for department_id in department_ids:
                self.base.insert(
                    self.model_place_department,
                    department_id=department_id,
                    place_id=place_id
                )
                self.base.commit()

    def delete_place_by_id(self, place_id):
        try:
            self.delete_place_departments_by_place_id(place_id)
            stmt = delete(self.model_place).where(self.model_place.id == place_id)
            return self.base.delete_by_statement(stmt)
        except NoResultFound:
            return None
