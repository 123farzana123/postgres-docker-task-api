# Task Manager API

A CRUD API built with FastAPI, backed by SQLite.

## Why SQLite

SQLite was chosen because it requires no separate installation or server setup —
the entire database lives in a single file (`tasks.db`) that Python's built-in
`sqlite3` module can read and write directly. This makes it ideal for local
development: anyone who clones this repo can run the project immediately,
with no database server to configure.

## Where the database lives

The database file `tasks.db` is created automatically in the project's root
folder the first time the app runs. It is gitignored, since it's local data,
not source code — anyone running the project gets a fresh file, auto-seeded
with 3 example tasks.

## Architecture

Routes call a service layer, which calls a repository interface
(`TaskRepository`). `SQLiteTaskRepository` is the current implementation —
swapping storage later (e.g. to Postgres) only requires writing a new
repository class and changing one line in `dependencies.py`. Routes and
service logic do not change.

## How to run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for interactive API docs.

## Database viewer

Data was inspected using [DB Browser for SQLite](https://sqlitebrowser.org/).

![DB Browser screenshot](screenshot.png)

Example query run directly against the database:

```sql
SELECT * FROM tasks;
```

## Proving persistence

1. Created a task via `POST /tasks`
2. Confirmed it via `GET /tasks`
3. Restarted the server completely
4. Ran `GET /tasks` again — the task was still present, confirming data
   survives a restart (unlike the in-memory version from Assignment 1)