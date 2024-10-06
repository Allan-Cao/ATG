from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.types import SmallInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base


class Tournament(Base):
    __tablename__ = "tournaments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # GRID Tournament ID
    grid_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Tournament Name
    name: Mapped[str] = mapped_column(String(255))
    # GRID offers a "shortened name" limited to 30 characters
    shortened_name: Mapped[str | None] = mapped_column(String(30), nullable=True)
    # We automatically parse the tournament year / league / split from its name for easy searching
    year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    league: Mapped[str | None] = mapped_column(String(50), nullable=True)
    split: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # For now, these are generally NULL, in the future we should automatically set based on first/last games
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
