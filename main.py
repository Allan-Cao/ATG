import os
import pygsheets
from dotenv import load_dotenv
import cassiopeia as cass
from collections import defaultdict
from cassiopeia import Summoner, Patch, Queue
from SQDBI.match_lib import get_player_stats, region_string, MINIMUM_MATCH_DURATION, upsert_player_match
from SQDBI.utils import update_validator_patches, update_player_accounts

load_dotenv()

RIOT_API = os.environ.get("RIOT_API")
TEAM_SHEET_ID = os.environ.get("TEAM_SHEET_ID")
SHEET_CLIENT_SECRET = os.environ.get("SHEET_CLIENT_SECRET")

cass.set_riot_api_key(RIOT_API)

gc = pygsheets.authorize(service_file=SHEET_CLIENT_SECRET)

TEAM_SHEET_ID = '1UBa-5HjmQxlbivhY-kjq0hqr6rXuuiQV_kG4eJQ0-Ho'

sh = gc.open_by_key(TEAM_SHEET_ID)

DEFAULT_REGION = sh.worksheet('title', 'validators').get_row(2)[4]
PLAYER_ACCOUNTS = update_player_accounts(sh, RIOT_API)

MATCH_WKS = sh.worksheet('title', 'matches')
IMPORTED_MATCH_IDS = MATCH_WKS.get_as_df()[["player", "match"]].groupby('player')['match'].apply(lambda x: set(x.unique())).to_dict()

SEASON_START = Patch.from_str("14.1", region=DEFAULT_REGION).start

# MANUALLY SKIPPING THIS FOR NOW
# update_validator_patches(sh, None, DEFAULT_REGION)

for player in PLAYER_ACCOUNTS.keys():
    upsert_player_match(MATCH_WKS, player, PLAYER_ACCOUNTS[player], IMPORTED_MATCH_IDS, DEFAULT_REGION, SEASON_START)