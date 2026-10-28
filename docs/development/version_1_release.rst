=================
1.X Release Notes
=================

As of version 1.X, PostgreSQL is the **required** database backend due to the
use of JSONB columns which are declared using the
``sqlalchemy.dialects.postgresql.JSONB`` datatype.

I have decided to bump the major version since this library is mature enough
for my production needs *however* expect extensive schema changes as I look to
fully mature my database models.

Although naming initially reflects the match-v5 API's choices and the
terminology used by GRID esports, I've had to make some changes.

Here are the major differences / exceptions that should be noted.

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Key used
     - Meaning
     - Examples
   * - ``Series``
     - A collection of related games
     - A series has many games
   * - ``source_data``
     - Raw/unprocessed/additional data
     - Specifically in ``ParticipantStats`` we store the unprocessed
       ``match_v5`` columns here
   * - ``X_id``
     - table_id; Foreign key name
     - ``champion_id``, ``game_id``
   * - ``team_id``
     - Blue / red sides
     - 100 - Blue, 200 - Red
   * - ``participant_id``
     - The "#" of the participant
     - From 1 - 10 representing blue top -> red bottom most of the time.