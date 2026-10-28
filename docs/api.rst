=============
API Reference
=============

Riot API endpoints
==================

Helpers are grouped by what they look up rather than by Riot API. See
:doc:`development/conventions` for how they are named and called.

.. code-block:: python

   from ATG.api import riot_client, get_account_by_riot_id, get_all_match_ids_by_puuid

   client = riot_client(api_key)
   puuid = get_account_by_riot_id(client, "Hide on bush", "KR1").json()["puuid"]
   match_ids = get_all_match_ids_by_puuid(client, puuid, region="KR", queue=420)

Client
------

.. autofunction:: ATG.api.riot_client

Accounts
--------

Any account can be looked up from any account route, so ``region`` defaults to
``"NA1"`` here and only picks the nearest route.

.. autofunction:: ATG.api.get_account_by_riot_id
.. autofunction:: ATG.api.get_account_by_puuid
.. autofunction:: ATG.api.get_region_by_puuid
.. autofunction:: ATG.api.get_summoner_by_puuid

Ranked
------

.. autofunction:: ATG.api.get_league_entries_by_puuid
.. autofunction:: ATG.api.get_challengers
.. autofunction:: ATG.api.get_grandmasters
.. autofunction:: ATG.api.get_masters
.. autofunction:: ATG.api.get_league_entries

Matches
-------

.. autofunction:: ATG.api.get_match_by_id
.. autofunction:: ATG.api.get_match_timeline_by_id
.. autofunction:: ATG.api.get_match_ids_by_puuid
.. autofunction:: ATG.api.get_all_match_ids_by_puuid
.. autofunction:: ATG.api.parse_match_id

Live games
----------

.. autofunction:: ATG.api.get_active_game_by_puuid

Champion mastery
----------------

.. autofunction:: ATG.api.get_champion_masteries_by_puuid
.. autofunction:: ATG.api.get_champion_mastery_by_puuid
.. autofunction:: ATG.api.get_top_champion_masteries_by_puuid
.. autofunction:: ATG.api.get_mastery_score_by_puuid

Champions
---------

.. autofunction:: ATG.api.get_free_champion_rotation
.. autofunction:: ATG.api.get_ddragon_versions

Challenges
----------

.. autofunction:: ATG.api.get_challenges_by_puuid
.. autofunction:: ATG.api.get_challenge_configs
.. autofunction:: ATG.api.get_challenge_config_by_id
.. autofunction:: ATG.api.get_challenge_percentiles
.. autofunction:: ATG.api.get_challenge_percentiles_by_id
.. autofunction:: ATG.api.get_challenge_leaderboard

Clash
-----

.. autofunction:: ATG.api.get_clash_players_by_puuid
.. autofunction:: ATG.api.get_clash_team_by_id
.. autofunction:: ATG.api.get_clash_tournaments
.. autofunction:: ATG.api.get_clash_tournament_by_id
.. autofunction:: ATG.api.get_clash_tournament_by_team_id

Server status
-------------

.. autofunction:: ATG.api.get_server_status

Regions & ranked values
-----------------------

.. autodata:: ATG.api.REGIONS
.. autodata:: ATG.api.QUEUES
.. autodata:: ATG.api.TIERS
.. autodata:: ATG.api.DIVISIONS

Match ingestion
===============

.. automodule:: ATG.match_lib
   :members:

Database
========

.. automodule:: ATG.database
   :members:

Rate limiting
=============

.. automodule:: ATG.rate_limiter
   :members:

Constants & helpers
===================

.. automodule:: ATG.utils
   :members:
