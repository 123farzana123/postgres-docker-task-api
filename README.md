# Task Manager API — with Supabase Authentication

A CRUD API built with FastAPI, backed by PostgreSQL (running in Docker), with
user authentication and route protection powered by Supabase Auth.

## What this project is

This started as a simple in-memory CRUD API for managing tasks, and evolved
in stages:
1. In-memory storage → SQLite → PostgreSQL (in Docker, with a persistent volume)
2. Open, unprotected endpoints → Supabase-backed authentication with
   protected routes, verified via Bearer tokens

The architecture keeps storage and authentication as separate, swappable
layers — routes call a service, which calls a repository interface;
auth is checked via a reusable FastAPI dependency, independent of the
task logic entirely.

## Setup — environment variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Required variables:

| Variable | Description |
|---|---|
| `POSTGRES_USER` | Postgres username (used by Docker Compose) |
| `POSTGRES_PASSWORD` | Postgres password |
| `POSTGRES_DB` | Postgres database name |
| `DATABASE_URL` | Full connection string (use `db` as host when running via Docker Compose, `localhost` when running the app directly on your machine) |
| `SUPABASE_URL` | Your Supabase project URL (Project Settings → API Keys) |
| `SUPABASE_KEY` | Your Supabase anon public key (same page) |

`.env` is gitignored — never commit real credentials. `.env.example` is
committed as a template with no real values.

## How to run

**Option 1 — full stack via Docker Compose** (app + Postgres together):
```bash
docker compose up --build
```

**Option 2 — running the API locally** (useful for fast iteration; requires
the Postgres container running separately, and `DATABASE_URL` in `.env`
pointed at `localhost` instead of `db`):
```bash
docker compose up -d db
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Either way, visit `http://localhost:8000/docs` for interactive API docs.

## API Reference

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| POST | `/auth/signup` | No | Create a new account (email + password) |
| POST | `/auth/login` | No | Log in, returns an access token |
| POST | `/auth/logout` | Yes (Bearer token) | End the current session |
| GET | `/public/info` | No | Public, unprotected message |
| GET | `/protected/profile` | Yes (Bearer token) | Returns the logged-in user's id, email, created_at |
| GET | `/protected/dashboard` | Yes (Bearer token) | Personalized welcome message, proves the auth dependency is reusable |
| GET | `/tasks` | No | List all tasks |
| POST | `/tasks` | No | Create a task |
| GET | `/tasks/{id}` | No | Get one task |
| PUT | `/tasks/{id}` | No | Update a task |
| DELETE | `/tasks/{id}` | No | Delete a task |

## Testing authentication

1. `POST /auth/signup` with a new email/password → 201
2. `POST /auth/login` with the same credentials → 200, returns `access_token`
3. Click **Authorize** in `/docs`, paste the token
4. `GET /protected/profile` → 200, returns your user info
5. `GET /protected/dashboard` → 200, personalized message
6. `POST /auth/logout` → 204

Swagger UI, showing the padlock icons and Authorize button on protected
routes:

![Swagger UI screenshot](swagger-screenshot.png)

## Notes on this implementation

- Token verification uses `supabase.auth.get_user(token)` — Supabase checks
  the token's validity, expiry, and signature; we never handle passwords or
  cryptography ourselves.
- Auth checking is centralized in `app/auth_dependency.py` as a single
  reusable dependency (`get_current_user`), applied via FastAPI's `Depends()`
  to every protected route — not duplicated per-route.
- Email confirmation is disabled in this Supabase project for local
  development convenience (Authentication → Providers → Email → "Confirm
  email" toggled off). In production, this would stay enabled.