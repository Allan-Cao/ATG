from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.base import Base
from datetime import datetime
from SQDBI.models.participant import Participant

from SQDBI.models.player import Player


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    puuid: Mapped[str] = Column(String(255), unique=True)
    account_name: Mapped[str] = Column(String(255))
    account_tagline: Mapped[str] = Column(String(255))
    region: Mapped[str] = Column(String(50))
    last_update: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    latest_game: Mapped[Optional[datetime]] = Column(DateTime, nullable=True)

    player_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("players.id"))

    player: Mapped[Optional["Player"]] = relationship(
        "Player", back_populates="accounts"
    )
    games: Mapped[List["Participant"]] = relationship(
        "Participant", back_populates="account"
    )

    def __repr__(self) -> str:
        return f"<Account(id='{self.id}', {self.account_name}#{self.account_tagline}, region='{self.region}')>"

    def __str__(self) -> str:
        return f"{self.account_name}#{self.account_tagline}"
