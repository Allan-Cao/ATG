from datetime import datetime
from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Tournament(Base):
    __tablename__ = "tournaments"
    # Same as with team, for consistancy, we use an integer id primary key.
    # Practically, we store GRID ID's here (even though GRID IDs are typed as string by GRID)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Tournament Name
    name: Mapped[str] = mapped_column(Text)
    # We should automatically parse the tournament year / league / split from its name for easy searching
    year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    league: Mapped[str | None] = mapped_column(Text, nullable=True)
    split: Mapped[str | None] = mapped_column(Text, nullable=True)

    # For now, these are generally NULL, in the future we should automatically set based on first/last games
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Additional tournament information can be stored here
    tournament_details = mapped_column(JSONB)
