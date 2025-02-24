import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv()

DB_URL = "mariadb+mariadbconnector://{}:{}@{}:{}/{}".format(os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"))
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()
session=sqlalchemy.orm.Session(bind=engine, autoflush=False, autocommit=False)