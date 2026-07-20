from .sqlite_repository import SQLiteTaskRepository
from .service import TaskService

_repository = SQLiteTaskRepository()
_service = TaskService(_repository)

def get_service() -> TaskService:
    return _service