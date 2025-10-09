from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegistryCredentialCreate(BaseModel):
    name: str
    access_key: str
    secret_key: str
    region: str
    registry_provider_id: int


class RegistryCredentialUpdate(BaseModel):
    name: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    region: Optional[str] = None
    registry_provider_id: Optional[int] = None


class RegistryCredentialResponse(BaseModel):
    id: int
    name: str
    access_key: str
    secret_key: str
    region: str
    registry_provider_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

