from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff
from app.database import get_db
from app.models.cleaning import CleaningStatus, CleaningTask
from app.models.room import RoomStatus
from app.schemas.cleaning import CleaningTaskCreate, CleaningTaskResponse, CleaningTaskUpdate

router = APIRouter(prefix="/api/cleaning", tags=["cleaning"])


@router.get("", response_model=list[CleaningTaskResponse])
def list_tasks(db: Session = Depends(get_db), _: object = RequireStaff):
    return db.query(CleaningTask).order_by(CleaningTask.scheduled_at).all()


@router.post("", response_model=CleaningTaskResponse, status_code=201)
def create_task(data: CleaningTaskCreate, db: Session = Depends(get_db), _: object = RequireStaff):
    task = CleaningTask(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=CleaningTaskResponse)
def update_task(
    task_id: int,
    data: CleaningTaskUpdate,
    db: Session = Depends(get_db),
    _: object = RequireStaff,
):
    task = db.query(CleaningTask).filter(CleaningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router.post("/{task_id}/complete", response_model=CleaningTaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db), _: object = RequireStaff):
    task = db.query(CleaningTask).filter(CleaningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task.status = CleaningStatus.completed
    task.completed_at = datetime.now(timezone.utc)
    task.room.status = RoomStatus.available
    db.commit()
    db.refresh(task)
    return task
