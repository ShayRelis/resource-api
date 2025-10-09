"""CRUD operations for ContainerImage model."""

from app.crud.base import CRUDBase
from app.models import ContainerImage
from app.schemas import ContainerImageCreate, ContainerImageUpdate


class CRUDContainerImage(CRUDBase[ContainerImage, ContainerImageCreate, ContainerImageUpdate]):
    """CRUD operations for ContainerImage model."""
    pass


# Create instance
container_image = CRUDContainerImage(ContainerImage)

