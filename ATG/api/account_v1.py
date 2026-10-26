from httpx2 import Client, Response
from .utils import RoutingLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="account_v1_by_riot_id")
def get_account_by_riot_id(
    client: Client, game_name: str, tag_line: str, routing: RoutingLiteral = "americas"
) -> Response:
    """Get an account by its Riot ID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param game_name: The name half of the Riot ID.
    :type game_name: str
    :param tag_line: The tagline half of the Riot ID, without the ``#``.
    :type tag_line: str
    :param routing: Regional routing value, defaults to ``"americas"``. Any
        account can be queried from any of the three account-v1 routes, so
        the nearest cluster is the best choice.
    :type routing: str
    :returns: The raw account-v1 response.
    :rtype: httpx2.Response
    """
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    return client.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )


@riot_api_limiter(endpoint_key="account_v1_by_puuid")
def get_account_by_puuid(
    client: Client, puuid: str, routing: RoutingLiteral = "americas"
) -> Response:
    """Get an account by its PUUID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param routing: Regional routing value, defaults to ``"americas"``.
    :type routing: str
    :returns: The raw account-v1 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    )
