from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.cleaning import CleaningStatus


class CleaningTaskCreate(BaseModel):
    room_id: int
    assigned_to_id: int | None = None
    scheduled_at: datetime
    notes: str = Field(default="", max_length=500)


class CleaningTaskUpdate(BaseModel):
    assigned_to_id: int | None = None
    scheduled_at: datetime | None = None
    status: CleaningStatus | None = None
    notes: str | None = Field(default=None, max_length=500)


class CleaningTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    assigned_to_id: int | None
    scheduled_at: datetime
    completed_at: datetime | None
    status: CleaningStatus
    notes: str
