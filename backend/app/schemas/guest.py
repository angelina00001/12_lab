from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GuestBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    passport_number: str | None = Field(default=None, max_length=50)


class GuestCreate(GuestBase):
    pass


class GuestUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    passport_number: str | None = Field(default=None, max_length=50)


class GuestResponse(GuestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
