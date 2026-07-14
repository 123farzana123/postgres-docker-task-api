from fastapi import FastAPI, Body

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks",
    version="1.0.0"
)

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "title": "Build an API",
        "completed": False
    }
]

@app.get("/", description="Welcome message for the API")
def home():
    return {"message": "Hello World"}

@app.get("/health", description="Check if the API is running")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", description="Get all tasks") 
def get_tasks():
    return tasks

@app.post("/tasks", description="Create a new task")
def create_task(task: dict = Body(...)):
    new_task = {
        "id":len(tasks) + 1,
        "title": task["title"],
        "completed": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}", description="Update an existing task")
def update_task(task_id: int, task: dict = Body(...)):
    for item in tasks:
        if item["id"] == task_id:
            item["title"] = task["title"]
            item["completed"] = task["completed"]
            return item

    return {"error": "Task not found"}

@app.delete("/tasks/{task_id}", description="Delete a task")
def delete_task(task_id: int):
    for item in tasks:
        if item["id"] == task_id:
            tasks.remove(item)
            return {"message": "Task deleted"}

    return {"error": "Task not found"}