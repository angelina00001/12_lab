from datetime import date, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.guest import Guest
from app.models.room import Room, RoomStatus, RoomType
from app.schemas.booking import BookingCreate
from app.services import booking_service


@pytest.fixture()
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    room = Room(number="T1", room_type=RoomType.standard, price_per_night=1000, capacity=2)
    guest = Guest(full_name="Test Guest", email="guest@test.com")
    session.add_all([room, guest])
    session.commit()
    yield session, room, guest
    session.close()


def test_calculate_total_price(db):
    _, room, _ = db
    check_in = date(2026, 6, 1)
    check_out = date(2026, 6, 4)
    assert booking_service.calculate_total_price(room, check_in, check_out) == 3000.0


def test_calculate_zero_nights_raises(db):
    _, room, _ = db
    d = date(2026, 6, 1)
    with pytest.raises(ValueError):
        booking_service.calculate_total_price(room, d, d)


def test_has_overlapping_empty(db):
    session, room, _ = db
    check_in = date(2026, 7, 1)
    check_out = check_in + timedelta(days=2)
    assert not booking_service.has_overlapping_booking(session, room.id, check_in, check_out)


def test_create_booking_success(db):
    session, room, guest = db
    check_in = date(2026, 8, 1)
    check_out = check_in + timedelta(days=2)
    data = BookingCreate(room_id=room.id, guest_id=guest.id, check_in=check_in, check_out=check_out)
    booking = booking_service.create_booking(session, data, created_by_id=1)
    assert booking.total_price == 2000.0


def test_create_booking_room_not_found(db):
    session, _, guest = db
    check_in = date(2026, 8, 1)
    check_out = check_in + timedelta(days=1)
    data = BookingCreate(room_id=999, guest_id=guest.id, check_in=check_in, check_out=check_out)
    with pytest.raises(ValueError, match="Номер не найден"):
        booking_service.create_booking(session, data, None)
