from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegistryProviderCreate(BaseModel):
    name: str


class RegistryProviderUpdate(BaseModel):
    name: Optional[str] = None


class RegistryProviderResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

