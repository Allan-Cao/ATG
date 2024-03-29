import requests as r
from .utils import headers, routing
from ratelimit import limits, RateLimitException, sleep_and_retry

MAX_CALLS_PER_TEN_SECONDS = 2000
TEN_SECONDS = 10


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_TEN_SECONDS, period=TEN_SECONDS)
def get_match_by_id(match_id: str, region: str, api_key: str) -> dict:
    if region not in routing.keys():
        raise ValueError(
            "Invalid region. Expecting NA/EUW/EUNE/KR/BR/LAN/LAS/TR/RU/OCE/JP/SEA"
        )
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    response = r.get(
        f"https://{routing[region]}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_TEN_SECONDS, period=TEN_SECONDS)
def get_available_matches(puuid: str, region: str, api_key: str, **kwargs) -> list:
    response = r.get(
        f"https://{routing[region]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={api_key}",
        headers=headers,
        params=kwargs,
    )

    response.raise_for_status()

    return response.json()
