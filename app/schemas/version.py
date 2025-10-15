from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VersionCreate(BaseModel):
    name: str


class VersionUpdate(BaseModel):
    name: Optional[str] = None


class VersionResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

