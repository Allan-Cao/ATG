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
    # Tournament Realm accounts technically have name/taglines (something#eProd) but this changes when a player moves teams
    # so we don't store them for TR accounts
    account_name: Mapped[Optional[str]] = mapped_column(String(255))
    account_tagline: Mapped[Optional[str]] = mapped_column(String(255))
    # Regions should be set on insertion
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    # Last time an update occured on the account name/tagline/when the account was inserted
    last_update: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    # Last time a new game was added to the database (used for match history ingestion)
    latest_game: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    # We require that all tracked accounts are associated with a player
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))

    player: Mapped["Player"] = relationship("Player", back_populates="accounts")

    def __repr__(self) -> str:
        return f"<Account(id='{self.id}', {self.account_name}#{self.account_tagline}, region='{self.region}')>"

    def __str__(self) -> str:
        return f"{self.account_name}#{self.account_tagline}"
