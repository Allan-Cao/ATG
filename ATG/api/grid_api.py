import requests as r
from requests import Response

def get_grid_riot_summary(series_id: str, game_number: int, GRID_API_KEY: str) -> Response:
    headers = {"x-api-key": GRID_API_KEY}
    headers.update({"Accept": "application/json"})
    return r.get(
        f"https://api.grid.gg/file-download/end-state/riot/series/{series_id}/games/{game_number}/summary",
        headers=headers,
    )
