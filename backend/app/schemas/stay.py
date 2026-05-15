from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.stay import StayStatus


class StayCreate(BaseModel):
    booking_id: int


class StayCheckIn(BaseModel):
    actual_check_in: datetime | None = None


class StayCheckOut(BaseModel):
    actual_check_out: datetime | None = None


class StayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: int
    actual_check_in: datetime | None
    actual_check_out: datetime | None
    status: StayStatus
