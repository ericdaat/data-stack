import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists


ENGINE_URL = "postgres://user:password@localhost:5432/ml_helper"

engine = db.create_engine(ENGINE_URL)
metadata = db.MetaData()
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)


def init_db():
    if not database_exists(ENGINE_URL):
        create_database(ENGINE_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)
