import sys
import os

from SQDBI.api.account_v1 import get_account_by_puuid

sys.path.append("..")
from dotenv import load_dotenv

load_dotenv("../.shared.env")
from sqlalchemy import select, func, desc, and_, case
from sqlalchemy.exc import IntegrityError
from SQDBI.database import Session
from SQDBI.models import *
from SQDBI.api import get_account_by_riot_id
from typing import Annotated, Optional, Union
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

API_KEY = os.environ.get("RIOT_API")
app = FastAPI()


class NewAccount(BaseModel):
    riot_username: Optional[str] = Field(None, description="Account's riot username")
    riot_tagline: Optional[str] = Field(None, description="Account's riot tagline")
    puuid: Optional[str] = Field(None, description="Account's PUUID")
    region: Optional[str] = Field(None, description="Account's region e.g. NA, EUW")
    player_name: str


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


@app.post("/players/new_player/")
def create_new_player(name: Annotated[str, Body()]):
    with Session() as session:
        player = session.scalar(select(Player.id).where(Player.name == name))
        if player is not None:
            raise HTTPException(
                status_code=409, detail=f"Player with {name} already exists."
            )
        p = Player(name=name)
        session.add(p)
        session.commit()
    return name


@app.post("/players/new_account/")
def associate_new_account(new_account: NewAccount) -> dict:
    with Session() as session:
        player_id = session.scalar(
            select(Player.id).where(Player.name == new_account.player_name)
        )
        if player_id is None:
            raise HTTPException(status_code=400, detail="Unknown player name received")
        # We default to using the PUUID (since it's more accurate), then try the account/tagline
        try:
            if new_account.puuid is not None:
                new_account_details = get_account_by_puuid(new_account.puuid, API_KEY)
            elif (
                new_account.riot_username is not None
                and new_account.riot_tagline is not None
            ):
                new_account_details = get_account_by_riot_id(
                    new_account.riot_username, new_account.riot_tagline, API_KEY
                )
            else:
                raise ValueError(
                    "Expecting PUUID or Account/Tagline pair. No values were received."
                )
        except Exception as e:
            # Might want to handle 429/404 exceptions differently.
            raise HTTPException(status_code=400, detail=str(e))
        if new_account_details is None:
            raise HTTPException(
                status_code=400, detail="Invalid riot account details received"
            )
        new_account_obj = Account(
            puuid=new_account_details["puuid"],
            account_name=new_account_details.get("gameName"),
            account_tagline=new_account_details.get("tagLine"),
            player_id=player_id,
        )
        if new_account.region is not None:
            new_account_obj.region = new_account.region
        session.add(new_account_obj)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Account already exists")

        return {
            "puuid": new_account_obj.puuid,
            "account_name": new_account_obj.account_name,
            "account_tagline": new_account_obj.account_tagline,
            "player_id": player_id,
        }
