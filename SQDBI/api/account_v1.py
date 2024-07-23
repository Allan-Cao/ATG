import requests as r
from .utils import headers
from ratelimit import limits, RateLimitException, sleep_and_retry

MAX_CALLS_PER_MINUTE = 1000
ONE_MINUTE = 60


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get_account_by_riot_id(game_name: str, tag_line: str, api_key: str) -> dict:
    _headers = {"X-Riot-Token": api_key, **headers}
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    response = r.get(
        f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
        headers=_headers,
    )

    response.raise_for_status()

    return response.json()


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get_account_by_puuid(puuid: str, api_key: str) -> dict:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}",
        headers=_headers,
    )

    response.raise_for_status()

    return response.json()
