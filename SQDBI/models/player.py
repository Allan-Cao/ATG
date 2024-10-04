from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from SQDBI.models import Account, Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Not sure how to deal with naming conflicts. For now, we assume that names can be repeated but we can use the column below.
    name: Mapped[str] = mapped_column(String(255))
    # These *should* be unique and defined but we are storing non-GRID tracked players hence it should be nullable.
    grid_id: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    # We store the name used on Leaguepedia/Oracles Elixer here for easier use with those services.
    # For now, this should be their Leaguepedia disambiguation name
    disambiguation: Mapped[str | None] = mapped_column(String(255), unique=True)
    # We store the associated RIOT Esports API accounts in the account table too in a *weird* but appropriate format
    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="player")

    def __repr__(self) -> str:
        if self.disambiguation is None:
            return f"{self.name}:{self.id}"
        return f"{self.name}-{self.disambiguation}:{self.id}"
