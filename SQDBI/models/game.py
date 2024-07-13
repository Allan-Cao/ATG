from typing import List
from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models import Base
from datetime import datetime


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = Column(
        String(255), primary_key=True
    )  # Complete game id containing region and game id (e.g. EUW1_1234567890)
    game_id: Mapped[int] = Column(BigInteger)  # Riot's game id
    platform_id: Mapped[str] = Column(String(50))  # e.g. EUW1
    game_creation: Mapped[int] = Column(BigInteger)
    game_start: Mapped[int] = Column(BigInteger)
    game_end: Mapped[int] = Column(BigInteger)
    game_duration: Mapped[int] = Column(Integer)  # in seconds

    game_type: Mapped[str] = Column(String(50))
    game_version_major: Mapped[int] = Column(Integer())
    game_version_minor: Mapped[int] = Column(Integer())

    queue_id: Mapped[int] = Column(Integer)

    participants: Mapped[List["Participant"]] = relationship(
        "Participant", back_populates="game"
    )
