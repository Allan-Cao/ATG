from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class GameEvent(Base):
    __tablename__ = "game_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))
    # rfc461Schema (identifies the event type)
    schema: Mapped[str] = mapped_column(Text)
    sequence_index: Mapped[int] = mapped_column(Integer)
    # Missing from 'champ_select', 'game_info' type events
    game_time: Mapped[int] = mapped_column(Integer)

    # This field flexibly stores the rest of the relevant fields
    additional_details = mapped_column(JSONB)
