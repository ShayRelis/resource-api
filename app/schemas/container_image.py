from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContainerImageCreate(BaseModel):
    name: str
    tag: str
    registry_id: int
    pushed_at: datetime


class ContainerImageUpdate(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = None
    registry_id: Optional[int] = None
    pushed_at: Optional[datetime] = None


class ContainerImageResponse(BaseModel):
    id: int
    name: str
    tag: str
    registry_id: int
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

