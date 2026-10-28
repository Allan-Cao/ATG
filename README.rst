===================
ATG - All The Games
===================

.. image:: https://img.shields.io/pypi/v/ATG-lib?label=latest
   :target: https://pypi.org/project/ATG-lib/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/ATG-lib
   :target: https://pypi.org/project/ATG-lib/
   :alt: Python Versions

.. image:: https://img.shields.io/pypi/l/ATG-lib
   :target: https://github.com/Allan-Cao/ATG/blob/main/LICENSE
   :alt: License

**ATG makes it easy to collect, store League of Legends data.**

ATG is an opinionated but flexible library that handles the complexities of the Riot API
and the data it returns. It provides region-aware functions and rate limiters for the Riot API,
PostgreSQL database models to store solo queue and competitive games, players and teams,
and functions to ingest and manage that data.

  This library is currently under `active development <https://atg.readthedocs.io/en/latest/development/todo.html>`_; expect breaking changes before 2.0.

Features
========

- Functions for the League of Legends Riot API endpoints with platform to regional routing handled for you
- Header-based rate limiting
- SQLAlchemy database models compatible with both solo queue & esports games
- Database models to store Riot esports game event (JSONL) data
- Ingestion of Match-V5 data, with unmapped fields kept in JSONB columns
- Functions to update solo queue account names & store new solo queue games

For more information on this library, refer to `the documentation <https://atg.readthedocs.io/en/latest/>`_

Installation
============

The following command will install ATG from the `Python Package Index <https://pypi.org/project/ATG-lib/>`_. You will
need a working installation of Python and pip.

.. code-block:: shell

    pip install -U ATG-lib

