from typing import List, Optional
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.functions import func
from datetime import datetime
from SQDBI.models import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    puuid: Mapped[str] = mapped_column(String(255), unique=True)
    account_name: Mapped[str] = mapped_column(String(255))
    account_tagline: Mapped[str] = mapped_column(String(255))
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    last_update: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )  # last time we updated the account details
    latest_game: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    # last time a new game was added to the database (used for match history ingestion)

    player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("players.id"))

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
