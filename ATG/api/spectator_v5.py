from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="spectator-v5.getCurrentGameInfoByPuuid")
def get_active_game_by_puuid(client: Client, puuid: str, *, region: Region) -> Response:
    """Get the game a PUUID is currently in.

    Riot endpoint: ``spectator-v5`` ``GET /lol/spectator/v5/active-games/by-summoner/{encryptedPUUID}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw spectator-v5 response. The endpoint answers ``404`` when
        the account is not in a game.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/spectator/v5/active-games/by-summoner/{puuid}"
    )
