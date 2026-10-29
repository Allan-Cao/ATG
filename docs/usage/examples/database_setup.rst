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

***************************
 Setting up a new database
***************************

1. Install ATG in your project:

   .. code-block:: bash

       pip install -U ATG-lib

2. Create a ``.env`` file in your project, based on the project's `EXAMPLE.env
   <https://github.com/Allan-Cao/ATG/blob/main/EXAMPLE.env>`_. The ``POSTGRES_*`` values
   set the database credentials, and ``DB_CONNECTION`` is built from them.

   .. literalinclude:: ../../../EXAMPLE.env
       :caption: .env
       :language: bash

3. Start PostgreSQL. The recommended way to run it locally is with `Docker
   <https://docs.docker.com/engine/install/>`_. Save the project's `docker-compose.yml
   <https://github.com/Allan-Cao/ATG/blob/main/docker-compose.yml>`_ next to your
   ``.env``, which it reads its credentials from, and start it:

   .. literalinclude:: ../../../docker-compose.yml
       :caption: docker-compose.yml
       :language: yaml

   .. code-block:: bash

       docker compose up -d

   To use an existing PostgreSQL server instead, point ``DB_CONNECTION`` at it.

4. Create the tables by running :download:`create_tables.py
   <../../_static/create_tables.py>` from the directory containing your ``.env``:

   .. literalinclude:: ../../_static/create_tables.py
       :caption: create_tables.py
       :language: python

   .. code-block:: bash

       python create_tables.py

.. warning::

    ATG does not ship its migrations yet. When you upgrade ATG, you must apply any
    schema changes to your database yourself.
