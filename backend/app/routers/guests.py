from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff, get_current_user
from app.database import get_db
from app.models.guest import Guest
from app.models.user import User
from app.schemas.guest import GuestCreate, GuestResponse, GuestUpdate

router = APIRouter(prefix="/api/guests", tags=["guests"])


@router.get("", response_model=list[GuestResponse])
def list_guests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Guest).offset(skip).limit(limit).all()


@router.post("", response_model=GuestResponse, status_code=201)
def create_guest(data: GuestCreate, db: Session = Depends(get_db), _: User = RequireStaff):
    if data.email and db.query(Guest).filter(Guest.email == data.email).first():
        raise HTTPException(status_code=400, detail="Гость с таким email уже существует")
    guest = Guest(**data.model_dump())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


@router.patch("/{guest_id}", response_model=GuestResponse)
def update_guest(
    guest_id: int,
    data: GuestUpdate,
    db: Session = Depends(get_db),
    _: User = RequireStaff,
):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Гость не найден")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(guest, key, value)
    db.commit()
    db.refresh(guest)
    return guest


@router.delete("/{guest_id}", status_code=204)
def delete_guest(guest_id: int, db: Session = Depends(get_db), _: User = RequireStaff):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Гость не найден")
    if guest.bookings:
        raise HTTPException(status_code=400, detail="Нельзя удалить гостя с бронированиями")
    db.delete(guest)
    db.commit()
