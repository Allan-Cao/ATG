from cassiopeia import Patch
from datetime import timedelta
from enum import Enum

DEFAULT_REGION = "NA"
SEASON_START = Patch.from_str("14.1", region=DEFAULT_REGION).start
MINIMUM_MATCH_DURATION = timedelta(minutes=10)

class Side(Enum):
    blue = 100
    red = 200