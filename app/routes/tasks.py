
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task
from app.models.user import User
from app.database.connection import get_db
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Task not found"}
    }
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a task for the currently authenticated user."
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Get all tasks",
    description="Retrieve paginated tasks belonging to the authenticated user."
)
def get_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Task).filter(
        Task.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a task owned by the authenticated user."
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task



@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task owned by the authenticated user."
)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    summary="Delete a task",
    description="Delete a task owned by the authenticated user."
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
