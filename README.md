# ATG - All The Games

Opinionated but flexible library of database models and scripts to store solo queue / competitive player data tailored for LoL Esports.

#### Verson 1.0
As of version 1.0, PostgreSQL is now required as we extensively use the JSONB functionality to efficiently store and query stats and minimize schema changes.

Although I've decided to use a version number >= 1, do expect schema changes and functionality to break at any point. With the use of JSONB columns, the core schema and functionality of the library, storing Match-V5 JSONs, should be more or less stable but expect less stability as I look to develop esports tournament/draft support.


## Features
- Ratelimited functions to access Riot & GRID APIs with smart region handling
- SQLAlchemy database models compatible with solo queue & esports games
- Ability to store complete Match-V5 JSON objects
- Scripts to insert/manage solo queue accounts & games

## Todo
- Properly handle API error codes
- Handle draft data / other available esports data
- Open source GRID ingest code

## Virtualenv

Please use a virtual environment to manage dependencies.

```bash
python -m virtualenv .venv
source .venv/bin/activate
```

To setup the project

```bash
python -m pip install -r requirements.txt
```

On Linux, to satisfy psycopg2 in a virtual environment, you may need to run
```bash
sudo apt-get install libpq-dev
```

## Alembic Commands

```bash
alembic revision --autogenerate -m "changes"
alembic upgrade head
alembic downgrade base
```
