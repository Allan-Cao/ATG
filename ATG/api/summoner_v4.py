import requests as r
from requests import Response
from .utils import headers
from ratelimit import limits
from backoff import on_predicate, runtime

MAX_CALLS_PER_MINUTE = 1600
MINUTE = 60


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_MINUTE, period=MINUTE)
def get_summoner_by_account(account_id: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}",
        headers=_headers,
        params=kwargs,
    )
    return response

@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_MINUTE, period=MINUTE)
def get_summoner_by_puuid(puuid: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}",
        headers=_headers,
        params=kwargs,
    )
    return response

@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_MINUTE, period=MINUTE)
def get_summoner_by_summoner_id(summoner_id: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}",
        headers=_headers,
        params=kwargs,
    )
    return response
