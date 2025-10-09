"""CRUD operations for RegistryCredential model."""

from app.crud.base import CRUDBase
from app.models import RegistryCredential
from app.schemas import RegistryCredentialCreate, RegistryCredentialUpdate


class CRUDRegistryCredential(CRUDBase[RegistryCredential, RegistryCredentialCreate, RegistryCredentialUpdate]):
    """CRUD operations for RegistryCredential model."""
    pass


# Create instance
registry_credential = CRUDRegistryCredential(RegistryCredential)

