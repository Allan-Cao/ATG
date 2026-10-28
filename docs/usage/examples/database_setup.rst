################
 Database setup
################

ATG includes SQLAlchemy database models to simplify storing League of Legends data for
later analysis. A database is required to use the ``match_lib`` module and the ingestion
scripts.

.. tip::

    A database is **not** required to use the ``ATG.api`` module on its own. If you only
    need to call the Riot API, create a client with ``riot_client`` and call the
    endpoint functions directly. Each function returns the raw ``httpx2.Response``
    object, leaving parsing and storage up to you.

`PostgreSQL <https://www.postgresql.org/>`_ is the **required** database backend, as the
models make extensive use of ``JSONB`` columns to store structured esports data whose
schema changes over time.

****************
 Local database
****************

The recommended way to run PostgreSQL locally is with `Docker
<https://docs.docker.com/engine/install/>`_. A ``docker-compose.yml`` is provided to run
the PostgreSQL backend, reading its credentials from the same ``.env`` file.

.. code-block:: bash

    docker compose up -d

.. note::

    ``alembic upgrade head`` cannot build a database from scratch, as the migration
    history begins against an already populated database. ``get_session_factory``
    creates the schema on first connection; follow it with ``alembic stamp head`` to
    track migrations.
