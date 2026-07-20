from fastapi import APIRouter, Depends, HTTPException, Response

from .dependencies import get_service
from .models import Task, TaskCreate, TaskUpdate
from .service import TaskService

router = APIRouter()


@router.get("/tasks", description="Get all tasks")
def get_tasks(service: TaskService = Depends(get_service)):
    return service.list_tasks()


@router.get("/tasks/{task_id}", description="Get one task")
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", status_code=201, description="Create a new task")
def create_task(task: TaskCreate, service: TaskService = Depends(get_service)):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    return service.create_task(task)


@router.put("/tasks/{task_id}", description="Update an existing task")
def update_task(task_id: int, task: TaskUpdate, service: TaskService = Depends(get_service)):
    updated = service.update_task(task_id, task)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}", description="Delete a task")
def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}