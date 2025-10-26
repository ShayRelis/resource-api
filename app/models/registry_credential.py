from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.database import TenantBase

class RegistryCredential(TenantBase):
    __tablename__ = "registry_credentials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    access_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    region = Column(String, nullable=False)
    registry_provider_id = Column(Integer, ForeignKey("registry_providers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())