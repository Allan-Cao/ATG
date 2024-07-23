from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base


class PlayerTeamAssociation(Base):
    __tablename__ = "player_team_associations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))
    position: Mapped[str] = mapped_column(String(10))

    player: Mapped["Player"] = relationship(
        "Player", back_populates="team_associations"
    )
    team: Mapped["Team"] = relationship("Team", back_populates="player_associations")

    def __repr__(self):
        return f"<PlayerTeamAssociation(id='{self.id}', player_id='{self.player_id}', team_id='{self.team_id}', position='{self.position}')>"
