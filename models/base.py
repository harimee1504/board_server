import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from sqlalchemy import create_engine, types
from sqlalchemy.orm import sessionmaker
import uuid

class UUIDType(types.TypeDecorator):
    impl = types.String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, uuid.UUID):
            return str(value)
        else:
            return str(uuid.UUID(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

    def get_col_spec(self, **kw):
        return "CHAR(36)"

from dotenv import load_dotenv
load_dotenv()

DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
engine = create_engine(DB_URL, echo=True, pool_pre_ping=True, pool_recycle=3600)
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()