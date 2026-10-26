from httpx2 import Client, Response
from .utils import RegionLiteral, QueueLiteral, DivisionLiteral, TierLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="league_v4_get_challengers")
def get_challengers(
    client: Client, region: RegionLiteral, queue: QueueLiteral
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_get_grandmasters")
def get_grandmasters(
    client: Client, region: RegionLiteral, queue: QueueLiteral
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_get_masters")
def get_masters(client: Client, region: RegionLiteral, queue: QueueLiteral) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}"
    )


@riot_api_limiter(endpoint_key="league_v4_entries_puuid")
def get_league_entries_by_puuid(
    client: Client, region: RegionLiteral, puuid: str
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    )


@riot_api_limiter(endpoint_key="league_v4_entries_summoner_id")
def get_league_entries_by_summoner_id(
    client: Client, region: RegionLiteral, summoner_id: str
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    )


@riot_api_limiter(endpoint_key="league_v4_all_entries")
def get_all_league_entries(
    client: Client,
    region: RegionLiteral,
    queue: QueueLiteral,
    tier: TierLiteral,
    division: DivisionLiteral,
    page: int = 1,
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}",
        headers={"page": str(page)},
    )


@riot_api_limiter(endpoint_key="league_v4_entries_league_id")
def get_league_entries_by_league_id(
    client: Client, region: RegionLiteral, league_id: str
) -> Response:
    return client.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/leagues/{league_id}"
    )
