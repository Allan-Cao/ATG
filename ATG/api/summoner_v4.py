from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="summoner-v4.getByPUUID")
def get_summoner_by_puuid(client: Client, puuid: str, *, region: Region) -> Response:
    """Get a summoner by PUUID.

    Riot endpoint: ``summoner-v4`` ``GET /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw summoner-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    )
