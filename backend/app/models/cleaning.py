import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class CleaningStatus(str, enum.Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class CleaningTask(Base):
    __tablename__ = "cleaning_tasks"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    status = Column(Enum(CleaningStatus), default=CleaningStatus.scheduled, nullable=False)
    notes = Column(String(500), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", backref="cleaning_tasks")
    assigned_to = relationship("User", backref="cleaning_tasks")
