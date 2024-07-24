from cassiopeia import Patch
from datetime import timedelta
from enum import Enum

DEFAULT_REGION = "NA"
# SEASON_START = Patch.from_str("14.1", region=DEFAULT_REGION).start
SEASON_START = 1704884400  # Season 14 start
MINIMUM_MATCH_DURATION = timedelta(minutes=10)


class Side(Enum):
    blue = 100
    red = 200


class Lane(Enum):
    TOP = "top_lane"
    JNG = "jungle"
    MID = "mid_lane"
    BOT = "bot_lane"
    SUP = "utility"
