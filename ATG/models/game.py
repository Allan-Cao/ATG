from sqlalchemy import ForeignKey, Text, Integer, BigInteger, DateTime, func, Index, text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedColumn
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .base import Base


class Game(Base):
    __tablename__ = "games"
    # InfoDto
    end_of_game_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    game_creation: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    game_duration: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # in seconds
    game_end_timestamp: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    game_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )  # Riot's game id
    game_mode: Mapped[str | None] = mapped_column(Text, nullable=True)
    game_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    game_start_timestamp: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    game_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    game_version: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Riot game version
    map_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    platform_id: Mapped[str | None] = mapped_column(Text, nullable=True)  # e.g. EUW1
    queue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tournament_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    INFO_DTO = [
        name for name, value in locals().items() if isinstance(value, MappedColumn)
    ]
    
    game_ended_in_early_surrender: Mapped[bool | None] = mapped_column(Boolean)
    game_ended_in_surrender: Mapped[bool | None] = mapped_column(Boolean)

    # Equivalent to matchId in the MatchV5 API (e.x. NA1_12345)
    id: Mapped[str] = mapped_column(Text, primary_key=True)
    # ParticipantDto
    participants: Mapped[list["Participant"]] = relationship()
    # TeamDto
    teams: Mapped[list["TeamDto"]] = relationship()

    # We can store additional info flexibly here
    additional_details = mapped_column(JSONB)
    # Tournament Game Information
    tournament_id: Mapped[int | None] = mapped_column(
        ForeignKey("tournaments.id"), nullable=True
    )
    # Esports Game Information (GRID)
    series_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    series_game_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    @hybrid_property
    def patch(self): # type: ignore
        version_split = self.game_version.split(".")
        return (
            f"{version_split[0]}.{version_split[1]}"
            if len(version_split) >= 2
            else None
        )

    @patch.expression
    def patch(cls):
        return func.concat(
            func.split_part(cls.game_version, ".", 1),
            ".",
            func.split_part(cls.game_version, ".", 2),
        )

    __table_args__ = (
        Index("idx_games_queue_id", "queue_id"),
        Index("idx_games_end_timestamp", text("game_end_timestamp DESC")),
        Index("idx_game_queue_timestamp", "queue_id", text("game_end_timestamp DESC")),
    )