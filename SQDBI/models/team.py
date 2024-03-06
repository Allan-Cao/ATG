from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.base import Base
from SQDBI.models.player_team_association import PlayerTeamAssociation


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    grid_id: Mapped[str] = Column(String(50), unique=True)
    code: Mapped[str] = Column(String(50), unique=True)

    player_associations: Mapped[List["PlayerTeamAssociation"]] = relationship(
        "PlayerTeamAssociation", back_populates="team"
    )

    def __repr__(self):
        return f"<Team(id='{self.id}', code='{self.code}')>"
