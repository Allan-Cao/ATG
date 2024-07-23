from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Account, Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))

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
