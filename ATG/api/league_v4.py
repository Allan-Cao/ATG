from httpx2 import Client, Response
from .utils import Region, Queue, Tier, Division, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="league-v4.getChallengerLeague")
def get_challengers(
    client: Client, *, region: Region, queue: Queue = "RANKED_SOLO_5x5"
) -> Response:
    """Get the challenger league for a queue.

    Riot endpoint: ``league-v4`` ``GET /lol/league/v4/challengerleagues/by-queue/{queue}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, defaults to ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/league/v4/challengerleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league-v4.getGrandmasterLeague")
def get_grandmasters(
    client: Client, *, region: Region, queue: Queue = "RANKED_SOLO_5x5"
) -> Response:
    """Get the grandmaster league for a queue.

    Riot endpoint: ``league-v4`` ``GET /lol/league/v4/grandmasterleagues/by-queue/{queue}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, defaults to ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/league/v4/grandmasterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league-v4.getMasterLeague")
def get_masters(
    client: Client, *, region: Region, queue: Queue = "RANKED_SOLO_5x5"
) -> Response:
    """Get the master league for a queue.

    Riot endpoint: ``league-v4`` ``GET /lol/league/v4/masterleagues/by-queue/{queue}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, defaults to ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/league/v4/masterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league-v4.getLeagueEntriesByPUUID")
def get_league_entries_by_puuid(
    client: Client, puuid: str, *, region: Region
) -> Response:
    """Get every ranked entry for a PUUID.

    Riot endpoint: ``league-v4`` ``GET /lol/league/v4/entries/by-puuid/{encryptedPUUID}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/league/v4/entries/by-puuid/{puuid}")


@riot_api_limiter(endpoint_key="league-v4.getLeagueEntries")
def get_league_entries(
    client: Client,
    tier: Tier,
    division: Division,
    *,
    region: Region,
    queue: Queue = "RANKED_SOLO_5x5",
    page: int = 1,
) -> Response:
    """Get one page of ranked entries for a tier and division.

    Riot endpoint: ``league-v4`` ``GET /lol/league/v4/entries/{queue}/{tier}/{division}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param tier: Ranked tier from ``"DIAMOND"`` down to ``"IRON"``. Master and
        above are served by :func:`get_masters`, :func:`get_grandmasters` and
        :func:`get_challengers` instead.
    :type tier: str
    :param division: Division within the tier, from ``"I"`` to ``"IV"``.
    :type division: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Ranked queue, defaults to ``"RANKED_SOLO_5x5"``.
    :type queue: str
    :param page: Page of results to request, starting at ``1``. An empty page
        means there are no more entries.
    :type page: int
    :returns: The raw league-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/league/v4/entries/{queue}/{tier}/{division}",
        params={"page": page},
    )
