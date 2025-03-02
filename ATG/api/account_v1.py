import requests as r
from requests import Response
from .utils import headers
import backoff
import time

# @backoff.on_predicate(
#     backoff.runtime,
#     predicate=lambda r: r.status_code == 429,
#     value=lambda r: int(r.headers.get("Retry-After")),
#     jitter=None,
# )
@backoff.on_predicate(backoff.expo, predicate=lambda r: r.status_code == 429, max_tries=8)
def get_account_by_riot_id(
    game_name: str, tag_line: str, api_key: str, routing: str = "americas"
) -> Response:
    time.sleep(200/120)
    _headers = {"X-Riot-Token": api_key, **headers}
    # There are three routing values for account-v1; americas, asia, and europe. You can query for any account in any region. We recommend using the nearest cluster.
    response = r.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
        headers=_headers,
    )
    return response


# @backoff.on_predicate(
#     backoff.runtime,
#     predicate=lambda r: r.status_code == 429,
#     value=lambda r: int(r.headers.get("Retry-After")),
#     jitter=None,
# )
@backoff.on_predicate(backoff.expo, predicate=lambda r: r.status_code == 429, max_tries=8)
def get_account_by_puuid(
    puuid: str, api_key: str, routing: str = "americas"
) -> Response:
    time.sleep(200/120)
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
        headers=_headers,
    )
    return response
