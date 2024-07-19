import sys

sys.path.append("..")
from dotenv import load_dotenv

load_dotenv("../.env")
from sqlalchemy import select, func, desc, and_, case
from SQDBI.database import Session
from SQDBI.models import *

from typing import Optional, Union
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root() -> Union[str, dict]:
    return {"Hello": "World"}


@app.get("/players/available_players")
def get_available_players() -> list:
    with Session() as session:
        statement = select(Player.name)
        rows = session.execute(statement).all()
        if len(rows) == 0:
            return []
        else:
            return [_[0] for _ in rows]


@app.get("/players/get_player_team/{player_name}")
def get_player_team(player_name: str) -> Union[None, str]:
    with Session() as session:
        player = session.scalar(select(Player).where(Player.name == player_name))

        if player is None:
            raise HTTPException(status_code=400, detail="Unknown player_name received")

        statement = (
            select(Team.code)
            .join(PlayerTeamAssociation, Team.id == PlayerTeamAssociation.team_id)
            .join(Player, Player.id == PlayerTeamAssociation.player_id)
            .where(Player.id == player.id)
        )
        return session.scalar(statement)


@app.get("/stats/{by_player_name}")
def get_player_stats_by_name(player_name: str) -> list[dict]:
    with Session() as session:
        statement = (
            select(Account.puuid)
            .join(Player, Player.id == Account.player_id)
            .where(Player.name == player_name)
        )
        player_accounts = session.scalars(statement)

        if player_accounts is None:
            raise HTTPException(status_code=400, detail="Unknown player_name received")

        print(player_accounts)

        statement = (
            select(
                Participant.champion_id.label("Champion"),
                func.count(Participant.champion_id).label("Games"),
                func.avg(Participant.kda).label("KDA"),
            )
            # .join(Game, Participant.game)
            .where(Participant.puuid.in_(player_accounts))
            .group_by("Champion")
            .order_by(desc("Games"))
            .limit(20)
        )

        results = session.execute(statement).all()
        return [
            {
                "Champion": row.Champion,
                "Games": row.Games,
                "KDA": row.KDA,
            }
            for row in results
        ]
