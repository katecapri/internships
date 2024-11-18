from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from src.user.models import User
from src.init_database import Base


class Place(Base):
    __tablename__ = 'places'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    address = Column(String(), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now())
    description = Column(String(), nullable=True)

    place_departments = relationship('PlaceDepartment', back_populates='place', lazy='subquery')

    @property
    def departments(self):
        departments = list()
        for place_department in self.place_departments:
            departments.append(place_department.department)
        return departments


class Department(Base):
    __tablename__ = 'departments'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)

    department_places = relationship('PlaceDepartment', back_populates='department')
    department_directions = relationship('DepartmentDirection', back_populates='department', lazy='subquery')

    @property
    def directions(self):
        directions = list()
        for department_direction in self.department_directions:
            directions.append(department_direction.direction)
        return directions


class PlaceDepartment(Base):
    __tablename__ = 'places_departments'

    place_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Place.id, ondelete="CASCADE"),
                      primary_key=True, nullable=False)
    department_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Department.id, ondelete="CASCADE"),
                           primary_key=True, nullable=False)

    place = relationship(Place, back_populates='place_departments')
    department = relationship(Department, back_populates='department_places', lazy='subquery')


class Curator(Base):
    __tablename__ = 'curators'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    directions = relationship('Direction', back_populates='curator')


class Direction(Base):
    __tablename__ = 'directions'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(), nullable=False)
    curator_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Curator.id), nullable=True)
    display = Column(Text(), nullable=True)

    curator = relationship(Curator, back_populates='directions')
    direction_departments = relationship('DepartmentDirection', back_populates='direction', lazy='subquery')

    @property
    def departments(self):
        departments = list()
        for direction_department in self.direction_departments:
            departments.append(direction_department.department)
        return departments


class DepartmentDirection(Base):
    __tablename__ = 'departments_directions'

    department_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Department.id, ondelete="CASCADE"),
                           primary_key=True, nullable=False)
    direction_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Direction.id, ondelete="CASCADE"),
                          primary_key=True, nullable=False)

    department = relationship(Department, back_populates='department_directions', lazy='subquery')
    direction = relationship(Direction, back_populates='direction_departments', lazy='subquery')
