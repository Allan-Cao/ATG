import httpx2
from httpx2 import Response


def get_ddragon_versions() -> Response:
    """Get the list of Data Dragon versions, newest first.

    This endpoint is not part of the Riot API and needs no API key, so it is
    called without a client and is not rate limited.

    :returns: The raw response from Data Dragon.
    :rtype: httpx2.Response
    """
    return httpx2.get("https://ddragon.leagueoflegends.com/api/versions.json")
