"""CRUD operations for Registry model."""

from app.crud.base import CRUDBase
from app.models import Registry
from app.schemas import RegistryCreate, RegistryUpdate


class CRUDRegistry(CRUDBase[Registry, RegistryCreate, RegistryUpdate]):
    """CRUD operations for Registry model."""
    pass


# Create instance
registry = CRUDRegistry(Registry)

