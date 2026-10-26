from httpx2 import Client, Response
from .utils import PLATFORM_ROUTING, parse_match_id, RegionLiteral
from ..rate_limiter import riot_api_limiter


@riot_api_limiter(endpoint_key="match_v5_by_id")
def get_match_by_id(client: Client, match_id: str, timeline: bool = False) -> Response:
    """Get a match, or its timeline, by match ID.

    The regional route is derived from the match ID, so no region needs to be
    passed.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param match_id: Match ID of the form ``"<REGION>_<GAME ID>"``.
    :type match_id: str
    :param timeline: Request the match timeline instead of the match itself,
        defaults to ``False``.
    :type timeline: bool
    :returns: The raw match-v5 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``match_id`` cannot be parsed.
    """
    region, _ = parse_match_id(match_id)
    is_timeline = "/timeline" if timeline else ""
    return client.get(
        f"https://{PLATFORM_ROUTING[region]}.api.riotgames.com/lol/match/v5/matches/{match_id}{is_timeline}"
    )


@riot_api_limiter(endpoint_key="match_v5_available_matches")
def get_available_matches(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> Response:
    """Get one page of match IDs for a PUUID.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``, mapped to its
        regional route.
    :type region: str
    :param kwargs: Additional query parameters accepted by the endpoint, such
        as ``start``, ``count``, ``startTime``, ``endTime``, ``queue`` and
        ``type``.
    :returns: The raw match-v5 response, whose body is a list of match IDs.
    :rtype: httpx2.Response
    """
    return client.get(
        f"https://{PLATFORM_ROUTING[region]}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids",
        params=kwargs,
    )


def get_match_history(
    client: Client, puuid: str, region: RegionLiteral, **kwargs
) -> list[str]:
    """Get every available match ID for a PUUID.

    Repeatedly calls :func:`get_available_matches` in pages of 100 until a page
    comes back empty. If a request fails, the IDs collected so far are returned
    rather than raising, so a short list is not proof that no more games exist.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param kwargs: Additional query parameters passed through to
        :func:`get_available_matches`. ``start`` and ``count`` are managed by
        the pagination and must not be passed.
    :returns: The match IDs found.
    :rtype: list[str]
    """
    start = 0
    count = 100
    match_history = []
    while True:
        match_list = get_available_matches(
            client,
            puuid=puuid,
            region=region,
            start=start,
            count=count,
            **kwargs,
        )
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
