from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff
from app.database import get_db
from app.models.booking import Booking, BookingStatus
from app.models.room import RoomStatus
from app.models.stay import Stay, StayStatus
from app.schemas.stay import StayCreate, StayResponse

router = APIRouter(prefix="/api/stays", tags=["stays"])


@router.get("", response_model=list[StayResponse])
def list_stays(db: Session = Depends(get_db), _: object = RequireStaff):
    return db.query(Stay).all()


@router.post("/check-in", response_model=StayResponse, status_code=201)
def check_in(data: StayCreate, db: Session = Depends(get_db), _: object = RequireStaff):
    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    if booking.status == BookingStatus.cancelled:
        raise HTTPException(status_code=400, detail="Бронирование отменено")
    if db.query(Stay).filter(Stay.booking_id == data.booking_id).first():
        raise HTTPException(status_code=400, detail="Заезд уже оформлен")
    now = datetime.now(timezone.utc)
    stay = Stay(booking_id=data.booking_id, actual_check_in=now, status=StayStatus.active)
    booking.status = BookingStatus.completed
    booking.room.status = RoomStatus.occupied
    db.add(stay)
    db.commit()
    db.refresh(stay)
    return stay


@router.post("/{stay_id}/check-out", response_model=StayResponse)
def check_out(stay_id: int, db: Session = Depends(get_db), _: object = RequireStaff):
    stay = db.query(Stay).filter(Stay.id == stay_id).first()
    if not stay:
        raise HTTPException(status_code=404, detail="Проживание не найдено")
    if stay.status != StayStatus.active:
        raise HTTPException(status_code=400, detail="Проживание уже завершено")
    now = datetime.now(timezone.utc)
    stay.actual_check_out = now
    stay.status = StayStatus.completed
    stay.booking.room.status = RoomStatus.cleaning
    db.commit()
    db.refresh(stay)
    return stay
