import enum

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, func

from app.database import Base


class RoomType(str, enum.Enum):
    standard = "standard"
    deluxe = "deluxe"
    suite = "suite"


class RoomStatus(str, enum.Enum):
    available = "available"
    occupied = "occupied"
    maintenance = "maintenance"
    cleaning = "cleaning"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), unique=True, nullable=False, index=True)
    room_type = Column(Enum(RoomType), default=RoomType.standard, nullable=False)
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, default=2, nullable=False)
    status = Column(Enum(RoomStatus), default=RoomStatus.available, nullable=False)
    floor = Column(Integer, default=1)
    description = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
