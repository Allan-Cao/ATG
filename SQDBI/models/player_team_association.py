from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from SQDBI.models.base import Base

class PlayerTeamAssociation(Base):
    __tablename__ = 'player_team_associations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    position = Column(String(10))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    player = relationship('Player', back_populates='team_associations')
    team = relationship('Team', back_populates='player_associations')

    def __repr__(self):
        return f"<PlayerTeamAssociation(id='{self.id}', player_id='{self.player_id}', team_id='{self.team_id}', position='{self.position}')>"