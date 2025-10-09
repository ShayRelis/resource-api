from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ServiceTypeCreate(BaseModel):
    name: str
    description: str
    is_managed: bool = True


class ServiceTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_managed: Optional[bool] = None


class ServiceTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    is_managed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

