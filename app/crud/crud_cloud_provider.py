"""CRUD operations for CloudProvider model."""

from app.crud.base import CRUDBase
from app.models import CloudProvider
from app.schemas import CloudProviderCreate, CloudProviderUpdate


class CRUDCloudProvider(CRUDBase[CloudProvider, CloudProviderCreate, CloudProviderUpdate]):
    """CRUD operations for CloudProvider model."""
    pass


# Create instance
cloud_provider = CRUDCloudProvider(CloudProvider)

