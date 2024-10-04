from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Base, PlayerTeamAssociation


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    grid_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    # Multiple teams can share the same team_code due to inconsistancies in GRID/Bayes data e.x. academy teams share
    # the same team code as their main team for some weird reason.
    team_code: Mapped[str | None] = mapped_column(String(5), unique=False)
    # We store both GRID and RIOT esports IDs as Strings
    riot_esports_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    logo_url: Mapped[str | None] = mapped_column(String())
    colour_primary: Mapped[str | None] = mapped_column(String(7))
    colour_secondary: Mapped[str | None] = mapped_column(String(7))

    player_associations: Mapped[list["PlayerTeamAssociation"]] = relationship(
        "PlayerTeamAssociation", back_populates="team"
    )

    def __repr__(self):
        return f"<Team(id='{self.id}', code='{self.code}')>"
