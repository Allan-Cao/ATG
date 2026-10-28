from datetime import datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Literal, get_args
from urllib.parse import quote
from httpx2 import Client

try:
    _VERSION = version("ATG-lib")
except PackageNotFoundError:
    _VERSION = "unknown"

headers = {"User-Agent": f"ATG-lib/{_VERSION}"}

Region = Literal[
    "NA1",
    "BR1",
    "LA1",
    "LA2",
    "KR",
    "JP1",
    "ME1",
    "EUN1",
    "EUW1",
    "TR1",
    "RU",
    "OC1",
    "SG2",
    "TW2",
    "VN2",
]
Queue = Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"]
Tier = Literal["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"]
Division = Literal["I", "II", "III", "IV"]
MatchType = Literal["ranked", "normal", "tourney", "tutorial"]
ChallengeLevel = Literal["MASTER", "GRANDMASTER", "CHALLENGER"]

#: Every platform accepted as ``region``.
REGIONS: tuple[Region, ...] = get_args(Region)
#: Every ranked queue.
QUEUES: tuple[Queue, ...] = get_args(Queue)
#: Every ranked tier served by :func:`ATG.api.get_league_entries`.
TIERS: tuple[Tier, ...] = get_args(Tier)
#: Every division within a tier.
DIVISIONS: tuple[Division, ...] = get_args(Division)

# The AMERICAS routing value serves NA, BR, LAN and LAS. The ASIA routing value serves KR and JP. The EUROPE routing value serves EUNE, EUW, ME1, TR and RU. The SEA routing value serves OCE, SG2, TW2 and VN2.
PLATFORM_ROUTING: dict[Region, str] = {
    "NA1": "americas",
    "BR1": "americas",
    "LA1": "americas",
    "LA2": "americas",
    "KR": "asia",
    "JP1": "asia",
    "ME1": "europe",
    "EUN1": "europe",
    "EUW1": "europe",
    "TR1": "europe",
    "RU": "europe",
    "OC1": "sea",
    "SG2": "sea",
    "TW2": "sea",
    "VN2": "sea",
}

# account-v1 has no SEA route, but any account can be queried from any route, so SEA platforms use the nearest one.
ACCOUNT_ROUTING: dict[str, str] = {
    "americas": "americas",
    "asia": "asia",
    "europe": "europe",
    "sea": "asia",
}


def _validate_region(region: str) -> Region:
    if region.upper() not in REGIONS:
        raise ValueError(f"Unknown region {region}, expected one of {REGIONS}")
    return region.upper()


def platform_url(region: str) -> str:
    """Build the base URL of a platform route, such as ``NA1``.

    :param region: Platform routing value, such as ``"NA1"``. Case-insensitive.
    :type region: str
    :returns: The base URL, without a trailing slash.
    :rtype: str
    :raises ValueError: If ``region`` is not a known platform.
    """
    return f"https://{_validate_region(region).lower()}.api.riotgames.com"


def regional_url(region: str) -> str:
    """Build the base URL of the regional route serving a platform.

    :param region: Platform routing value, such as ``"NA1"``. Case-insensitive.
    :type region: str
    :returns: The base URL, without a trailing slash.
    :rtype: str
    :raises ValueError: If ``region`` is not a known platform.
    """
    return f"https://{PLATFORM_ROUTING[_validate_region(region)]}.api.riotgames.com"


def account_url(region: str) -> str:
    """Build the base URL of the account-v1 route nearest to a platform.

    :param region: Platform routing value, such as ``"NA1"``. Case-insensitive.
    :type region: str
    :returns: The base URL, without a trailing slash.
    :rtype: str
    :raises ValueError: If ``region`` is not a known platform.
    """
    routing = ACCOUNT_ROUTING[PLATFORM_ROUTING[_validate_region(region)]]
    return f"https://{routing}.api.riotgames.com"


def path_segment(value: str) -> str:
    """Percent-encode a value for use as one URL path segment.

    Riot IDs may contain spaces and non-ASCII characters, such as Korean or
    Cyrillic names, which must be encoded exactly once.

    :param value: The raw value.
    :type value: str
    :returns: The encoded value.
    :rtype: str
    """
    return quote(value, safe="")


def epoch_seconds(value: datetime | int | None) -> int | None:
    """Convert a time to epoch seconds, as Riot expects in query parameters.

    :param value: A datetime, epoch seconds, or ``None``.
    :type value: datetime.datetime | int | None
    :returns: Epoch seconds, or ``None`` if ``value`` is ``None``.
    :rtype: int | None
    """
    if isinstance(value, datetime):
        return int(value.timestamp())
    return value


def parse_match_id(match_id: str) -> tuple[str, str]:
    """Split a match ID into its region and game ID halves.

    :param match_id: Match ID of the form ``"<REGION>_<GAME ID>"``, such as
        ``"NA1_4567890123"``.
    :type match_id: str
    :returns: The region and the game ID.
    :rtype: tuple[str, str]
    :raises ValueError: If ``match_id`` is not two underscore-separated parts,
        or the region is not a known platform routing value.
    """
    split = match_id.split("_")
    if len(split) != 2:
        raise ValueError(f"Unable to parse {match_id}")
    if split[0] not in REGIONS:
        raise ValueError(f"Unknown region {split[0]} received")
    return split[0], split[1]


def riot_client(api_key: str, **kwargs) -> Client:
    """Build a client carrying the Riot API key.

    :param api_key: Riot API key, sent as the ``X-Riot-Token`` header.
    :type api_key: str
    :param kwargs: Additional keyword arguments passed to :class:`httpx2.Client`.
    :returns: A client preconfigured with the API key and default headers.
    :rtype: httpx2.Client
    """
    return Client(headers={"X-Riot-Token": api_key, **headers}, **kwargs)
