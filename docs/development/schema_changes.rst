################
 Schema changes
################

When schema changes are made, Alembic is used to automatically generate a script to
apply the changes to the database. When a commit will cause a schema change, an alembic
script should be attached to the commit.

To create and apply the script, run the following:

.. code-block:: bash

    alembic revision --autogenerate -m "changes"
    alembic upgrade head
