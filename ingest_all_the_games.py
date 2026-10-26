import sys
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from ATG.database import get_session_factory
from ATG.api import (
    riot_client,
    get_challengers,
    get_masters,
    get_grandmasters,
    get_match_history,
    get_match_by_id,
)
from ATG.utils import SEASON_START
from ATG.models import Game
from ATG.match_lib import process_match
from sqlalchemy import select
from tqdm import tqdm

RIOT_API = os.environ["RIOT_API"]
DB_CONNECTION = os.environ["DB_CONNECTION"]

Session = get_session_factory(DB_CONNECTION)

with riot_client(RIOT_API) as client, Session() as session:
    region = sys.argv[1]
    players = []
    players.extend(get_challengers(client, region, "RANKED_SOLO_5x5").json()["entries"])
    players.extend(
        get_grandmasters(client, region, "RANKED_SOLO_5x5").json()["entries"]
    )
    players.extend(get_masters(client, region, "RANKED_SOLO_5x5").json()["entries"])

    import random

    random.shuffle(players)

    existing_ids = set(session.scalars(select(Game.id)).all())
    for player in players:
        match_ids = get_match_history(
            client,
            player["puuid"],
            region,
            startTime=1745888400,
            queue=420,
        )
        new_match_ids = set(match_ids) - existing_ids

        for match_id in tqdm(new_match_ids):
            try:
                game_data = get_match_by_id(client, match_id)
                game_data = game_data.json()["info"]
                process_match(session, match_id, game_data)
                existing_ids.add(match_id)
            except Exception as e:
                print(f"Failed to upsert match {match_id}: {str(e)}")
        session.commit()
