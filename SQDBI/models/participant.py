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
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.base import Base


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[str] = Column(String(255), ForeignKey("games.id"))
    game_duration: Mapped[int] = Column(Integer)
    puuid: Mapped[str] = Column(String(255))
    account_name: Mapped[str] = Column(String(255))
    account_tagline: Mapped[str] = Column(String(255))
    side: Mapped[str] = Column(String(10))
    win: Mapped[bool] = Column(Boolean)
    team_position: Mapped[str] = Column(String(10))
    lane: Mapped[str] = Column(String(10))
    champion: Mapped[str] = Column(String(255))
    champion_id: Mapped[int] = Column(Integer)
    kills: Mapped[int] = Column(Integer)
    deaths: Mapped[int] = Column(Integer)
    assists: Mapped[int] = Column(Integer)
    summoner1_id: Mapped[int] = Column(Integer)
    summoner2_id: Mapped[int] = Column(Integer)
    gold_earned: Mapped[int] = Column(Integer)
    total_minions_killed: Mapped[int] = Column(Integer)
    total_neutral_minions_killed: Mapped[int] = Column(Integer)
    total_ally_jungle_minions_killed: Mapped[int] = Column(Integer)
    total_enemy_jungle_minions_killed: Mapped[int] = Column(Integer)
    early_surrender: Mapped[bool] = Column(Boolean)
    surrender: Mapped[bool] = Column(Boolean)
    first_blood: Mapped[bool] = Column(Boolean)
    first_blood_assist: Mapped[bool] = Column(Boolean)
    first_tower: Mapped[bool] = Column(Boolean)
    first_tower_assist: Mapped[bool] = Column(Boolean)
    damage_dealt_to_buildings: Mapped[int] = Column(Integer)
    turret_kills: Mapped[int] = Column(Integer)
    turrets_lost: Mapped[int] = Column(Integer)
    damage_dealt_to_objectives: Mapped[int] = Column(Integer)
    dragon_kills: Mapped[int] = Column(Integer)
    objectives_stolen: Mapped[int] = Column(Integer)
    longest_time_spent_living: Mapped[int] = Column(Integer)
    largest_killing_spree: Mapped[int] = Column(Integer)
    total_damage_dealt_champions: Mapped[int] = Column(Integer)
    total_damage_taken: Mapped[int] = Column(Integer)
    total_damage_self_mitigated: Mapped[int] = Column(Integer)
    total_damage_shielded_teammates: Mapped[int] = Column(Integer)
    total_heals_teammates: Mapped[int] = Column(Integer)
    total_time_crowd_controlled: Mapped[int] = Column(Integer)
    total_time_spent_dead: Mapped[int] = Column(Integer)
    vision_score: Mapped[int] = Column(Integer)
    wards_killed: Mapped[int] = Column(Integer)
    wards_placed: Mapped[int] = Column(Integer)
    control_wards_placed: Mapped[int] = Column(Integer)
    item0: Mapped[int] = Column(Integer)
    item1: Mapped[int] = Column(Integer)
    item2: Mapped[int] = Column(Integer)
    item3: Mapped[int] = Column(Integer)
    item4: Mapped[int] = Column(Integer)
    item5: Mapped[int] = Column(Integer)
    item6: Mapped[int] = Column(Integer)
    perk_keystone: Mapped[int] = Column(Integer)
    perk_primary_row_1: Mapped[int] = Column(Integer)
    perk_primary_row_2: Mapped[int] = Column(Integer)
    perk_primary_row_3: Mapped[int] = Column(Integer)
    perk_secondary_row_1: Mapped[int] = Column(Integer)
    perk_secondary_row_2: Mapped[int] = Column(Integer)
    perk_primary_style: Mapped[int] = Column(Integer)
    perk_secondary_style: Mapped[int] = Column(Integer)
    perk_shard_defense: Mapped[int] = Column(Integer)
    perk_shard_flex: Mapped[int] = Column(Integer)
    perk_shard_offense: Mapped[int] = Column(Integer)

    account_puuid: Mapped[Optional[str]] = Column(
        String(255), ForeignKey("accounts.puuid")
    )
    player_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("players.id"))

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
