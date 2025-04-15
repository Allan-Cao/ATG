import requests as r
from requests import Response
from .utils import headers, QUEUES, REGIONS
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="league_v4_get_challengers")
def get_challengers(region: str, queue: str, api_key: str) -> Response:
    if queue not in QUEUES:
        raise ValueError("Invalid queue received. Expecting " + " ".join(QUEUES))
    if region not in REGIONS:
        raise ValueError("Invalid region received. Expecting " + " ".join(REGIONS))
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queue}",
        headers=_headers,
    )
    return response


@riot_api_limiter(endpoint_key="league_v4_get_grandmasters")
def get_grandmasters(region: str, queue: str, api_key: str) -> Response:
    if queue not in QUEUES:
        raise ValueError("Invalid queue received. Expecting " + " ".join(QUEUES))
    if region not in REGIONS:
        raise ValueError("Invalid region received. Expecting " + " ".join(REGIONS))
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queue}",
        headers=_headers,
    )
    return response


@riot_api_limiter(endpoint_key="league_v4_get_masters")
def get_masters(region: str, queue: str, api_key: str) -> Response:
    if queue not in QUEUES:
        raise ValueError("Invalid queue received. Expecting " + " ".join(QUEUES))
    if region not in REGIONS:
        raise ValueError("Invalid region received. Expecting " + " ".join(REGIONS))
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}",
        headers=_headers,
    )
    return response
