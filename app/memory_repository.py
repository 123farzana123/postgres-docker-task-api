from .models import Task, TaskCreate, TaskUpdate
from typing import Optional
from .repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._tasks: list[Task] = [
            Task(id=1, title="Learn FastAPI", completed=False),
            Task(id=2, title="Build an API", completed=False),
        ]
        self._next_id = 3

    def list_tasks(self) -> list[Task]:
        return self._tasks

    def create_task(self, task: TaskCreate) -> Task:
        new_task = Task(id=self._next_id, title=task.title, completed=False)
        self._next_id = self._next_id + 1
        self._tasks.append(new_task)
        return new_task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        existing = self.get_task(task_id)
        if existing is None:
            return None
        existing.title = task.title
        existing.completed = task.completed
        return existing
    
    def delete_task(self, task_id: int) -> bool:
        existing = self.get_task(task_id)
        if existing is None:
            return False
        self._tasks.remove(existing)
        return True
