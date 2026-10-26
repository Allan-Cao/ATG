from httpx2 import Client, Response
from .utils import RegionLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="spectator_v5_active_games")
def get_active_games(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> Response:
    """Get the game a PUUID is currently in.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters.
    :returns: The raw spectator-v5 response. The endpoint answers ``404`` when
        the account is not in a game.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="spectator_v5_featured_games")
def get_featured_games(client: Client, region: RegionLiteral, **kwargs) -> Response:
    """Get the list of featured games for a region.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters.
    :returns: The raw spectator-v5 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/featured-games",
        params=kwargs,
    )
