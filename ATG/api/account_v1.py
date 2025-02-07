import requests as r
from requests import Response
from .utils import headers
from ratelimit import limits
from backoff import on_predicate, runtime

MAX_CALLS_PER_MINUTE = 1000
ONE_MINUTE = 60


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get_account_by_riot_id(
    game_name: str, tag_line: str, api_key: str, routing: str = "americas"
) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    response = r.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
        headers=_headers,
    )
    return response


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get_account_by_puuid(
    puuid: str, api_key: str, routing: str = "americas"
) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
        headers=_headers,
    )
    return response
