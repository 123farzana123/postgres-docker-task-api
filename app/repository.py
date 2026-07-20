from abc import ABC, abstractmethod
from typing import Optional
from .models import Task, TaskCreate, TaskUpdate

class TaskRepository(ABC):
    @abstractmethod
    def list_tasks(self) -> list[Task]:
        ...

    @abstractmethod
    def create_task(self, task: TaskCreate) -> Task:
        ...

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        ...

    @abstractmethod
    def update_task(self, task_id: int, task: TaskUpdate) -> Optional[Task]:
        ...   

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        ...