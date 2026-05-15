from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.cleaning import CleaningTask, CleaningStatus
from app.models.room import Room, RoomStatus
from app.models.stay import Stay, StayStatus


def occupancy_report(db: Session, from_date: date, to_date: date) -> dict:
    total_rooms = db.query(Room).count()
    active_bookings = (
        db.query(Booking)
        .filter(
            Booking.status.in_([BookingStatus.confirmed, BookingStatus.completed]),
            Booking.check_in <= to_date,
            Booking.check_out >= from_date,
        )
        .count()
    )
    occupied_rooms = db.query(Room).filter(Room.status == RoomStatus.occupied).count()
    rate = round((occupied_rooms / total_rooms * 100) if total_rooms else 0, 2)
    return {
        "period": {"from": str(from_date), "to": str(to_date)},
        "total_rooms": total_rooms,
        "active_bookings_in_period": active_bookings,
        "currently_occupied": occupied_rooms,
        "occupancy_rate_percent": rate,
    }


def revenue_report(db: Session, from_date: date, to_date: date) -> dict:
    total = (
        db.query(func.coalesce(func.sum(Booking.total_price), 0.0))
        .filter(
            Booking.status != BookingStatus.cancelled,
            Booking.check_in >= from_date,
            Booking.check_in <= to_date,
        )
        .scalar()
    )
    by_status = (
        db.query(Booking.status, func.count(Booking.id), func.sum(Booking.total_price))
        .filter(Booking.check_in >= from_date, Booking.check_in <= to_date)
        .group_by(Booking.status)
        .all()
    )
    return {
        "period": {"from": str(from_date), "to": str(to_date)},
        "total_revenue": float(total or 0),
        "breakdown": [
            {"status": s.value, "count": c, "revenue": float(r or 0)} for s, c, r in by_status
        ],
    }


def cleaning_report(db: Session) -> dict:
    pending = db.query(CleaningTask).filter(CleaningTask.status == CleaningStatus.scheduled).count()
    in_progress = db.query(CleaningTask).filter(CleaningTask.status == CleaningStatus.in_progress).count()
    start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    completed_today = (
        db.query(CleaningTask)
        .filter(
            CleaningTask.status == CleaningStatus.completed,
            CleaningTask.completed_at >= start_of_day,
        )
        .count()
    )
    rooms_need_cleaning = db.query(Room).filter(Room.status == RoomStatus.cleaning).count()
    return {
        "scheduled": pending,
        "in_progress": in_progress,
        "completed_today": completed_today,
        "rooms_marked_cleaning": rooms_need_cleaning,
    }


def stays_summary(db: Session) -> dict:
    active = db.query(Stay).filter(Stay.status == StayStatus.active).count()
    completed = db.query(Stay).filter(Stay.status == StayStatus.completed).count()
    return {"active_stays": active, "completed_stays": completed}
