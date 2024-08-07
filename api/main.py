import sys

sys.path.append("..")

import os
from dotenv import load_dotenv

load_dotenv("../.shared.env")

import requests
from sqlalchemy import Integer, select, func, desc, and_, case
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
    account_name: Optional[str] = Field(None, description="Account's riot username")
    account_tagline: Optional[str] = Field(None, description="Account's riot tagline")
    puuid: Optional[str] = Field(None, description="Account's PUUID")
    region: Optional[str] = Field(None, description="Account's region e.g. NA, EUW")
    player_name: str


class PlayerStatRequest(BaseModel):
    player_name: str
    return_calculated_games: bool = Field(
        False, description="Returns the games used in calculation"
    )
    patch: Optional[str] = Field(None, description="LoL Patch")
    before: Optional[int] = Field(
        None, description="Gets games before-before UNIX timestamp"
    )
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
def get_available_players(db: _Session = Depends(get_db)) -> List[str]:
    return list(db.scalars(select(Player.name)))


@app.get("/players/get_player_accounts/{player_name}")
def get_player_accounts(
    player_name: str, db: _Session = Depends(get_db)
) -> List[Union[None, str]]:
    accounts = db.execute(
        select(Account.account_name, Account.account_tagline)
        .join(Player, Player.id == Account.player_id)
        .where(and_(Player.name == player_name), Account.region != "TOURNAMENT")
    )
    return [_.account_name + "#" + _.account_tagline for _ in accounts]


@app.get("/players/available_puuids")
def get_available_puuids(db: _Session = Depends(get_db)) -> List[str]:
    return list(db.scalars(select(Account.puuid)))


@app.get("/players/get_player_team/{player_name}")
def get_player_team(
    player_name: str, db: _Session = Depends(get_db)
) -> Union[None, str]:
    player = db.scalar(select(Player).where(Player.name == player_name))

    if player is None:
        raise HTTPException(status_code=400, detail="Unknown player_name received")

    statement = (
        select(Team.team_code)
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
            Participant.champion_id.label("champion"),
            func.count(Participant.champion_id).label("games"),
            func.avg(Participant.kda).label("kda"),
            func.sum(Participant.win.cast(Integer)).label("wins"),
        )
        .join(Game, Participant.game_id == Game.id)
        .where(Participant.puuid.in_(player_accounts))
        .group_by("champion")
        .order_by(desc("games"))
    )
    statement = statement.where(Game.patch == player_request.patch)
    if player_request.after is not None:
        statement = statement.where(Game.game_start > player_request.after)
    if player_request.before is not None:
        statement = statement.where(Game.game_start < player_request.before)
    if player_request.game_type is not None:
        statement = statement.where(Game.game_type == player_request.game_type)

    results = db.execute(statement).all()
    return {
        "stats": [
            {
                "champion": row.champion,
                "games": row.games,
                "kda": row.kda,
                "wins": row.wins,
            }
            for row in results
        ],
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
    if new_account.region != "TOURNAMENT":
        # We can't process this if don't receive a puuid and either name/tagline is not received
        if new_account.puuid is None and (
            new_account.account_name is None or new_account.account_tagline is None
        ):
            raise HTTPException(
                status_code=400,
                detail="Expecting PUUID and/or Account/Tagline pair. Not enough values were received.",
            )
        try:
            if new_account.puuid is not None:
                account_details = get_account_by_puuid(new_account.puuid, API_KEY)
            else:
                account_details = get_account_by_riot_id(
                    new_account.account_name, new_account.account_tagline, API_KEY
                )
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
        new_account_obj = Account(
            puuid=account_details.get("puuid"),
            account_name=account_details.get("gameName"),
            account_tagline=account_details.get("tagLine"),
            region=new_account.region,
            player_id=player_id,
        )
    else:
        if new_account.puuid is None:
            raise HTTPException(
                status_code=400, detail="PUUIDs are required for TR accounts"
            )
        new_account_obj = Account(
            puuid=new_account.puuid,
            account_name=new_account.account_name,
            account_tagline=new_account.account_tagline,
            region=new_account.region,
            player_id=player_id,
        )
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
