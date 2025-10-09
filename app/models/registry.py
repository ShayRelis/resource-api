from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base

class Registry(Base):
    __tablename__ = "registries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    is_private = Column(Boolean, default=True, nullable=False)
    registry_provider_id = Column(Integer, ForeignKey("registry_providers.id"))
    registry_credentials_id = Column(Integer, ForeignKey("registry_credentials.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())