from sqlalchemy import Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .base import Base

# Data derived from the game_info event
class GameParticipant(Base):
    __tablename__ = "game_participants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))
    puuid: Mapped[str] = mapped_column(Text, ForeignKey("accounts.puuid"))
    # Integer from 1-10 "probably" means the position
    participant_id: Mapped[int] = mapped_column(Integer)
    # We are storing the display name since it contains team tri-code information
    display_name: Mapped[str] = mapped_column(Text)
    champion: Mapped[str] = mapped_column(Text, ForeignKey("champions.alias"))
    # Not sure what this is, assuming it's a Riot account ID
    account_id: Mapped[str] = mapped_column(Text)
    side: Mapped[int] = mapped_column(Integer) # 100 for blue, 200 for red

    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now())
