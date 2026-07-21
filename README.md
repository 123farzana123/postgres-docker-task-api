# Task Manager API

A CRUD API built with FastAPI, backed by PostgreSQL, running in Docker.

## Architecture

routes.py -> service.py -> repository.py (interface) -> postgres_repository.py

**Honest note:** switching storage from SQLite to Postgres only required
writing `postgres_repository.py` and changing two lines in
`app/dependencies.py` (which repository class gets instantiated).
`routes.py`, `service.py`, and `models.py` were not touched.

## Running it

```bash
cp .env.example .env      # already done in this repo for convenience
docker compose up --build
```

This starts Postgres (with a named volume `pgdata`) and the FastAPI app
together, in the correct order (app waits for Postgres to report healthy).
API available at http://localhost:8000, docs at http://localhost:8000/docs.

## Proving persistence

1. `docker compose up --build`
2. Created a task via `POST /tasks` (`{"title": "Survive a restart"}`)
3. Confirmed it via `GET /tasks`
4. Ran `docker compose down` (stops and removes both containers)
5. Ran `docker compose up` again
6. `GET /tasks` still showed the new task, along with the two seed tasks
   from `sql/init.sql` (seed data does not duplicate, since the init
   script only runs once, on first volume creation)

This confirms data survives both an app restart and a full container
restart, because Postgres's data directory lives in the named volume
`pgdata`, not inside the container itself.

## Environment variables

See `.env.example`. `.env` is gitignored since it holds connection details.