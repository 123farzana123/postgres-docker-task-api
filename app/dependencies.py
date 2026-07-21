from .postgres_repository import PostgresTaskRepository
from .service import TaskService

_repository = PostgresTaskRepository()
_service = TaskService(_repository)

def get_service() -> TaskService:
    return _service