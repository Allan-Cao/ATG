from sqlalchemy import ForeignKey, Text, Integer, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedColumn
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from .base import Base


class Game(Base):
    __tablename__ = "games"
    # InfoDto
    end_of_game_result: Mapped[str] = mapped_column(Text)
    game_creation: Mapped[int] = mapped_column(BigInteger)
    game_duration: Mapped[int] = mapped_column(Integer)  # in seconds
    game_end_timestamp: Mapped[int] = mapped_column(BigInteger)
    game_id: Mapped[int] = mapped_column(BigInteger)  # Riot's game id
    game_mode: Mapped[str] = mapped_column(Text)
    game_name: Mapped[str] = mapped_column(Text)
    game_start_timestamp: Mapped[int] = mapped_column(BigInteger)
    game_type: Mapped[str] = mapped_column(Text)
    game_version: Mapped[str] = mapped_column(Text) # Riot game version
    map_id: Mapped[int] = mapped_column(Integer)
    platform_id: Mapped[str] = mapped_column(Text)  # e.g. EUW1
    queue_id: Mapped[int] = mapped_column(Integer)
    tournament_code: Mapped[str] = mapped_column(Text)
    INFO_DTO = [name for name, value in locals().items() if isinstance(value, MappedColumn)]

    # Equivalent to matchId in the MatchV5 API (e.x. NA1_12345)
    id: Mapped[str] = mapped_column(
        Text, primary_key=True
    )
    # ParticipantDto
    participants: Mapped[list["Participant"]] = relationship()
    # TeamDto
    teams: Mapped[list["TeamDto"]] = relationship()

    # Tournament Game Information
    tournament_id: Mapped[int | None] = mapped_column(ForeignKey("tournaments.id"), nullable=True)
    # Esports Game Information (GRID)
    series_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    series_game_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    @hybrid_property
    def patch(self):
        version_split = self.game_version.split(".")
        return f"{version_split[0]}.{version_split[1]}" if len(version_split) >= 2 else None

    @patch.expression
    def patch(cls):
        return func.concat(
            func.split_part(cls.game_version, ".", 1),
            ".",
            func.split_part(cls.game_version, ".", 2)
        )
