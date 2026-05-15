from sqlalchemy.orm import Session

from app.auth.security import get_password_hash
from app.models.guest import Guest
from app.models.room import Room, RoomStatus, RoomType
from app.models.user import User, UserRole


def seed_database(db: Session) -> None:
    if db.query(User).filter(User.email == "admin@hotel.example.com").first():
        return

    admin = User(
        email="admin@hotel.example.com",
        full_name="Администратор",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.admin,
    )
    staff = User(
        email="staff@hotel.example.com",
        full_name="Сотрудник ресепшн",
        hashed_password=get_password_hash("staff123"),
        role=UserRole.staff,
    )
    db.add_all([admin, staff])

    rooms = [
        Room(number="A-1-01", room_type=RoomType.standard, price_per_night=3500, capacity=2, floor=1),
        Room(number="A-1-02", room_type=RoomType.standard, price_per_night=3500, capacity=2, floor=1),
        Room(number="B-2-01", room_type=RoomType.deluxe, price_per_night=5500, capacity=3, floor=2),
        Room(number="C-3-01", room_type=RoomType.suite, price_per_night=12000, capacity=4, floor=3, status=RoomStatus.available),
    ]
    db.add_all(rooms)

    guests = [
        Guest(full_name="Иван Петров", email="ivan@example.com", phone="+79001234567"),
        Guest(full_name="Мария Сидорова", email="maria@example.com", phone="+79007654321"),
    ]
    db.add_all(guests)
    db.commit()
