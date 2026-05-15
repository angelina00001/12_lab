from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    room_id: int
    guest_id: int
    check_in: date
    check_out: date
    notes: str = Field(default="", max_length=500)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("Дата выезда должна быть позже даты заезда")
        return self


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    check_in: date | None = None
    check_out: date | None = None
    status: BookingStatus | None = None
    notes: str | None = Field(default=None, max_length=500)


class BookingResponse(BookingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_price: float
    status: BookingStatus
    nights: int = 0
