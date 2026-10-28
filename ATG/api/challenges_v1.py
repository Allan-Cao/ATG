from httpx2 import Client, Response
from .utils import ChallengeLevel, Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="lol-challenges-v1.getAllChallengeConfigs")
def get_challenge_configs(client: Client, *, region: Region) -> Response:
    """Get the configuration of every challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/challenges/config``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-challenges-v1 response, including every translation
        of each challenge's name and description.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/challenges/v1/challenges/config")


@riot_api_limiter(endpoint_key="lol-challenges-v1.getChallengeConfigs")
def get_challenge_config_by_id(
    client: Client, challenge_id: int, *, region: Region
) -> Response:
    """Get the configuration of one challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/challenges/{challengeId}/config``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param challenge_id: The challenge's ID.
    :type challenge_id: int
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-challenges-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/challenges/v1/challenges/{challenge_id}/config"
    )


@riot_api_limiter(endpoint_key="lol-challenges-v1.getAllChallengePercentiles")
def get_challenge_percentiles(client: Client, *, region: Region) -> Response:
    """Get the share of players who reached each level of every challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/challenges/percentiles``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-challenges-v1 response, keyed by challenge ID, then
        level.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/challenges/v1/challenges/percentiles"
    )


@riot_api_limiter(endpoint_key="lol-challenges-v1.getChallengePercentiles")
def get_challenge_percentiles_by_id(
    client: Client, challenge_id: int, *, region: Region
) -> Response:
    """Get the share of players who reached each level of one challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/challenges/{challengeId}/percentiles``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param challenge_id: The challenge's ID.
    :type challenge_id: int
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-challenges-v1 response, keyed by level.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/challenges/v1/challenges/{challenge_id}/percentiles"
    )


@riot_api_limiter(endpoint_key="lol-challenges-v1.getChallengeLeaderboards")
def get_challenge_leaderboard(
    client: Client,
    challenge_id: int,
    level: ChallengeLevel,
    *,
    region: Region,
    limit: int | None = None,
) -> Response:
    """Get the top players of one level of a challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/challenges/{challengeId}/leaderboards/by-level/{level}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param challenge_id: The challenge's ID.
    :type challenge_id: int
    :param level: ``"MASTER"``, ``"GRANDMASTER"`` or ``"CHALLENGER"``.
    :type level: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param limit: Maximum number of players to return, defaults to Riot's
        limit.
    :type limit: int | None
    :returns: The raw lol-challenges-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/challenges/v1/challenges/{challenge_id}/leaderboards/by-level/{level}",
        params={} if limit is None else {"limit": limit},
    )


@riot_api_limiter(endpoint_key="lol-challenges-v1.getPlayerData")
def get_challenges_by_puuid(client: Client, puuid: str, *, region: Region) -> Response:
    """Get a PUUID's progress on every challenge.

    Riot endpoint: ``lol-challenges-v1`` ``GET /lol/challenges/v1/player-data/{puuid}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw lol-challenges-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/challenges/v1/player-data/{puuid}")
