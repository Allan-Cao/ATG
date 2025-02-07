from sqlalchemy import ForeignKey, Text, Integer, Boolean, DateTime, Float, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn
from datetime import datetime
from .base import Base


class Participant(Base):
    __tablename__ = "participants"
    # ParticipantDto
    assists: Mapped[int] = mapped_column(Integer)
    champion_id: Mapped[int] = mapped_column(Integer)
    champion_name: Mapped[str] = mapped_column(Text)
    deaths: Mapped[int] = mapped_column(Integer)
    game_ended_in_early_surrender: Mapped[bool] = mapped_column(Boolean)
    game_ended_in_surrender: Mapped[bool] = mapped_column(Boolean)
    kills: Mapped[int] = mapped_column(Integer)
    puuid: Mapped[str] = mapped_column(Text)
    riot_id_game_name: Mapped[str] = mapped_column(Text)
    riot_id_tagline: Mapped[str] = mapped_column(Text)
    summoner_id: Mapped[str] = mapped_column(Text)
    summoner_name: Mapped[str] = mapped_column(Text)
    team_id: Mapped[int] = mapped_column(Integer)
    team_position: Mapped[str] = mapped_column(Text)
    win: Mapped[bool] = mapped_column(Boolean)
    # Calculated stats (will likely remove in the future)
    total_minions_killed: Mapped[int] = mapped_column(Integer)
    neutral_minions_killed: Mapped[int] = mapped_column(Integer)
    # Automatically generate the stored_keys
    PARTICIPANT_DTO = [name for name, value in locals().items() if isinstance(value, MappedColumn)]

    # We need to move these declarations below the auto generation
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(Text, ForeignKey("games.id"))
    game_duration: Mapped[int] = mapped_column(Integer)  # in seconds

    # Calculated stats
    kda: Mapped[float | None] = mapped_column(Float)
    total_cs: Mapped[int | None] = mapped_column(Integer)
    cspm: Mapped[float | None] = mapped_column(Float)

    # Stored JSONs
    challenges = mapped_column(JSONB)
    missions = mapped_column(JSONB)
    perks = mapped_column(JSONB)
    STORED_DTOS = [name for name, value in locals().items() if isinstance(value, MappedColumn) and isinstance(value.column.type, JSONB)]
    # We store the ParticipantDto - the above stored JSONs here
    participant = mapped_column(JSONB)

    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kda = self.calculate_kda()
        self.total_cs = self.calculate_total_cs()
        self.cspm = self.calculate_cspm()

    def calculate_kda(self) -> float | None:
        if self.kills is None or self.assists is None or self.deaths is None:
            return None
        if self.deaths > 0:
            return (self.kills + self.assists) / self.deaths
        return self.kills + self.assists

    def calculate_total_cs(self) -> int | None:
        if (
            self.total_minions_killed is None
            or self.neutral_minions_killed is None
        ):
            return None
        return self.total_minions_killed + self.neutral_minions_killed

    def calculate_cspm(self) -> float | None:
        if (
            self.total_cs is None
            or self.game_duration is None
            or self.game_duration == 0
        ):
            return None
        return self.total_cs / (self.game_duration / 60)

    def __repr__(self):
        return f"{self.game_id}-{self.riot_id_game_name}#{self.riot_id_tagline} on {self.champion_name}"
