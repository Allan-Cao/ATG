import httpx2
from httpx2 import Response


def get_ddragon_versions() -> Response:
    return httpx2.get("https://ddragon.leagueoflegends.com/api/versions.json")
