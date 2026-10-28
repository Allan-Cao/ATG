from sqlalchemy import Integer, Text, ForeignKey, Date, DateTime, Index, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, datetime
from .base import Base


class PlayerTeamAssociation(Base):
    __tablename__ = "player_team_associations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    team_id: Mapped[str] = mapped_column(Text, ForeignKey("teams.id"))
    # Although not explicitly enforced, the (TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY) is generally used
    position: Mapped[str | None] = mapped_column(Text, nullable=True)
    # A NULL end_date means the player is currently on the team
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Debug
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    player: Mapped["Player"] = relationship(
        "Player", back_populates="team_associations"
    )
    team: Mapped["Team"] = relationship("Team", back_populates="player_associations")

    __table_args__ = (
        Index(
            "uq_player_team_associations",
            "player_id",
            "team_id",
            "position",
            "start_date",
            unique=True,
            postgresql_nulls_not_distinct=True,
        ),
        Index("idx_player_team_associations_team_id", "team_id"),
    )

    def __repr__(self):
        return f"<PlayerTeamAssociation(id='{self.id}', player_id='{self.player_id}', team_id='{self.team_id}', position='{self.position}')>"
