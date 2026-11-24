from fastapi import FastAPI
from app.routes.tasks import router as tasks_router
from app.database.connection import engine, Base
from app.models.task import Task

app = FastAPI(
    title="Student Task Manager API",
    description="A task management API for students",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


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