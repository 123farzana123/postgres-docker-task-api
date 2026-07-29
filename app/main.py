from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .routes import router

from .auth_routes import router as auth_router

app = FastAPI(
    title="Task Manager API",
    description="A CRUD API for managing tasks, with Supabase-backed authentication",
    version="1.0.0",
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


app.include_router(router)
app.include_router(auth_router)


@app.get("/", description="Welcome message for the API")
def home():
    return {"message": "Hello World"}


@app.get("/health", description="Check if the API is running")
def health_check():
    return {"status": "ok"}

