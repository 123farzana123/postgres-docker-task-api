from typing import Optional

from .models import Task, TaskCreate, TaskUpdate
from .repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.list_tasks()
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repository.get_task(task_id)

    def create_task(self, task: TaskCreate) -> Task:
        return self.repository.create_task(task)

    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        return self.repository.update_task(task_id, task)

    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete_task(task_id)