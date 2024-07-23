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
from SQDBI.match_lib import upsert_match_history
from SQDBI.database import Session
from SQDBI.models import Player


RIOT_API = os.environ.get("RIOT_API")

if RIOT_API is None:
    print("Riot API is not set.")
    exit()
cass.set_riot_api_key(RIOT_API)

with Session() as session:
    PLAYERS = session.query(Player).all()
    # For now, we do insertion synchronously
    for player in PLAYERS:
        upsert_match_history(session, player, RIOT_API)
