from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="champion-mastery-v4.getAllChampionMasteriesByPUUID")
def get_champion_masteries_by_puuid(
    client: Client, puuid: str, *, region: Region
) -> Response:
    """Get every champion mastery for a PUUID, highest champion points first.

    Riot endpoint: ``champion-mastery-v4`` ``GET /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw champion-mastery-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    )


@riot_api_limiter(endpoint_key="champion-mastery-v4.getChampionMasteryByPUUID")
def get_champion_mastery_by_puuid(
    client: Client, puuid: str, champion_id: int, *, region: Region
) -> Response:
    """Get a PUUID's mastery of one champion.

    Riot endpoint: ``champion-mastery-v4`` ``GET /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/by-champion/{championId}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param champion_id: The champion's numeric ID, such as ``266`` for Aatrox.
    :type champion_id: int
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw champion-mastery-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/by-champion/{champion_id}"
    )


@riot_api_limiter(endpoint_key="champion-mastery-v4.getTopChampionMasteriesByPUUID")
def get_top_champion_masteries_by_puuid(
    client: Client, puuid: str, *, region: Region, count: int = 3
) -> Response:
    """Get a PUUID's highest champion masteries.

    Riot endpoint: ``champion-mastery-v4`` ``GET /lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param count: Number of masteries to return, defaults to ``3``.
    :type count: int
    :returns: The raw champion-mastery-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top",
        params={"count": count},
    )


@riot_api_limiter(endpoint_key="champion-mastery-v4.getChampionMasteryScoreByPUUID")
def get_mastery_score_by_puuid(
    client: Client, puuid: str, *, region: Region
) -> Response:
    """Get a PUUID's total mastery score, the sum of its champion mastery levels.

    Riot endpoint: ``champion-mastery-v4`` ``GET /lol/champion-mastery/v4/scores/by-puuid/{encryptedPUUID}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw champion-mastery-v4 response, whose body is an integer.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/champion-mastery/v4/scores/by-puuid/{puuid}"
    )
