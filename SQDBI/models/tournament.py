from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    # For now, id and grid_id are the same but in the future we may store games from different sources with string ids
    grid_id: Mapped[str | None] = mapped_column(String(50))
    league: Mapped[str | None] = mapped_column(String(50))  # e.g. LCS/NACL
    split: Mapped[str | None] = mapped_column(String(50))  # e.g. Spring/Summer
    playoffs: Mapped[bool | None] = mapped_column(Boolean)
