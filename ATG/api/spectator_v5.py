from httpx2 import Client, Response
from .utils import RegionLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="spectator_v5_active_games")
def get_active_games(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="spectator_v5_featured_games")
def get_featured_games(client: Client, region: RegionLiteral, **kwargs) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/featured-games",
        params=kwargs,
    )
