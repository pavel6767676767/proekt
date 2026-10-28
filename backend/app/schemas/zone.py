from pydantic import BaseModel, ConfigDict, Field

from app.schemas.machine import MachineOut


class ZoneBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = ""


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class ZoneOut(ZoneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    machines_count: int = 0


class ZoneDetail(ZoneOut):
    machines: list[MachineOut] = []
