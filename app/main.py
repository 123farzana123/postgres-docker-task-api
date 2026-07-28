from fastapi import FastAPI

from .routes import router

from .auth_routes import router as auth_router

app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks",
    version="1.0.0",
)

app.include_router(router)

app.include_router(auth_router)


@app.get("/", description="Welcome message for the API")
def home():
    return {"message": "Hello World"}


@app.get("/health", description="Check if the API is running")
def health_check():
    return {"status": "ok"}

