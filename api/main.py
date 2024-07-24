import sys

sys.path.append("..")

import os
from dotenv import load_dotenv

load_dotenv("../.shared.env")

from sqlalchemy import select, func, desc, and_, case
from sqlalchemy.exc import IntegrityError
from SQDBI.database import Session
from SQDBI.models import *
from SQDBI.api import get_account_by_riot_id, get_account_by_puuid
from sqlalchemy.orm import Session as _Session
from typing import Annotated, Optional, Union, List
from fastapi import Body, FastAPI, HTTPException, Depends
from pydantic import Field, BaseModel

API_KEY = os.environ.get("RIOT_API")
app = FastAPI()


class NewAccount(BaseModel):
    riot_username: Optional[str] = Field(None, description="Account's riot username")
    riot_tagline: Optional[str] = Field(None, description="Account's riot tagline")
    puuid: Optional[str] = Field(None, description="Account's PUUID")
    region: Optional[str] = Field(None, description="Account's region e.g. NA, EUW")
    player_name: str


class PlayerStatRequest(BaseModel):
    player_name: str
    return_calculated_games: bool = Field(
        False, description="Returns the games used in calculation"
    )
    game_version_major: Optional[int] = Field(None, description="LoL Season")
    game_version_minor: Optional[int] = Field(None, description="Patch number")
    after: Optional[int] = Field(
        None, description="Gets games after-after UNIX timestamp"
    )
    excludes_games: Optional[List[str]] = Field(
        None, description="Game IDs to ignore in the calculation"
    )
    game_type: Optional[str] = Field(None, description="SOLO_QUEUE, SCRIM, ESPORTS")


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/players/available_players")
def get_available_players(db: _Session = Depends(get_db)) -> list:
    statement = select(Player.name)
    rows = db.execute(statement).all()
    if len(rows) == 0:
        return []
    else:
        return [_[0] for _ in rows]


@app.get("/players/get_player_team/{player_name}")
def get_player_team(
    player_name: str, db: _Session = Depends(get_db)
) -> Union[None, str]:
    player = db.scalar(select(Player).where(Player.name == player_name))

    if player is None:
        raise HTTPException(status_code=400, detail="Unknown player_name received")

    statement = (
        select(Team.code)
        .join(PlayerTeamAssociation, Team.id == PlayerTeamAssociation.team_id)
        .join(Player, Player.id == PlayerTeamAssociation.player_id)
        .where(Player.id == player.id)
    )
    return db.scalar(statement)


@app.get("/stats/by_player/")
def get_player_stats_by_name(
    player_request: PlayerStatRequest, db: _Session = Depends(get_db)
) -> dict:
    statement = (
        select(Account.puuid)
        .join(Player, Player.id == Account.player_id)
        .where(Player.name == player_request.player_name)
    )
    player_accounts = db.scalars(statement)
    if player_accounts is None:
        raise HTTPException(status_code=400, detail="Unknown player_name received")

    statement = (
        select(
            Participant.champion_id.label("Champion"),
            func.count(Participant.champion_id).label("Games"),
            func.avg(Participant.kda).label("KDA"),
            func.sum(case((Participant.win == True, 1), else_=0)).label("Wins"),
        )
        .join(Game, Participant.game_id == Game.id)
        .where(Participant.puuid.in_(player_accounts))
        .group_by("Champion")
        .order_by(desc("Games"))
    )
    if (
        player_request.game_version_major is not None
        and player_request.game_version_minor is not None
    ):
        statement = statement.where(
            and_(
                Game.game_version_major == player_request.game_version_major,
                Game.game_version_minor == player_request.game_version_minor,
            )
        )
    if player_request.after is not None:
        statement = statement.where(Game.game_start > player_request.after)
    if player_request.game_type is not None:
        statement = statement.where(Game.game_type == player_request.game_type)
    if player_request.excludes_games is not None:
        statemennt = statement.where(Game.id.not_in(player_request.excludes_games))

    results = db.execute(statement).all()
    return {
        "stats": [
            {
                "Champion": row.Champion,
                "Games": row.Games,
                "KDA": row.KDA,
                "Wins": row.Wins,
            }
            for row in results
        ],
        "games": [],  # TODO
    }


@app.post("/players/new_player/")
def create_new_player(name: Annotated[str, Body()], db: _Session = Depends(get_db)):
    player = db.scalar(select(Player.id).where(Player.name == name))
    if player is not None:
        raise HTTPException(
            status_code=409, detail=f"Player with name {name} already exists."
        )
    p = Player(name=name)
    db.add(p)
    db.commit()


@app.post("/players/new_account/")
def associate_new_account(
    new_account: NewAccount, db: _Session = Depends(get_db)
) -> dict:
    player_id = db.scalar(
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
    db.add(new_account_obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Account already exists")

    return {
        "puuid": new_account_obj.puuid,
        "account_name": new_account_obj.account_name,
        "account_tagline": new_account_obj.account_tagline,
        "player_id": player_id,
    }
