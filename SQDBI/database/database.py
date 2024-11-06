from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base


def get_session_factory(database_url: str):
    engine = create_engine(database_url, pool_recycle=3600)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
