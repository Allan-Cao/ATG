from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    Float,
    func,
    case,
    type_coerce,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, MappedColumn, relationship
from datetime import datetime
from .base import Base


class ParticipantStat(Base):
    __tablename__ = "participant_stats"
    # This first section is for innate stats which should always be available
    # thus are not nullable. Where possible, we keep the original Match-V5 column name.
    kills: Mapped[int] = mapped_column(Integer)
    deaths: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    # Total *lane* minions killed.
    total_minions_killed: Mapped[int] = mapped_column(Integer)
    # Total *jungle* minions killed.
    neutral_minions_killed: Mapped[int] = mapped_column(Integer)

    # 0 if the item slot is empty. Should be a foreign key in the future.
    item_0: Mapped[int] = mapped_column(Integer, default=0)
    item_1: Mapped[int] = mapped_column(Integer, default=0)
    item_2: Mapped[int] = mapped_column(Integer, default=0)
    item_3: Mapped[int] = mapped_column(Integer, default=0)
    item_4: Mapped[int] = mapped_column(Integer, default=0)
    item_5: Mapped[int] = mapped_column(Integer, default=0)
    item_6: Mapped[int] = mapped_column(Integer, default=0)  # Trinket

    # Should also be a foreign key in the future.
    summoner_1_id: Mapped[int] = mapped_column(Integer)
    summoner_2_id: Mapped[int] = mapped_column(Integer)

    # We use this to automatically grab the data from the MatchV5 participant json
    PARTICIPANT_STAT_DTO = [
        name for name, value in locals().items() if isinstance(value, MappedColumn)
    ]

    # Calculated Stats
    # This section will eventualy store stats that require additional processing and thus can be nullable.
    # I am not sure if it's best to store them as columns or as an additional JSONB field.
    # e.x. jng_prox, cs_8, cs_15, csd_15

    # This JSONB column to stores the rest of the Match-V5 data for future use
    source_data = mapped_column(JSONB)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    participant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("participants.id"), unique=True
    )

    participant: Mapped["Participant"] = relationship(
        "Participant", back_populates="stats"
    )

    @classmethod
    def _game_duration_minutes(cls):
        from .participant import Participant
        from .game import Game

        return (
            select(Game.game_duration / 60)
            .join(Participant, Participant.game_id == Game.id)
            .where(Participant.id == cls.participant_id)
            .scalar_subquery()
        )

    @hybrid_property
    def cs(self) -> int:
        return self.total_minions_killed + self.neutral_minions_killed

    @cs.expression
    @classmethod
    def cs(cls):
        return type_coerce(
            cls.total_minions_killed + cls.neutral_minions_killed, Integer
        )

    @hybrid_property
    def cspm(self) -> float | None:
        return self.cs / (self.participant.game.game_duration / 60)

    @cspm.expression
    @classmethod
    def cspm(cls):
        return type_coerce(cls.cs / (cls._game_duration_minutes()), Float)

    @hybrid_property
    def kda(self) -> float:
        if self.deaths > 0:
            return (self.kills + self.assists) / self.deaths
        return self.kills + self.assists

    @kda.expression
    @classmethod
    def kda(cls):
        return case(
            (cls.deaths > 0, (cls.kills + cls.assists) / cls.deaths),
            else_=(cls.kills + cls.assists),
        )

    # Debug
    updated: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
