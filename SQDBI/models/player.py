from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Account, Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Not sure how to deal with naming conflicts. For now, we assume that names can be repeated but we can use the column below.
    name: Mapped[str] = mapped_column(String(255))
    # We store the name used on Leaguepedia/Oracles Elixer here for easier use with those services.
    # For now, this should be their Leaguepedia disambiguation name
    disambiguation: Mapped[Optional[str]] = mapped_column(String(255), unique=True)

    accounts: Mapped[Optional[List["Account"]]] = relationship(
        "Account", back_populates="player"
    )
    team_associations: Mapped[Optional[List["PlayerTeamAssociation"]]] = relationship(
        "PlayerTeamAssociation", back_populates="player"
    )
    solo_queue_games: Mapped[Optional[List["Participant"]]] = relationship(
        "Participant", back_populates="player"
    )

    def __repr__(self) -> str:
        if self.disambiguation is None:
            return f"{self.name}:{self.id}"
        return f"{self.name}-{self.disambiguation}:{self.id}"
