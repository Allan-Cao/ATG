from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base, PlayerTeamAssociation


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    grid_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    # Multiple teams can share the same team_code due to inconsistancies in GRID/Bayes data e.x. academy teams share
    # the same team code as their main team for some weird reason.
    team_code: Mapped[Optional[str]] = mapped_column(String(5), unique=False)
    riot_esports_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String())
    colour_primary: Mapped[Optional[str]] = mapped_column(String(7))
    colour_secondary: Mapped[Optional[str]] = mapped_column(String(7))

    player_associations: Mapped[List["PlayerTeamAssociation"]] = relationship(
        "PlayerTeamAssociation", back_populates="team"
    )

    def __repr__(self):
        return f"<Team(id='{self.id}', code='{self.code}')>"
