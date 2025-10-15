from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base

# Association table for many-to-many relationship between Version and ContainerImage
version_container_images = Table(
    'version_container_images',
    Base.metadata,
    Column('version_id', Integer, ForeignKey('versions.id'), primary_key=True),
    Column('container_image_id', Integer, ForeignKey('container_images.id'), primary_key=True)
)

class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

