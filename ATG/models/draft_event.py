from sqlalchemy import Integer, Text, ForeignKey, DateTime, func, Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class DraftEvent(Base):
    __tablename__ = "draft_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))
    champion: Mapped[int] = mapped_column(Integer, ForeignKey("champions.id"))
    # Derived from game_info based on champion_id
    participant_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # True if pick event, false if ban event
    is_pick: Mapped[bool] = mapped_column(Boolean)
    # True if first 3 bans/picks, False if last 2 picks/bans
    is_phase_one: Mapped[bool] = mapped_column(Boolean)
    # True if blue team, false if red team (100 / 200)
    is_blue: Mapped[bool] = mapped_column(Boolean)
    # Draft turn (blue1, red2, red3, blue4, blue5, red6, red7, blue8, blue9, red10)
    pick_turn: Mapped[int] = mapped_column(Integer)
    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now())
