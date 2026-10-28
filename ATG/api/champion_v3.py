from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="champion-v3.getChampionInfo")
def get_free_champion_rotation(client: Client, *, region: Region) -> Response:
    """Get the current free-to-play champion rotation.

    Riot endpoint: ``champion-v3`` ``GET /lol/platform/v3/champion-rotations``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw champion-v3 response, including the separate rotation
        for new players.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/platform/v3/champion-rotations")
