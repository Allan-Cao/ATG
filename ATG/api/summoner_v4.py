from httpx2 import Client, Response
from .utils import RegionLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="summoner_v4_by_account_id")
def get_summoner_by_account_id(
    client: Client, account_id: str, region: RegionLiteral, **kwargs
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="summoner_v4_by_puuid")
def get_summoner_by_puuid(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}",
        params=kwargs,
    )


@riot_api_limiter(endpoint_key="summoner_v4_by_summoner_id")
def get_summoner_by_summoner_id(
    client: Client, summoner_id: str, region: RegionLiteral, **kwargs
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}",
        params=kwargs,
    )
