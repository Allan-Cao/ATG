from httpx2 import Client, Response
from .utils import RegionLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="summoner_v4_by_account_id")
def get_summoner_by_account_id(
    client: Client, account_id: str, region: RegionLiteral, **kwargs
) -> Response:
    """Get a summoner by encrypted account ID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param account_id: The account's encrypted account ID.
    :type account_id: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters.
    :returns: The raw summoner-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="summoner_v4_by_puuid")
def get_summoner_by_puuid(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> Response:
    """Get a summoner by PUUID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters.
    :returns: The raw summoner-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="summoner_v4_by_summoner_id")
def get_summoner_by_summoner_id(
    client: Client, summoner_id: str, region: RegionLiteral, **kwargs
) -> Response:
    """Get a summoner by encrypted summoner ID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param summoner_id: The account's encrypted summoner ID.
    :type summoner_id: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters.
    :returns: The raw summoner-v4 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}",
        params=kwargs,
    )
