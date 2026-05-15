import enum
from datetime import date

from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)
    notes = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", backref="bookings")
    guest = relationship("Guest", backref="bookings")

    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    @staticmethod
    def validate_dates(check_in: date, check_out: date) -> None:
        if check_out <= check_in:
            raise ValueError("Дата выезда должна быть позже даты заезда")
        if (check_out - check_in).days > 365:
            raise ValueError("Бронирование не может превышать 365 ночей")
