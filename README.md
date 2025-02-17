# ATG - All The Games

Opinionated but flexible library of database models and scripts to store solo queue / competitive player data tailored for LoL Esports.

#### Verson 1.0
As of version 1.0, PostgreSQL is the required database backend since JSONB columns are extensively used to easily store game stats while minimizing schema changes.

Although I've decided to use a version number >= 1, do expect schema changes and functionality to break at any point. With the use of JSONB columns, the core schema and functionality of the library, storing Match-V5 JSONs/Riot "summary" files and accounts linked to players will remain stable. However, expect changes to the esports tournament/draft models as I look to add support for saving drafts / additional match information.


## Features
- Ratelimited functions to access Riot & GRID APIs with smart region handling
- SQLAlchemy database models compatible with both solo queue & esports games
- Ability to store complete Match-V5 JSON objects
- Scripts to insert/manage solo queue accounts & store new solo queue games

## Todo
- Properly handle API error codes
- Handle database sessions better using dependency injection or something other than passing session objects around.
- Add the ability to store draft / other available esports game information
- Open source GRID API code and GRID insertion scripts

## Setup & Example Usage

It is recommended to use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) when directly running this library's scripts.

Setup dependencies
```bash
pip install -r requirements.txt
```

Edit the .env file with your Riot API key and database connection string. The [psycopg3 database driver](https://www.psycopg.org/psycopg3/docs/basic/install.html) is installed and recommended.

```bash
python main.py
```

## Schema changes - Alembic commands

In the case of schema changes, Alembic allows us to automatically generate a script to apply the changes to the database. When a commit will cause a schema change, an alembic script should be attached to the commit.

```bash
alembic revision --autogenerate -m "changes"
alembic upgrade head
```
