from httpx2 import Client, Response
from .utils import Region, platform_url
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="clash-v1.getPlayersByPUUID")
def get_clash_players_by_puuid(
    client: Client, puuid: str, *, region: Region
) -> Response:
    """Get a PUUID's active Clash registrations.

    Riot endpoint: ``clash-v1`` ``GET /lol/clash/v1/players/by-puuid/{puuid}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw clash-v1 response, with one entry per registered
        tournament.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/clash/v1/players/by-puuid/{puuid}")


@riot_api_limiter(endpoint_key="clash-v1.getTeamById")
def get_clash_team_by_id(client: Client, team_id: str, *, region: Region) -> Response:
    """Get a Clash team by ID.

    Riot endpoint: ``clash-v1`` ``GET /lol/clash/v1/teams/{teamId}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param team_id: The Clash team's ID.
    :type team_id: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw clash-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/clash/v1/teams/{team_id}")


@riot_api_limiter(endpoint_key="clash-v1.getTournaments")
def get_clash_tournaments(client: Client, *, region: Region) -> Response:
    """Get every active and upcoming Clash tournament.

    Riot endpoint: ``clash-v1`` ``GET /lol/clash/v1/tournaments``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw clash-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(f"{platform_url(region)}/lol/clash/v1/tournaments")


@riot_api_limiter(endpoint_key="clash-v1.getTournamentById")
def get_clash_tournament_by_id(
    client: Client, tournament_id: int, *, region: Region
) -> Response:
    """Get a Clash tournament by ID.

    Riot endpoint: ``clash-v1`` ``GET /lol/clash/v1/tournaments/{tournamentId}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param tournament_id: The Clash tournament's ID.
    :type tournament_id: int
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw clash-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/clash/v1/tournaments/{tournament_id}"
    )


@riot_api_limiter(endpoint_key="clash-v1.getTournamentByTeam")
def get_clash_tournament_by_team_id(
    client: Client, team_id: str, *, region: Region
) -> Response:
    """Get the Clash tournament a team is registered for.

    Riot endpoint: ``clash-v1`` ``GET /lol/clash/v1/tournaments/by-team/{teamId}``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param team_id: The Clash team's ID.
    :type team_id: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :returns: The raw clash-v1 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    return client.get(
        f"{platform_url(region)}/lol/clash/v1/tournaments/by-team/{team_id}"
    )
