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
    game_duration: Mapped[int] = mapped_column(Integer)
    puuid: Mapped[str] = mapped_column(String(255))
    account_name: Mapped[str] = mapped_column(String(255))
    account_tagline: Mapped[str] = mapped_column(String(255))
    side: Mapped[str] = mapped_column(String(10))
    win: Mapped[bool] = mapped_column(Boolean)
    team_position: Mapped[str] = mapped_column(String(10))
    lane: Mapped[str] = mapped_column(String(10))
    champion: Mapped[str] = mapped_column(String(255))
    champion_id: Mapped[int] = mapped_column(Integer)
    kills: Mapped[int] = mapped_column(Integer)
    deaths: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    summoner1_id: Mapped[int] = mapped_column(Integer)
    summoner2_id: Mapped[int] = mapped_column(Integer)
    gold_earned: Mapped[int] = mapped_column(Integer)
    total_minions_killed: Mapped[int] = mapped_column(Integer)
    total_neutral_minions_killed: Mapped[int] = mapped_column(Integer)
    total_ally_jungle_minions_killed: Mapped[int] = mapped_column(Integer)
    total_enemy_jungle_minions_killed: Mapped[int] = mapped_column(Integer)
    early_surrender: Mapped[bool] = mapped_column(Boolean)
    surrender: Mapped[bool] = mapped_column(Boolean)
    first_blood: Mapped[bool] = mapped_column(Boolean)
    first_blood_assist: Mapped[bool] = mapped_column(Boolean)
    first_tower: Mapped[bool] = mapped_column(Boolean)
    first_tower_assist: Mapped[bool] = mapped_column(Boolean)
    damage_dealt_to_buildings: Mapped[int] = mapped_column(Integer)
    turret_kills: Mapped[int] = mapped_column(Integer)
    turrets_lost: Mapped[int] = mapped_column(Integer)
    damage_dealt_to_objectives: Mapped[int] = mapped_column(Integer)
    dragon_kills: Mapped[int] = mapped_column(Integer)
    objectives_stolen: Mapped[int] = mapped_column(Integer)
    longest_time_spent_living: Mapped[int] = mapped_column(Integer)
    largest_killing_spree: Mapped[int] = mapped_column(Integer)
    total_damage_dealt_champions: Mapped[int] = mapped_column(Integer)
    total_damage_taken: Mapped[int] = mapped_column(Integer)
    total_damage_self_mitigated: Mapped[int] = mapped_column(Integer)
    total_damage_shielded_teammates: Mapped[int] = mapped_column(Integer)
    total_heals_teammates: Mapped[int] = mapped_column(Integer)
    total_time_crowd_controlled: Mapped[int] = mapped_column(Integer)
    total_time_spent_dead: Mapped[int] = mapped_column(Integer)
    vision_score: Mapped[int] = mapped_column(Integer)
    wards_killed: Mapped[int] = mapped_column(Integer)
    wards_placed: Mapped[int] = mapped_column(Integer)
    control_wards_placed: Mapped[int] = mapped_column(Integer)
    item0: Mapped[int] = mapped_column(Integer)
    item1: Mapped[int] = mapped_column(Integer)
    item2: Mapped[int] = mapped_column(Integer)
    item3: Mapped[int] = mapped_column(Integer)
    item4: Mapped[int] = mapped_column(Integer)
    item5: Mapped[int] = mapped_column(Integer)
    item6: Mapped[int] = mapped_column(Integer)
    perk_keystone: Mapped[int] = mapped_column(Integer)
    perk_primary_row_1: Mapped[int] = mapped_column(Integer)
    perk_primary_row_2: Mapped[int] = mapped_column(Integer)
    perk_primary_row_3: Mapped[int] = mapped_column(Integer)
    perk_secondary_row_1: Mapped[int] = mapped_column(Integer)
    perk_secondary_row_2: Mapped[int] = mapped_column(Integer)
    perk_primary_style: Mapped[int] = mapped_column(Integer)
    perk_secondary_style: Mapped[int] = mapped_column(Integer)
    perk_shard_defense: Mapped[int] = mapped_column(Integer)
    perk_shard_flex: Mapped[int] = mapped_column(Integer)
    perk_shard_offense: Mapped[int] = mapped_column(Integer)

    account_puuid: Mapped[Optional[str]] = mapped_column(
        String(255), ForeignKey("accounts.puuid")
    )
    player_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("players.id"))

    game: Mapped["Game"] = relationship("Game", back_populates="participants")
    account: Mapped[Optional["Account"]] = relationship(
        "Account", back_populates="games"
    )
    player: Mapped[Optional["Player"]] = relationship(
        "Player", back_populates="solo_queue_games"
    )

    kda: Mapped[float] = mapped_column(nullable=False)
    total_cs: Mapped[int] = mapped_column(nullable=False)
    cspm: Mapped[float] = mapped_column(nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kda = self.calculate_kda()
        self.total_cs = self.calculate_total_cs()
        self.cspm = self.calculate_cspm()

    def calculate_kda(self) -> float:
        if self.deaths > 0:
            return (self.kills + self.assists) / self.deaths
        return self.kills + self.assists

    def calculate_total_cs(self) -> int:
        return self.total_minions_killed + self.total_neutral_minions_killed

    def calculate_cspm(self) -> float:
        return self.total_cs / (self.game_duration / 60)
