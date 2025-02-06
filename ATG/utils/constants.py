from datetime import timedelta
from enum import Enum

DEFAULT_REGION = "NA"
SEASON_START = 1736420400  # Season 15. Season 14 was 1704884400
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


class TeamPosition(Enum):
    AFK = None
    BOTTOM = "BOT"
    JUNGLE = "JNG"
    MIDDLE = "MID"
    TOP = "TOP"
    UTILITY = "SUP"
