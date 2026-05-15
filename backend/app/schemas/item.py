"""Pydantic-схемы для /items (задание 1, 10 — валидация кода номера)."""

import re
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.room import Room, RoomStatus, RoomType
from app.services.room_score import calculate_room_attractiveness_score

ROOM_CODE_PATTERN = re.compile(r"^[A-Z]{1,2}-\d{1,2}-\d{2,3}$")


class ItemBase(BaseModel):
    number: Annotated[str, Field(min_length=3, max_length=20, description="Код номера AB-3-12")]
    room_type: RoomType = RoomType.standard
    price_per_night: float = Field(gt=0, le=1_000_000)
    capacity: int = Field(ge=1, le=10)
    floor: int = Field(ge=-2, le=200)
    description: str = Field(default="", max_length=500)

    @field_validator("number")
    @classmethod
    def validate_room_code(cls, value: str) -> str:
        code = value.strip().upper()
        if not ROOM_CODE_PATTERN.match(code):
            raise ValueError(
                "number must match format: CORPUS-FLOOR-ROOM (e.g. AB-3-12, A-1-05)"
            )
        return code

    @field_validator("description")
    @classmethod
    def forbid_html(cls, value: str) -> str:
        if "<" in value or ">" in value:
            raise ValueError("description must not contain HTML tags.")
        return value


class ItemCreate(ItemBase):
    status: RoomStatus = RoomStatus.available


class ItemUpdate(BaseModel):
    number: str | None = Field(default=None, min_length=3, max_length=20)
    room_type: RoomType | None = None
    price_per_night: float | None = Field(default=None, gt=0, le=1_000_000)
    capacity: int | None = Field(default=None, ge=1, le=10)
    floor: int | None = Field(default=None, ge=-2, le=200)
    status: RoomStatus | None = None
    description: str | None = Field(default=None, max_length=500)

    @field_validator("number")
    @classmethod
    def validate_room_code_optional(cls, value: str | None) -> str | None:
        if value is None:
            return value
        code = value.strip().upper()
        if not ROOM_CODE_PATTERN.match(code):
            raise ValueError("number must match format CORPUS-FLOOR-ROOM (e.g. AB-3-12)")
        return code

    @model_validator(mode="after")
    def ensure_any_field_present(self) -> "ItemUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided for update.")
        return self


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: RoomStatus
    attractiveness_score: int = 0

    @classmethod
    def from_room(cls, room: Room) -> "ItemResponse":
        score = calculate_room_attractiveness_score(
            price_per_night=room.price_per_night,
            room_type=room.room_type,
            status=room.status,
            capacity=room.capacity,
            floor=room.floor,
        )
        return cls(
            id=room.id,
            number=room.number,
            room_type=room.room_type,
            price_per_night=room.price_per_night,
            capacity=room.capacity,
            floor=room.floor,
            description=room.description or "",
            status=room.status,
            attractiveness_score=score,
        )
