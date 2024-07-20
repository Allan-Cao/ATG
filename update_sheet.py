import os
from dotenv import dotenv_values
from cassiopeia import Patch
from SQDBI.database import Session

# Load environment variables
config = {
    **dotenv_values(".sheet.env"),
    **os.environ,
}

# config.update(dotenv_values(".env.admin"))

os.environ.update(config)

import gspread
gc = gspread.service_account(filename=os.environ.get("SHEET_CLIENT_SECRET"))
sh = gc.open_by_key(os.environ.get("TEAM_SHEET_ID"))

DEFAULT_REGION = sh.worksheet('title', 'validators').get_row(2)[4]
# PLAYER_ACCOUNTS = update_player_accounts(sh, RIOT_API)

MATCH_WKS = sh.worksheet('title', 'matches')
IMPORTED_MATCH_IDS = MATCH_WKS.get_as_df()[["player", "match"]].groupby('player')['match'].apply(lambda x: set(x.unique())).to_dict()

SEASON_START = Patch.from_str("14.1", region=DEFAULT_REGION).start

# Update latest 3 patches
latest_patch = Patch.latest(DEFAULT_REGION)
patch = [f"{latest_patch.major}.{int(latest_patch.minor) - i}" for i in range(3)]
sh.worksheet('title', 'validators').update_values('C2', list(map(list, zip(patch))))

# We now need to retrieve the matches that haven't been updated in the google sheet (we can assume that our database is always updated)

from SQDBI.models import Participant

with Session() as session:
    print(session.query(Participant.player.name, Participant.game.game_version_major_minor).limit(10))