import os
from dotenv import load_dotenv

load_dotenv()

from ATG.database import get_session_factory
from ATG.api import get_challengers, get_masters, get_grandmasters, get_match_history, get_match_by_id
from ATG.utils import SEASON_START
from ATG.models import Game
from ATG.match_lib import upsert_match
from sqlalchemy import select
from tqdm import tqdm

RIOT_API = os.environ["RIOT_API"]
DB_CONNECTION = os.environ["DB_CONNECTION"]

Session = get_session_factory(DB_CONNECTION)

with Session() as session:
    region = "NA1"
    players = get_masters(region, "RANKED_SOLO_5x5", RIOT_API).json()["entries"]

    existing_ids = set(session.scalars(select(Game.id)).all())
    for player in players:
        match_ids = get_match_history(
            player["puuid"],
            region,
            RIOT_API,
            startTime=SEASON_START,
            queue=420,
        )
        new_match_ids = set(match_ids) - existing_ids

        for match_id in tqdm(new_match_ids):
            try:
                game_data = get_match_by_id(match_id, RIOT_API)
                game_data = game_data.json()
                game_info = game_data["info"]
                match_end_time = upsert_match(session, match_id, game_data, game_info)
                existing_ids.add(match_id)
            except Exception as e:
                print(f"Failed to upsert match {match_id}: {str(e)}")
        session.commit()
