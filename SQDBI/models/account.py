from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from SQDBI.models.base import Base
from datetime import datetime

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String(255), unique=True)
    account_name = Column(String(255))
    account_tagline = Column(String(255))
    region = Column(String(50))
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player', back_populates='accounts')

    games = relationship('Participant', back_populates='account')

    def __repr__(self):
        return f"<Account(id='{self.id}', {self.account_name}#{self.account_tagline}, region='{self.region}')>"