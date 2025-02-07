from sqlalchemy import Integer, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class TeamDto(Base):
    __tablename__ = "team_dtos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))

    # TeamDto
    bans = mapped_column(JSONB)
    objectives = mapped_column(JSONB)
    team_id: Mapped[int] = mapped_column(Integer)
    win: Mapped[bool] = mapped_column(Boolean)
