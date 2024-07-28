from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    BigInteger,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = mapped_column(String(255), ForeignKey("games.id"))
    game_duration: Mapped[Optional[int]] = mapped_column(Integer)
    puuid: Mapped[str] = mapped_column(String(255))
    account_name: Mapped[Optional[str]] = mapped_column(String(255))
    account_tagline: Mapped[Optional[str]] = mapped_column(String(255))
    side: Mapped[str] = mapped_column(String(10))
    win: Mapped[bool] = mapped_column(Boolean)
    team_position: Mapped[Optional[str]] = mapped_column(String(10))
    lane: Mapped[Optional[str]] = mapped_column(String(10))
    champion: Mapped[str] = mapped_column(String(255))
    champion_id: Mapped[int] = mapped_column(Integer)
    kills: Mapped[Optional[int]] = mapped_column(Integer)
    deaths: Mapped[Optional[int]] = mapped_column(Integer)
    assists: Mapped[Optional[int]] = mapped_column(Integer)
    summoner1_id: Mapped[Optional[int]] = mapped_column(Integer)
    summoner2_id: Mapped[Optional[int]] = mapped_column(Integer)
    gold_earned: Mapped[Optional[int]] = mapped_column(Integer)
    total_minions_killed: Mapped[Optional[int]] = mapped_column(Integer)
    total_neutral_minions_killed: Mapped[Optional[int]] = mapped_column(Integer)
    total_ally_jungle_minions_killed: Mapped[Optional[int]] = mapped_column(Integer)
    total_enemy_jungle_minions_killed: Mapped[Optional[int]] = mapped_column(Integer)
    early_surrender: Mapped[Optional[bool]] = mapped_column(Boolean)
    surrender: Mapped[Optional[bool]] = mapped_column(Boolean)
    first_blood: Mapped[Optional[bool]] = mapped_column(Boolean)
    first_blood_assist: Mapped[Optional[bool]] = mapped_column(Boolean)
    first_tower: Mapped[Optional[bool]] = mapped_column(Boolean)
    first_tower_assist: Mapped[Optional[bool]] = mapped_column(Boolean)
    damage_dealt_to_buildings: Mapped[Optional[int]] = mapped_column(Integer)
    turret_kills: Mapped[Optional[int]] = mapped_column(Integer)
    turrets_lost: Mapped[Optional[int]] = mapped_column(Integer)
    damage_dealt_to_objectives: Mapped[Optional[int]] = mapped_column(Integer)
    dragon_kills: Mapped[Optional[int]] = mapped_column(Integer)
    objectives_stolen: Mapped[Optional[int]] = mapped_column(Integer)
    longest_time_spent_living: Mapped[Optional[int]] = mapped_column(Integer)
    largest_killing_spree: Mapped[Optional[int]] = mapped_column(Integer)
    total_damage_dealt_champions: Mapped[Optional[int]] = mapped_column(Integer)
    total_damage_taken: Mapped[Optional[int]] = mapped_column(Integer)
    total_damage_self_mitigated: Mapped[Optional[int]] = mapped_column(Integer)
    total_damage_shielded_teammates: Mapped[Optional[int]] = mapped_column(Integer)
    total_heals_teammates: Mapped[Optional[int]] = mapped_column(Integer)
    total_time_crowd_controlled: Mapped[Optional[int]] = mapped_column(Integer)
    total_time_spent_dead: Mapped[Optional[int]] = mapped_column(Integer)
    vision_score: Mapped[Optional[int]] = mapped_column(Integer)
    wards_killed: Mapped[Optional[int]] = mapped_column(Integer)
    wards_placed: Mapped[Optional[int]] = mapped_column(Integer)
    control_wards_placed: Mapped[Optional[int]] = mapped_column(Integer)
    item0: Mapped[Optional[int]] = mapped_column(Integer)
    item1: Mapped[Optional[int]] = mapped_column(Integer)
    item2: Mapped[Optional[int]] = mapped_column(Integer)
    item3: Mapped[Optional[int]] = mapped_column(Integer)
    item4: Mapped[Optional[int]] = mapped_column(Integer)
    item5: Mapped[Optional[int]] = mapped_column(Integer)
    item6: Mapped[Optional[int]] = mapped_column(Integer)
    perk_keystone: Mapped[Optional[int]] = mapped_column(Integer)
    perk_primary_row_1: Mapped[Optional[int]] = mapped_column(Integer)
    perk_primary_row_2: Mapped[Optional[int]] = mapped_column(Integer)
    perk_primary_row_3: Mapped[Optional[int]] = mapped_column(Integer)
    perk_secondary_row_1: Mapped[Optional[int]] = mapped_column(Integer)
    perk_secondary_row_2: Mapped[Optional[int]] = mapped_column(Integer)
    perk_primary_style: Mapped[Optional[int]] = mapped_column(Integer)
    perk_secondary_style: Mapped[Optional[int]] = mapped_column(Integer)
    perk_shard_defense: Mapped[Optional[int]] = mapped_column(Integer)
    perk_shard_flex: Mapped[Optional[int]] = mapped_column(Integer)
    perk_shard_offense: Mapped[Optional[int]] = mapped_column(Integer)
    kda: Mapped[Optional[float]] = mapped_column(nullable=False)
    total_cs: Mapped[Optional[int]] = mapped_column(nullable=False)
    cspm: Mapped[Optional[float]] = mapped_column(nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kda = self.calculate_kda()
        self.total_cs = self.calculate_total_cs()
        self.cspm = self.calculate_cspm()

    def calculate_kda(self) -> Optional[float]:
        if self.kills is None or self.assists is None or self.deaths is None:
            return None
        if self.deaths > 0:
            return (self.kills + self.assists) / self.deaths
        return self.kills + self.assists

    def calculate_total_cs(self) -> Optional[int]:
        if (
            self.total_minions_killed is None
            or self.total_neutral_minions_killed is None
        ):
            return None
        return self.total_minions_killed + self.total_neutral_minions_killed

    def calculate_cspm(self) -> Optional[float]:
        if self.total_cs is None or self.game_duration is None:
            return None
        return self.total_cs / (self.game_duration / 60)
