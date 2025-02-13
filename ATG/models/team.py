from sqlalchemy import Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from .player_team_association import PlayerTeamAssociation


class Team(Base):
    __tablename__ = "teams"

    # For consistancy, we use an integer id primary key, however practically, it is good to set this as the GRID ID (even though it is originally a string)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Multiple teams can share the same name in the GRID and LoL Esports APIs
    name: Mapped[str] = mapped_column(Text, unique=False)
    # Multiple teams can share the same team code due to inconsistancies in GRID/Bayes data e.x. academy teams share team codes with their main team
    team_code: Mapped[str | None] = mapped_column(Text, unique=False, nullable=True)
    # We can store GRID, LOL IDs here
    external_ids = mapped_column(JSONB)

    # We store additional information in a JSONB blob
    additional_details = mapped_column(JSONB)

    player_associations: Mapped[list["PlayerTeamAssociation"]] = relationship(
        "PlayerTeamAssociation", back_populates="team"
    )

    def __repr__(self):
        return f"<Team(id='{self.id}', code='{self.name}')>"
