import requests as r
from requests import Response
from .utils import headers
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="spectator_v5_active_games")
def get_active_games(puuid: str, region: str, api_key: str, **kwargs) -> Response:
    _headers = {"X-Riot-Token": api_key, **headers}
    response = r.get(
        f"https://{region.lower()}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}",
        headers=_headers,
        params=kwargs,
    )
    return response
