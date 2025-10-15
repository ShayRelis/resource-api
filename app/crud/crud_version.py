"""CRUD operations for Version model."""

from app.crud.base import CRUDBase
from app.models import Version
from app.schemas import VersionCreate, VersionUpdate


class CRUDVersion(CRUDBase[Version, VersionCreate, VersionUpdate]):
    """CRUD operations for Version model."""
    pass


# Create instance
version = CRUDVersion(Version)

