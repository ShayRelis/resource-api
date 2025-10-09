from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegistryCreate(BaseModel):
    name: str
    url: str
    is_private: bool = True
    registry_provider_id: int
    registry_credentials_id: Optional[int] = None


class RegistryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    is_private: Optional[bool] = None
    registry_provider_id: Optional[int] = None
    registry_credentials_id: Optional[int] = None


class RegistryResponse(BaseModel):
    id: int
    name: str
    url: str
    is_private: bool
    registry_provider_id: int
    registry_credentials_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

