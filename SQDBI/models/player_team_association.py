from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.base import Base



class PlayerTeamAssociation(Base):
    __tablename__ = "player_team_associations"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = Column(Integer, ForeignKey("players.id"))
    team_id: Mapped[int] = Column(Integer, ForeignKey("teams.id"))
    position: Mapped[str] = Column(String(10))

    player: Mapped["Player"] = relationship(
        "Player", back_populates="team_associations"
    )
    team: Mapped["Team"] = relationship("Team", back_populates="player_associations")

    def __repr__(self):
        return f"<PlayerTeamAssociation(id='{self.id}', player_id='{self.player_id}', team_id='{self.team_id}', position='{self.position}')>"
