
from fastapi import FastAPI

from app.routes.tasks import router as tasks_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="Student Task Manager API",
    description="A task management API for students",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Student Task Manager API!",
        "status": "Running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(tasks_router)
app.include_router(auth_router)
