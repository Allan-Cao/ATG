import requests as r
from requests import Response
from .utils import headers
from ratelimit import limits
from backoff import on_predicate, runtime

MAX_CALLS_PER_TEN_SECONDS = 2000
TEN_SECONDS = 10


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_TEN_SECONDS, period=TEN_SECONDS)
def get_active_games(puuid: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}",
        headers=_headers,
        params=kwargs,
    )
    return response
