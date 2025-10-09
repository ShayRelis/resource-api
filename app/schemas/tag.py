from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str
    company_id: int


class TagUpdate(BaseModel):
    name: Optional[str] = None
    company_id: Optional[int] = None


class TagResponse(BaseModel):
    id: int
    name: str
    company_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

