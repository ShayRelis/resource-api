from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class VersionCreate(BaseModel):
    name: str
    container_image_ids: List[int] = []


class VersionUpdate(BaseModel):
    name: Optional[str] = None
    container_image_ids: Optional[List[int]] = None


class VersionResponse(BaseModel):
    id: int
    name: str
    container_image_ids: List[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

