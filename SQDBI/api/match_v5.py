import requests as r
from requests import Response
from .utils import headers, routing
from ratelimit import limits, RateLimitException
from backoff import on_predicate, runtime
from typing import List

MAX_CALLS_PER_TEN_SECONDS = 2000
TEN_SECONDS = 10


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_TEN_SECONDS, period=TEN_SECONDS)
def get_match_by_id(
    match_id: str, region: str, api_key: str, timeline: bool = False
) -> Response:
    if region not in routing.keys():
        raise ValueError(
            "Invalid region. Expecting NA/EUW/EUNE/KR/BR/LAN/LAS/TR/RU/OCE/JP/SEA"
        )
    is_timeline = "/timeline" if timeline else ""
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{routing[region]}.api.riotgames.com/lol/match/v5/matches/{match_id}{is_timeline}",
        headers=_headers,
    )
    # response.raise_for_status()
    return response


@on_predicate(
    runtime,
    predicate=lambda r: r.status_code == 429,
    value=lambda r: int(r.headers.get("Retry-After")),
    jitter=None,
)
@limits(calls=MAX_CALLS_PER_TEN_SECONDS, period=TEN_SECONDS)
def get_available_matches(puuid: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{routing[region]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
        headers=_headers,
        params=kwargs,
    )
    # response.raise_for_status()
    return response


def get_match_history(puuid: str, region: str, api_key: str, **kwargs) -> List[str]:
    start = 0
    count = 100
    matches = []
    while True:
        match_list = get_available_matches(
            puuid=puuid,
            region=region,
            api_key=api_key,
            start=start,
            count=count,
            **kwargs,
        ).json()
        if len(match_list) == 0:
            break
        matches.extend(match_list)
        start += count

    return matches
