import requests as r
from requests import Response
from .utils import headers, platform_routing, parse_match_id
import backoff
import time

# @on_predicate(
#     runtime,
#     predicate=lambda r: r.status_code == 429,
#     value=lambda r: int(r.headers.get("Retry-After")),
#     jitter=None,
# )
@backoff.on_predicate(backoff.expo, predicate=lambda r: r.status_code == 429, max_tries=8)
def get_match_by_id(match_id: str, api_key: str, timeline: bool = False) -> Response:
    time.sleep(200/120)
    region, match = parse_match_id(match_id)
    is_timeline = "/timeline" if timeline else ""
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{platform_routing[region]}.api.riotgames.com/lol/match/v5/matches/{match_id}{is_timeline}",
        headers=_headers,
    )
    return response


# @on_predicate(
#     runtime,
#     predicate=lambda r: r.status_code == 429,
#     value=lambda r: int(r.headers.get("Retry-After")),
#     jitter=None,
# )
@backoff.on_predicate(backoff.expo, predicate=lambda r: r.status_code == 429, max_tries=8)
def get_available_matches(puuid: str, region: str, api_key: str, **kwargs) -> Response:
    time.sleep(200/120)
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{platform_routing[region]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
        headers=_headers,
        params=kwargs,
    )
    return response


def get_match_history(puuid: str, region: str, api_key: str, **kwargs) -> list[str]:
    start = 0
    count = 100
    match_history = []
    while True:
        match_list = get_available_matches(
            puuid=puuid,
            region=region,
            api_key=api_key,
            start=start,
            count=count,
            **kwargs,
        )
        if match_list:
            try:
                match_list.raise_for_status()
                match_list = match_list.json()
                if len(match_list) == 0:
                    break
                match_history.extend(match_list)
                start += count
            except:
                # If an error occurs, we will fail.
                print(f"{match_list.status_code} - Failed to retrieve match history")
                return match_history
    return match_history
