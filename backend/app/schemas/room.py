from pydantic import BaseModel, ConfigDict, Field

from app.models.room import RoomStatus, RoomType


class RoomBase(BaseModel):
    number: str = Field(min_length=1, max_length=20)
    room_type: RoomType = RoomType.standard
    price_per_night: float = Field(gt=0, le=1_000_000)
    capacity: int = Field(ge=1, le=10)
    floor: int = Field(ge=-2, le=200)
    description: str = Field(default="", max_length=500)


class RoomCreate(RoomBase):
    status: RoomStatus = RoomStatus.available


class RoomUpdate(BaseModel):
    number: str | None = Field(default=None, min_length=1, max_length=20)
    room_type: RoomType | None = None
    price_per_night: float | None = Field(default=None, gt=0, le=1_000_000)
    capacity: int | None = Field(default=None, ge=1, le=10)
    floor: int | None = Field(default=None, ge=-2, le=200)
    status: RoomStatus | None = None
    description: str | None = Field(default=None, max_length=500)


class RoomResponse(RoomBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: RoomStatus
