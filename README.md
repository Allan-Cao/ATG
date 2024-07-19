# SQDBI - Solo Queue Database Ingest

Models and scripts to store riot summary files for a database of players.

## Alembic Commands

```bash
alembic revision -m "changes"
alembic upgrade head
alembic downgrade base
```

## FastAPI

** Run the FastAPI server with the following command: **
```bash
cd api
fastapi dev main.py
```
