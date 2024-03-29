import os
from dotenv import load_dotenv
import cassiopeia as cass
from cassiopeia import Patch
from SQDBI.match_lib.ingest_match import upsert_match_history
from SQDBI.database import get_db
from SQDBI.models import Player

load_dotenv()

RIOT_API = os.environ.get("RIOT_API")
cass.set_riot_api_key(RIOT_API)

db = next(get_db())
PLAYERS = db.query(Player).all()

# For now, we do insertion synchronously
for player in PLAYERS:
    upsert_match_history(player, RIOT_API)