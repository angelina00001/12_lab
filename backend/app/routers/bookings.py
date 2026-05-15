from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff, get_current_user
from app.database import get_db
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.services import booking_service

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def _to_response(booking: Booking) -> BookingResponse:
    return BookingResponse(
        id=booking.id,
        room_id=booking.room_id,
        guest_id=booking.guest_id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=booking.total_price,
        status=booking.status,
        notes=booking.notes or "",
        nights=booking.nights(),
    )


@router.get("", response_model=list[BookingResponse])
def list_bookings(
    status: BookingStatus | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Booking)
    if status:
        query = query.filter(Booking.status == status)
    return [_to_response(b) for b in query.offset(skip).limit(limit).all()]


@router.post("", response_model=BookingResponse, status_code=201)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = RequireStaff,
):
    try:
        booking = booking_service.create_booking(db, data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return _to_response(booking)


@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    data: BookingUpdate,
    db: Session = Depends(get_db),
    _: User = RequireStaff,
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    updates = data.model_dump(exclude_unset=True)
    check_in = updates.get("check_in", booking.check_in)
    check_out = updates.get("check_out", booking.check_out)
    if check_out <= check_in:
        raise HTTPException(status_code=400, detail="Некорректные даты")
    if "check_in" in updates or "check_out" in updates:
        if booking_service.has_overlapping_booking(db, booking.room_id, check_in, check_out, booking.id):
            raise HTTPException(status_code=400, detail="Номер занят на выбранные даты")
    for key, value in updates.items():
        setattr(booking, key, value)
    db.commit()
    db.refresh(booking)
    return _to_response(booking)


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), _: User = RequireStaff):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    booking.status = BookingStatus.cancelled
    db.commit()
    db.refresh(booking)
    return _to_response(booking)
