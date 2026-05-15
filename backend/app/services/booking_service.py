from datetime import date

from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.room import Room, RoomStatus
from app.schemas.booking import BookingCreate


def calculate_total_price(room: Room, check_in: date, check_out: date) -> float:
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Некорректный период бронирования")
    return round(room.price_per_night * nights, 2)


def has_overlapping_booking(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
    exclude_id: int | None = None,
) -> bool:
    query = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    )
    if exclude_id:
        query = query.filter(Booking.id != exclude_id)
    return query.first() is not None


def create_booking(db: Session, data: BookingCreate, created_by_id: int | None) -> Booking:
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise ValueError("Номер не найден")
    if room.price_per_night <= 0:
        raise ValueError("Цена номера должна быть положительной")
    if room.status == RoomStatus.maintenance:
        raise ValueError("Номер на обслуживании недоступен для бронирования")
    if has_overlapping_booking(db, data.room_id, data.check_in, data.check_out):
        raise ValueError("Номер занят на выбранные даты")

    total = calculate_total_price(room, data.check_in, data.check_out)
    booking = Booking(
        room_id=data.room_id,
        guest_id=data.guest_id,
        created_by_id=created_by_id,
        check_in=data.check_in,
        check_out=data.check_out,
        total_price=total,
        status=BookingStatus.confirmed,
        notes=data.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
