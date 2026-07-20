from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks",
    version="1.0.0",
)

app.include_router(router)


@app.get("/", description="Welcome message for the API")
def home():
    return {"message": "Hello World"}


@app.get("/health", description="Check if the API is running")
def health_check():
    return {"status": "ok"}