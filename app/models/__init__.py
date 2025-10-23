"""SQLAlchemy models package."""

from app.db.database import Base

from .cloud_provider import CloudProvider
from .company import Company
from .component import Component, component_teams, component_tags, component_container_images, component_versions
from .container_image import ContainerImage
from .registry import Registry
from .registry_credential import RegistryCredential
from .registry_provider import RegistryProvider
from .service_type import ServiceType
from .tag import Tag
from .team import Team
from .user import UserRole, User
from .version import Version, version_container_images


# Make all models available at package level
__all__ = [
    "Base",
    "CloudProvider",
    "Company",
    "Component",
    "component_teams",
    "component_tags",
    "component_container_images",
    "component_versions",
    "ContainerImage",
    "Registry",
    "RegistryCredential",
    "RegistryProvider",
    "ServiceType",
    "Tag",
    "Team",
    "User",
    "UserRole",
    "Version",
    "version_container_images",
]
