from typing import List, Optional

from .db import get_connection, put_connection
from .models import Task, TaskCreate, TaskUpdate
from .repository import TaskRepository


class PostgresTaskRepository(TaskRepository):

    def list_tasks(self) -> List[Task]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, completed FROM tasks ORDER BY id")
                rows = cur.fetchall()
            return [Task(id=r[0], title=r[1], completed=r[2]) for r in rows]
        finally:
            put_connection(conn)

    def create_task(self, task: TaskCreate) -> Task:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title, completed) VALUES (%s, %s) "
                    "RETURNING id, title, completed",
                    (task.title, False),
                )
                row = cur.fetchone()
            conn.commit()
            return Task(id=row[0], title=row[1], completed=row[2])
        finally:
            put_connection(conn)

    def get_task(self, task_id: int) -> Optional[Task]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, title, completed FROM tasks WHERE id = %s",
                    (task_id,),
                )
                row = cur.fetchone()
            return Task(id=row[0], title=row[1], completed=row[2]) if row else None
        finally:
            put_connection(conn)

    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tasks SET title = %s, completed = %s WHERE id = %s "
                    "RETURNING id, title, completed",
                    (task.title, task.completed, task_id),
                )
                row = cur.fetchone()
            conn.commit()
            return Task(id=row[0], title=row[1], completed=row[2]) if row else None
        finally:
            put_connection(conn)

    def delete_task(self, task_id: int) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                deleted = cur.rowcount > 0
            conn.commit()
            return deleted
        finally:
            put_connection(conn)