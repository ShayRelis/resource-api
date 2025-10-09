from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    company_id: int


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    company_id: Optional[int] = None


class TeamResponse(BaseModel):
    id: int
    name: str
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

