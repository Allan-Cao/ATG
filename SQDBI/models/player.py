from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from SQDBI.models.base import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    accounts = relationship('Account', back_populates='player')
    team_associations = relationship('PlayerTeamAssociation', back_populates='player')
    solo_queue_games = relationship('Participant', back_populates='player')

    def __repr__(self):
        return f"<Player(id='{self.id}', name='{self.name}')>"