from typing import List
from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from sqlalchemy.orm import relationship, Mapped
from SQDBI.models.base import Base
from datetime import datetime

from SQDBI.models.participant import Participant


class Game(Base):
    __tablename__ = "games"

    id: Mapped[str] = Column(
        String(255), primary_key=True
    )  # Complete game id containing region and game id (e.g. EUW1_1234567890)
    game_id: Mapped[int] = Column(BigInteger)  # Riot's game id
    platform_id: Mapped[str] = Column(String(50))  # e.g. EUW1
    game_creation: Mapped[datetime] = Column(DateTime)
    game_start: Mapped[datetime] = Column(DateTime)
    game_end: Mapped[datetime] = Column(DateTime)
    game_duration: Mapped[int] = Column(Integer)  # in seconds

    game_type: Mapped[str] = Column(String(50))
    game_version: Mapped[str] = Column(String(50))

    queue_id: Mapped[int] = Column(Integer)

    participants: Mapped[List["Participant"]] = relationship(
        "Participant", back_populates="game"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_version_major_minor = self.extract_major_minor_version()

    def extract_major_minor_version(self):
        if self.game_version:
            version_parts = self.game_version.split(".")
            if len(version_parts) >= 2:
                return f"{version_parts[0]}.{version_parts[1]}"
        return None
