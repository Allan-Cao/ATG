from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from SQDBI.models.base import Base

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    grid_id = Column(String(50), unique=True)
    code = Column(String(50), unique=True)

    player_associations = relationship('PlayerTeamAssociation', back_populates='team')

    def __repr__(self):
        return f"<Team(id='{self.id}', code='{self.code}')>"