from httpx2 import Client, Response
from .utils import RegionLiteral, QueueLiteral, DivisionLiteral, TierLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="league_v4_get_challengers")
def get_challengers(
    client: Client, region: RegionLiteral, queue: QueueLiteral
) -> Response:
    """Get the challenger league for a queue.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, such as ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_get_grandmasters")
def get_grandmasters(
    client: Client, region: RegionLiteral, queue: QueueLiteral
) -> Response:
    """Get the grandmaster league for a queue.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, such as ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_get_masters")
def get_masters(client: Client, region: RegionLiteral, queue: QueueLiteral) -> Response:
    """Get the master league for a queue.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, such as ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_entries_puuid")
def get_league_entries_by_puuid(
    client: Client, region: RegionLiteral, puuid: str
) -> Response:
    """Get every ranked entry for a PUUID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param puuid: The account's PUUID.
    :type puuid: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    )


@riot_api_limiter(endpoint_key="league_v4_entries_summoner_id")
def get_league_entries_by_summoner_id(
    client: Client, region: RegionLiteral, summoner_id: str
) -> Response:
    """Get every ranked entry for an encrypted summoner ID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param summoner_id: The account's encrypted summoner ID.
    :type summoner_id: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    )


@riot_api_limiter(endpoint_key="league_v4_all_entries")
def get_all_league_entries(
    client: Client,
    region: RegionLiteral,
    queue: QueueLiteral,
    tier: TierLiteral,
    division: DivisionLiteral,
    page: int = 1,
) -> Response:
    """Get a page of ranked entries for a queue, tier and division.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, such as ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :param tier: Ranked tier from ``"DIAMOND"`` down to ``"IRON"``. Master and
        above are served by :func:`get_masters`, :func:`get_grandmasters` and
        :func:`get_challengers` instead.
    :type tier: str
    :param division: Division within the tier, from ``"I"`` to ``"IV"``.
    :type division: str
    :param page: Page of results to request, defaults to ``1``. Sent as the
        ``page`` header rather than a query parameter.
    :type page: int
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}",
        headers={"page": str(page)},
    )


@riot_api_limiter(endpoint_key="league_v4_entries_league_id")
def get_league_entries_by_league_id(
    client: Client, region: RegionLiteral, league_id: str
) -> Response:
    """Get a league and all of its entries by league ID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param league_id: The league's UUID.
    :type league_id: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/leagues/{league_id}"
    )
