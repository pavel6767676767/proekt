from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Status = Literal["available", "maintenance"]


class MachineBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str = ""
    image_url: str | None = None
    specs: dict[str, str] = Field(default_factory=dict)
    quantity: int = Field(default=1, ge=1)
    status: Status = "available"
    zone_id: int


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    image_url: str | None = None
    specs: dict[str, str] | None = None
    quantity: int | None = Field(default=None, ge=1)
    status: Status | None = None
    zone_id: int | None = None


class MachineOut(MachineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
