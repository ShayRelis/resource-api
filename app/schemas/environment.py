from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnvironmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    version_id: int
    company_id: int


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version_id: Optional[int] = None
    company_id: Optional[int] = None


class EnvironmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    version_id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

