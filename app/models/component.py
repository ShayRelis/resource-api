from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.sql import func

from app.db.database import TenantBase

# Association table for many-to-many relationship between Component and Team
component_teams = Table(
    'component_teams',
    TenantBase.metadata,
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

# Association table for many-to-many relationship between Component and Tag
component_tags = Table(
    'component_tags',
    TenantBase.metadata,
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

# Association table for many-to-many relationship between Component and ContainerImage
component_container_images = Table(
    'component_container_images',
    TenantBase.metadata,
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True),
    Column('container_image_id', Integer, ForeignKey('container_images.id'), primary_key=True)
)

# Association table for many-to-many relationship between Component and Version
component_versions = Table(
    'component_versions',
    TenantBase.metadata,
    Column('component_id', Integer, ForeignKey('components.id'), primary_key=True),
    Column('version_id', Integer, ForeignKey('versions.id'), primary_key=True)
)

class Component(TenantBase):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    repository_url = Column(String, nullable=True)
    is_managed = Column(Boolean, default=True, nullable=False)
    is_third_party = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

