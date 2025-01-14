from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.types import SmallInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from .base import Base
from ..api.utils import server_string


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # This either the actual PUUID as per the Riot API OR Riot Esports API IDs
    puuid: Mapped[str] = mapped_column(String(255), unique=True)
    # Tournament Realm accounts technically have name/taglines (something#eProd) but this changes when a player moves teams
    # so we don't store them for TR accounts
    account_name: Mapped[str | None] = mapped_column(String(255))
    account_tagline: Mapped[str | None] = mapped_column(String(255))
    # Regions should be set on insertion
    # Exceptions to the normal Riot API regions include TOURNAMENT (for TR accounts) and RIOT_LOL (for Riot Esports API)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    # Last time an update occured on the account name/tagline/when the account was inserted
    last_update: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    # Last time a new game was added to the database (used for match history ingestion)
    latest_game: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    # Player id associated with the tracked account
    player_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("players.id"))
    # We need a way to flag inactive / non-match history tracked accounts
    skip_update: Mapped[bool] = mapped_column(Boolean, default=False)
    # We use an binary integer flag to save account details.
    account_details: Mapped[int] = mapped_column(SmallInteger, default=0)

    # We can use the server_string to define a class-level property to help us determine if an account is a solo queue account
    @hybrid_property
    def solo_queue_account(self) -> bool:
        return self.region in server_string.keys()

    player: Mapped["Player"] = relationship("Player", back_populates="accounts")

    def __repr__(self) -> str:
        return f"<Account(id='{self.id}', {self.account_name}#{self.account_tagline}, region='{self.region}')>"

    def __str__(self) -> str:
        return f"{self.account_name}#{self.account_tagline}"
