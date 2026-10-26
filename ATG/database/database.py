from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base


def get_session_factory(database_url: str, read_only: bool = False):
    """Build a session factory bound to a new engine.

    Unless ``read_only`` is set, any tables declared on the models but missing
    from the database are created as a side effect.

    :param database_url: SQLAlchemy database URL. PostgreSQL is required, as
        the models declare JSONB columns.
    :type database_url: str
    :param read_only: Skip creating missing tables, defaults to ``False``.
    :type read_only: bool
    :returns: A factory producing sessions with ``autocommit`` disabled and
        ``autoflush`` enabled.
    :rtype: sqlalchemy.orm.sessionmaker
    """
    engine = create_engine(database_url, pool_recycle=3600)
    if not read_only:
        Base.metadata.create_all(bind=engine)
    return sessionmaker(autocommit=False, autoflush=True, bind=engine)
