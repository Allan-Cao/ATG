from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.account import Account
from SQDBI.models.base import Base
from SQDBI.models.participant import Participant
from SQDBI.models.player_team_association import PlayerTeamAssociation


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255))

    accounts: Mapped[Optional[List["Account"]]] = relationship(
        "Account", back_populates="player"
    )
    team_associations: Mapped[Optional[List["PlayerTeamAssociation"]]] = relationship(
        "PlayerTeamAssociation", back_populates="player"
    )
    solo_queue_games: Mapped[Optional[List["Participant"]]] = relationship(
        "Participant", back_populates="player"
    )

    def __repr__(self) -> str:
        return f"<Player(id='{self.id}', name='{self.name}')>"
