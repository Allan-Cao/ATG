import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from ATG.models import Base

load_dotenv()

Base.metadata.create_all(create_engine(os.environ["DB_CONNECTION"]))
