from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from app.db.database import TenantBase

class ContainerImage(TenantBase):
    __tablename__ = "container_images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    registry_id = Column(Integer, ForeignKey("registries.id"))
    pushed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())