"""CRUD operations for RegistryProvider model."""

from app.crud.base import CRUDBase
from app.models import RegistryProvider
from app.schemas import RegistryProviderCreate, RegistryProviderUpdate


class CRUDRegistryProvider(CRUDBase[RegistryProvider, RegistryProviderCreate, RegistryProviderUpdate]):
    """CRUD operations for RegistryProvider model."""
    pass


# Create instance
registry_provider = CRUDRegistryProvider(RegistryProvider)

