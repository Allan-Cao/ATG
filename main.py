import os
from dotenv import dotenv_values

# Load environment variables
config = {
    **dotenv_values(".shared.env"),
    **os.environ,
}

config.update(dotenv_values(".admin.env"))

os.environ.update(config)

import cassiopeia as cass
from cassiopeia import Patch
from ATG.match_lib import upsert_match_history, update_player_accounts
from ATG.database import get_session_factory
from ATG.models import Player, Game


RIOT_API = os.environ.get("RIOT_API")
DB_CONNECTION = os.environ.get("DB_CONNECTION")

if RIOT_API is None:
    print("Riot API is not set.")
    exit()
if DB_CONNECTION is None:
    print("Database connection is not set.")
    exit()

cass.set_riot_api_key(RIOT_API)
Session = get_session_factory(DB_CONNECTION)

with Session() as session:
    update_player_accounts(session, RIOT_API)
    PLAYERS = session.query(Player).all()
    for player in PLAYERS:
        existing_ids = set(id for (id,) in session.query(Game.id).all())
        upsert_match_history(session, existing_ids, player, RIOT_API)
