import sqlite3
from typing import Optional

from .models import Task, TaskCreate, TaskUpdate
from .repository import TaskRepository

DB_FILE = "tasks.db"


class SQLiteTaskRepository(TaskRepository):
    def __init__(self):
        self._init_db()

    def _connect(self):
        return sqlite3.connect(DB_FILE)

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        cur.execute("SELECT COUNT(*) FROM tasks")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [("Learn FastAPI", 0), ("Build an API", 0), ("Add a database", 0)],
            )
        conn.commit()
        conn.close()

    def list_tasks(self) -> list[Task]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks")
        rows = cur.fetchall()
        conn.close()
        return [Task(id=r[0], title=r[1], completed=bool(r[2])) for r in rows]

    def create_task(self, task: TaskCreate) -> Task:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (task.title,))
        new_id = cur.lastrowid
        conn.commit()
        conn.close()
        return Task(id=new_id, title=task.title, completed=False)

    def get_task(self, task_id: int) -> Optional[Task]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        conn.close()
        return Task(id=row[0], title=row[1], completed=bool(row[2])) if row else None

    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (task.title, int(task.completed), task_id),
        )
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return self.get_task(task_id) if updated else None

    def delete_task(self, task_id: int) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
        return deleted