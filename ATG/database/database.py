from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_session_factory(database_url: str) -> sessionmaker[Session]:
    """Build a session factory bound to a new engine.

    :param database_url: SQLAlchemy database URL. PostgreSQL is required, as
        the models declare JSONB columns.
    :type database_url: str
    :returns: A factory producing sessions bound to the new engine.
    :rtype: sqlalchemy.orm.sessionmaker
    """
    engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=3600)
    return sessionmaker(bind=engine)
