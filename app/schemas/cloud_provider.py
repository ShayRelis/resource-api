from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CloudProviderCreate(BaseModel):
    name: str


class CloudProviderUpdate(BaseModel):
    name: Optional[str] = None


class CloudProviderResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

