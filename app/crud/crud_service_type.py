"""CRUD operations for ServiceType model."""

from app.crud.base import CRUDBase
from app.models import ServiceType
from app.schemas import ServiceTypeCreate, ServiceTypeUpdate


class CRUDServiceType(CRUDBase[ServiceType, ServiceTypeCreate, ServiceTypeUpdate]):
    """CRUD operations for ServiceType model."""
    pass


# Create instance
service_type = CRUDServiceType(ServiceType)

