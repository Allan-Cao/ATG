# ATG - All The Games

Opinionated library of database models and scripts to store solo queue / competitive player data tailored for LoL Esports.

## Features
- Ratelimited functions to access Riot & GRID APIs.
- SQLAlchemy database models compatible with solo queue & esports games
- Scripts to insert/manage solo queue accounts & games.

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


## Alembic Commands

```bash
alembic revision --autogenerate -m "changes"
alembic upgrade head
alembic downgrade base
```
