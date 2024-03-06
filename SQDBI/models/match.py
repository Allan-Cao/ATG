from sqlalchemy import Column, String, DateTime
from SQDBI.models.base import Base

class Match(Base):
    __tablename__ = 'matches'

    id = Column(String(255), primary_key=True)
    creation_time = Column(DateTime)
    duration = Column(Integer)
    patch = Column(String(20))
    # Add more columns as needed