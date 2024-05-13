from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from SQDBI.models.base import Base

# Get the database connection details from environment variables
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_USERNAME = os.getenv("DATABASE_USERNAME")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_recycle=3600)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
