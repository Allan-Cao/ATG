from sqlalchemy import Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class DraftEvent(Base):
    __tablename__ = "draft_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))
    # While there *should* be a foreign key relationship with champions.id,
    # we do not require it for now. left as a future TODO
    champion_id: Mapped[int] = mapped_column(Integer)
    # True if pick event, false if ban event
    is_pick: Mapped[bool] = mapped_column(Boolean)
    # True if first 3 bans/picks, False if last 2 picks/bans
    is_phase_one: Mapped[bool] = mapped_column(Boolean)
    # True if blue team, false if red team (100 / 200)
    is_blue: Mapped[bool] = mapped_column(Boolean)
    # Draft turn phase 1 - (1, 2, 3, 4, 5, 6) -> phase 2 - (1, 2, 3, 4)
    pick_turn: Mapped[int] = mapped_column(Integer)
