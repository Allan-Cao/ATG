from httpx2 import Client, Response
from .utils import Region, account_url, path_segment
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="account-v1.getByRiotId")
def get_account_by_riot_id(
    client: Client, game_name: str, tag_line: str, *, region: Region = "NA1"
) -> Response:
    """Get an account by its Riot ID.

    Riot endpoint: ``account-v1`` ``GET /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param game_name: The name half of the Riot ID. Spaces and non-ASCII
        characters are encoded for you.
    :type game_name: str
    :param tag_line: The tagline half of the Riot ID, without the ``#``.
    :type tag_line: str
    :param region: Platform routing value, such as ``"NA1"``, defaults to
        ``"NA1"``. Any account can be queried from any account route, so this
        only picks the nearest one.
    :type region: str
    :returns: The raw account-v1 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"{account_url(region)}/riot/account/v1/accounts/by-riot-id/{path_segment(game_name)}/{path_segment(tag_line)}"
    )


@riot_api_limiter(endpoint_key="account-v1.getByPuuid")
def get_account_by_puuid(
    client: Client, puuid: str, *, region: Region = "NA1"
) -> Response:
    """Get an account by its PUUID.

    Riot endpoint: ``account-v1`` ``GET /riot/account/v1/accounts/by-puuid/{puuid}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``, defaults to
        ``"NA1"``. Any account can be queried from any account route, so this
        only picks the nearest one.
    :type region: str
    :returns: The raw account-v1 response.
    :rtype: httpx2.Response
    """
    return client.get(
        f"{account_url(region)}/riot/account/v1/accounts/by-puuid/{puuid}"
    )


@riot_api_limiter(endpoint_key="account-v1.getActiveRegion")
def get_region_by_puuid(
    client: Client, puuid: str, *, region: Region = "NA1"
) -> Response:
    """Get the League of Legends platform an account is active on.

    Riot endpoint: ``account-v1`` ``GET /riot/account/v1/region/by-game/lol/by-puuid/{puuid}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``, defaults to
        ``"NA1"``. Any account can be queried from any account route, so this
        only picks the nearest one.
    :type region: str
    :returns: The raw account-v1 response, whose ``region`` field is the
        lowercase platform, such as ``"na1"``.
    :rtype: httpx2.Response
    """
    return client.get(
        f"{account_url(region)}/riot/account/v1/region/by-game/lol/by-puuid/{puuid}"
    )
