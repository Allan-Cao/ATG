from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="lol-status-v4.getPlatformData")
def get_server_status(client: Client, *, region: Region) -> Response:
    """Get the current maintenances and incidents for a platform.

    Riot endpoint: ``lol-status-v4`` ``GET /lol/status/v4/platform-data``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-status-v4 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/status/v4/platform-data")
