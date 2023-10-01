from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import settings


url = settings.sqlalchemy_database_url

engine = create_engine(url, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = session()


def get_db():
    db = session()
    try:
        return db
    except SQLAlchemyError as error:
        db.rollback()
        raise Exception(error)
    finally:
        db.close()
