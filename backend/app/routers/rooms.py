from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff, get_current_user
from app.database import get_db
from app.models.room import Room, RoomStatus
from app.models.user import User
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomResponse])
def list_rooms(
    status: RoomStatus | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Room)
    if status:
        query = query.filter(Room.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return room


@router.post("", response_model=RoomResponse, status_code=201)
def create_room(
    data: RoomCreate,
    db: Session = Depends(get_db),
    _: User = RequireStaff,
):
    if db.query(Room).filter(Room.number == data.number).first():
        raise HTTPException(status_code=400, detail="Номер с таким номером уже существует")
    room = Room(**data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    data: RoomUpdate,
    db: Session = Depends(get_db),
    _: User = RequireStaff,
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db), _: User = RequireStaff):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")
    if room.bookings:
        raise HTTPException(status_code=400, detail="Нельзя удалить номер с бронированиями")
    db.delete(room)
    db.commit()
