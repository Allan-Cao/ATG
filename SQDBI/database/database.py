from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from ..models import Base

# Get the database connection details from environment variables
DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

DATABASE_URL = f"postgresql+psycopg2://{DB_CONNECTION_STRING}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_recycle=3600)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
