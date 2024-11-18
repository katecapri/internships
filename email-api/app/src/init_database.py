import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.db_config import db_settings

engine = create_engine(db_settings.data_source_name, echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base(metadata=sqlalchemy.MetaData())
