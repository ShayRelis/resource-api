"""CRUD operations package."""

from app.crud.crud_user import user
from app.crud.crud_company import company
from app.crud.crud_team import team
from app.crud.crud_cloud_provider import cloud_provider
from app.crud.crud_registry_provider import registry_provider
from app.crud.crud_registry import registry
from app.crud.crud_registry_credential import registry_credential
from app.crud.crud_container_image import container_image
from app.crud.crud_service_type import service_type
from app.crud.crud_tag import tag
from app.crud.crud_version import version

__all__ = [
    "user",
    "company",
    "team",
    "cloud_provider",
    "registry_provider",
    "registry",
    "registry_credential",
    "container_image",
    "service_type",
    "tag",
    "version",
]

