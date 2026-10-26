from httpx2 import Client, Response
from .utils import RoutingLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="account_v1_by_riot_id")
def get_account_by_riot_id(
    client: Client, game_name: str, tag_line: str, routing: RoutingLiteral = "americas"
) -> Response:
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    return client.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )


@riot_api_limiter(endpoint_key="account_v1_by_puuid")
def get_account_by_puuid(
    client: Client, puuid: str, routing: RoutingLiteral = "americas"
) -> Response:
    return client.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    )
