########################
 API Naming Conventions
########################

Riot splits League of Legends data across many APIs (account-v1, summoner-v4, league-v4,
match-v5 and so on), each with its own routing rules. ATG hides that split: every helper
lives in ``ATG.api`` and is named for what it returns, not for the Riot API that serves
it.

*******
 Names
*******

``get_<thing>``
    Makes one request and returns the raw :class:`httpx2.Response`, so you decide how to
    handle status codes. Example: ``get_challengers``.

``get_<thing>_by_<key>``
    The same, looking ``<thing>`` up by ``<key>``. Example: ``get_summoner_by_puuid``,
    ``get_match_by_id``.

``get_all_<thing>…``
    Makes as many requests as it takes and returns the parsed data. Example:
    ``get_all_match_ids_by_puuid`` returns a ``list[str]``.

***********
 Arguments
***********

- The client and the identifiers being looked up are positional. Everything else is
  keyword-only:

  .. code-block:: python

      get_summoner_by_puuid(client, puuid, region="KR")
      get_league_entries(client, "GOLD", "II", region="NA1", page=2)

- ``region`` is always a platform, such as ``"NA1"``, ``"EUW1"`` or ``"KR"`` (see
  :data:`ATG.api.REGIONS`). The helper picks the right route for you. Match helpers take
  no region, as it is read from the match ID.
- ``region`` is required, except for account lookups: any account can be found from any
  route, so those default to ``"NA1"``.
- Riot's camelCase query parameters are snake_case, and times accept a
  :class:`datetime.datetime` or epoch seconds: ``get_match_ids_by_puuid(client, puuid,
  region="NA1", start_time=datetime(2025, 1, 9))``.
- Ranked helpers default ``queue`` to ``"RANKED_SOLO_5x5"``.

***************************
 Finding the Riot endpoint
***************************

Each helper's docstring names the Riot API and endpoint it calls, in the :doc:`../api`.
Its rate-limit key is that endpoint's Riot operation ID, such as
``league-v4.getChallengerLeague``.
