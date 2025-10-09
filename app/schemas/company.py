from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str


class CompanyUpdate(BaseModel):
    name: Optional[str] = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

