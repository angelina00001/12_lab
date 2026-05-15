from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(50))
    passport_number = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
