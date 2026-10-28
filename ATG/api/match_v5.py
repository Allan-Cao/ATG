import logging
from datetime import datetime
from httpx2 import Client, HTTPStatusError, Response
from .utils import MatchType, Region, epoch_seconds, parse_match_id, regional_url
from ..rate_limiter import riot_api_limiter

logger = logging.getLogger(__name__)


@riot_api_limiter(endpoint_key="match-v5.getMatch")
def get_match_by_id(client: Client, match_id: str) -> Response:
    """Get a match by match ID.

    Riot endpoint: ``match-v5`` ``GET /lol/match/v5/matches/{matchId}``.

    The regional route is derived from the match ID, so no region needs to be
    passed.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param match_id: Match ID of the form ``"<REGION>_<GAME ID>"``.
    :type match_id: str
    :returns: The raw match-v5 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``match_id`` cannot be parsed.
    """
    region, _ = parse_match_id(match_id)
    return client.get(f"{regional_url(region)}/lol/match/v5/matches/{match_id}")


@riot_api_limiter(endpoint_key="match-v5.getTimeline")
def get_match_timeline_by_id(client: Client, match_id: str) -> Response:
    """Get a match timeline by match ID.

    Riot endpoint: ``match-v5`` ``GET /lol/match/v5/matches/{matchId}/timeline``.

    The regional route is derived from the match ID, so no region needs to be
    passed.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param match_id: Match ID of the form ``"<REGION>_<GAME ID>"``.
    :type match_id: str
    :returns: The raw match-v5 response.
    :rtype: httpx2.Response
    :raises ValueError: If ``match_id`` cannot be parsed.
    """
    region, _ = parse_match_id(match_id)
    return client.get(
        f"{regional_url(region)}/lol/match/v5/matches/{match_id}/timeline"
    )


@riot_api_limiter(endpoint_key="match-v5.getMatchIdsByPUUID")
def get_match_ids_by_puuid(
    client: Client,
    puuid: str,
    *,
    region: Region,
    start: int = 0,
    count: int = 20,
    queue: int | None = None,
    match_type: MatchType | None = None,
    start_time: datetime | int | None = None,
    end_time: datetime | int | None = None,
) -> Response:
    """Get one page of match IDs for a PUUID, newest first.

    Riot endpoint: ``match-v5`` ``GET /lol/match/v5/matches/by-puuid/{puuid}/ids``.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``, mapped to its
        regional route for you.
    :type region: str
    :param start: Index of the first match ID to return, defaults to ``0``.
    :type start: int
    :param count: Number of match IDs to return, from ``0`` to ``100``,
        defaults to ``20``.
    :type count: int
    :param queue: Only return matches from this queue ID, such as ``420`` for
        ranked solo/duo.
    :type queue: int | None
    :param match_type: Only return matches of this type.
    :type match_type: str | None
    :param start_time: Only return matches played after this time. Riot only
        has timestamps for matches played after June 16th, 2021.
    :type start_time: datetime.datetime | int | None
    :param end_time: Only return matches played before this time.
    :type end_time: datetime.datetime | int | None
    :returns: The raw match-v5 response, whose body is a list of match IDs.
    :rtype: httpx2.Response
    :raises ValueError: If ``region`` is not a known platform.
    """
    params = {
        "start": start,
        "count": count,
        "queue": queue,
        "type": match_type,
        "startTime": epoch_seconds(start_time),
        "endTime": epoch_seconds(end_time),
    }
    return client.get(
        f"{regional_url(region)}/lol/match/v5/matches/by-puuid/{puuid}/ids",
        params={k: v for k, v in params.items() if v is not None},
    )


def get_all_match_ids_by_puuid(
    client: Client,
    puuid: str,
    *,
    region: Region,
    queue: int | None = None,
    match_type: MatchType | None = None,
    start_time: datetime | int | None = None,
    end_time: datetime | int | None = None,
) -> list[str]:
    """Get every available match ID for a PUUID, newest first.

    Repeatedly calls :func:`get_match_ids_by_puuid` in pages of 100 until a
    page comes back empty. If a request fails, a warning is logged and the IDs
    collected so far are returned rather than raising, so a short list is not
    proof that no more games exist.

    :param client: Client carrying the Riot API key.
    :type client: httpx2.Client
    :param puuid: The account's PUUID.
    :type puuid: str
    :param region: Platform routing value, such as ``"NA1"``.
    :type region: str
    :param queue: Only return matches from this queue ID, such as ``420`` for
        ranked solo/duo.
    :type queue: int | None
    :param match_type: Only return matches of this type.
    :type match_type: str | None
    :param start_time: Only return matches played after this time.
    :type start_time: datetime.datetime | int | None
    :param end_time: Only return matches played before this time.
    :type end_time: datetime.datetime | int | None
    :returns: The match IDs found.
    :rtype: list[str]
    :raises ValueError: If ``region`` is not a known platform.
    """
    start = 0
    count = 100
    match_ids = []
    while True:
        response = get_match_ids_by_puuid(
            client,
            puuid,
            region=region,
            start=start,
            count=count,
            queue=queue,
            match_type=match_type,
            start_time=start_time,
            end_time=end_time,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError:
            logger.warning(
                "%s - Failed to retrieve match history for %s",
                response.status_code,
                puuid,
            )
            return match_ids
        page = response.json()
        if len(page) == 0:
            return match_ids
        match_ids.extend(page)
        start += count
