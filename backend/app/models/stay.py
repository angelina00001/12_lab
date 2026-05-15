import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.database import Base


class StayStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    no_show = "no_show"


class Stay(Base):
    __tablename__ = "stays"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    actual_check_in = Column(DateTime(timezone=True))
    actual_check_out = Column(DateTime(timezone=True))
    status = Column(Enum(StayStatus), default=StayStatus.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", backref="stay", uselist=False)
